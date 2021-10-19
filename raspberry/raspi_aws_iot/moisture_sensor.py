import json

from raspi_aws_iot.adc_device import ADS7830
from raspi_aws_iot.config import MOISTURE_MAX, MOISTURE_MIN, MOISTURE_PATH
from raspi_aws_iot.utils import LastSentUtils
from raspi_aws_iot.mqtt import MQTTConnection

class MoistureSensor:

    def __init__(self, adc, chn, max_v, min_v):
        self.adc = adc
        self.chn = chn
        self.max_v = max_v
        self.min_v = min_v

    def read_humidity(self):
        value_read = self.adc.analogRead(self.chn)
        value_perc = (value_read - self.max_v) / (self.max_v - self.min_v) * 100
        value_perc = min(max(value_perc, 100), 0)
        humidity = 100 - value_perc
        return humidity


class MoistureStreamMQTT:
    def __init__(self, channels, mqtt: MQTTConnection, topic):
        self.mqtt = mqtt
        self.topic = topic
        self.last_sent_utils = LastSentUtils(f"{MOISTURE_PATH}/last_sent.txt")
        self.sensors = {}

        adc = ADS7830()
        for c in channels:
            self.sensors[c] = MoistureSensor(adc, c, MOISTURE_MAX, MOISTURE_MIN)

    def upload_moistures(self):
        msg = {c: self.sensors[c].read_humidity() for c in self.sensors}
        msg = json.dumps(msg)
        open(f"{MOISTURE_PATH}/moisture.json", "w").write(msg)
        self.mqtt.send_message(self.topic, msg)

    def remove_last_sent(self):
        self.last_sent_utils.remove_last_sent()

    def send_moistures(self, interval_min=1):
        if self.last_sent_utils.check_upload(interval_min):
            self.upload_moistures()
            self.last_sent_utils.update_last_sent()
        

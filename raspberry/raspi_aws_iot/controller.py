from raspi_aws_iot.messages import Message, MsgType
import json
from gpiozero import LED


class Controller:
    def __init__(self, leds):
        self.leds = {}
        for name, l in leds.items():
            self.leds[name] = LED(l)

    def parse_msg(self, msg: str):
        msg = Message.parse_obj(json.loads(msg))
        if msg.msg_type == MsgType.LED:
            self.control_leds(msg.msg_body.leds, msg.msg_body.statuses)

    def control_leds(self, leds, statues):
        for i, l in enumerate(leds):
            if l in self.leds:
                if statues[i]:
                    self.leds[l].on()
                else:
                    self.leds[l].off()

        
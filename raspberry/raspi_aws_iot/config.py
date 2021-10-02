from uuid import uuid4

class MQTTConfig:
    TOPIC = "raspberry-aws-iot/dev"
    PORT = 443
    ROOT_CA = "/home/pi/.aws/Amazon-root-CA-1.pem"
    CERT = "/home/pi/.aws/device.pem.crt"
    KEY = "/home/pi/.aws/private.pem.key"
    ENDPOINT = "a3ig8qh8u66gen-ats.iot.eu-west-1.amazonaws.com"
    CLIENT_ID = "raspberry-" + str(uuid4())


class DeviceConfig:
    LEDS = {
        "green": 17,
        "yellow": 22,
        "red": 6
    }



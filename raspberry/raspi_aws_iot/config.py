from uuid import uuid4

BASE_TOPIC = "matt-iot/dev"
CLIENT_ID = "1"

CAMERA_TOPIC = f"{BASE_TOPIC}/camera/{CLIENT_ID}"
CMD_TOPIC = f"{BASE_TOPIC}/cmd"

PORT = 443

ROOT_CA = "/home/pi/.aws/Amazon-root-CA-1.pem"
CERT = "/home/pi/.aws/device.pem.crt"
KEY = "/home/pi/.aws/private.pem.key"
ENDPOINT = "a3ig8qh8u66gen-ats.iot.eu-west-1.amazonaws.com"

IMG_PATH = "/home/pi/pictures/tmp.jpg"
LAST_IMG_SENT_PATH = "/home/pi/pictures/last_sent.txt"

LEDS = {
    "green": 17,
    "yellow": 22,
    "red": 6
}

CAMERA_RESOLUTION = (512, 320)
CAMERA_INTERVAL_MIN = 10




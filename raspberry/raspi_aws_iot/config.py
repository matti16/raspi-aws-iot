BASE_TOPIC = "matt-iot/dev"
CLIENT_ID = "1"

PORT = 443
ROOT_CA = "/home/pi/.aws/Amazon-root-CA-1.pem"
CERT = "/home/pi/.aws/device.pem.crt"
KEY = "/home/pi/.aws/private.pem.key"
ENDPOINT = "a3ig8qh8u66gen-ats.iot.eu-west-1.amazonaws.com"


CMD_TOPIC = f"{BASE_TOPIC}/cmd"

LEDS = {
    "green": 17,
    "yellow": 22,
    "red": 6
}


OUTPUT_FOLDER = "/home/pi/raspi-aws-iot/raspberry/tmp"

CAMERA_TOPIC = f"{BASE_TOPIC}/camera/{CLIENT_ID}"
CAMERA_RESOLUTION = (500, 300)
CAMERA_INTERVAL_MIN = 10
CAMERA_PATH = f"{OUTPUT_FOLDER}/pictures"


MOISTURE_TOPIC = f"{BASE_TOPIC}/moisture/{CLIENT_ID}"
MOISTURE_SENSORS_CHANNELS = [0]
MOISTURE_INTERVAL_MIN = 10
MOISTURE_MAX = 230
MOISTURE_MIN = 100
MOISTURE_PATH = f"{OUTPUT_FOLDER}/moisture"




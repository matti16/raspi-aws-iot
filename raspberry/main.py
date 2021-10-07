import time
import traceback

from raspi_aws_iot.mqtt import MQTTConnection
from raspi_aws_iot.config import *
from raspi_aws_iot.controller import Controller
from raspi_aws_iot.camera_stream import Camera, CameraStreamMQTT

ctrl = Controller(LEDS)


def on_msg_received(topic, payload, dup, qos, retain, **kwargs):
    print(f"Received message from topic '{topic}': {payload}")
    try:
        ctrl.parse_msg(payload)
    except Exception as e:
        print(e)


def main():
    mqtt_connection = MQTTConnection(ENDPOINT, PORT, CERT, KEY, ROOT_CA, CLIENT_ID)
    mqtt_connection.connect()
    mqtt_connection.subscribe(CMD_TOPIC, on_msg_received)

    camera = Camera(IMG_PATH, CAMERA_RESOLUTION)
    camera_stream = CameraStreamMQTT(camera, mqtt_connection, CAMERA_TOPIC, LAST_IMG_SENT_PATH)

    while True:
        try:
            camera_stream.send_picture(interval_min=CAMERA_INTERVAL_MIN)
            time.sleep(5)
        except Exception:
            mqtt_connection.disconnect()
            print(traceback.format_exc())
            break

if __name__ == '__main__':
    main()
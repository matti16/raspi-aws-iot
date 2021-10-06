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


def main(
    endpoint=ENDPOINT, 
    port=PORT, 
    cert=CERT, 
    key=KEY, 
    root_ca=ROOT_CA, 
    client_id=CLIENT_ID, 
    topic=BASE_TOPIC
    ):
    mqtt_connection = MQTTConnection(endpoint, port, cert, key, root_ca, client_id)
    mqtt_connection.connect()
    mqtt_connection.subscribe(topic, on_msg_received)

    camera = Camera(IMG_PATH)
    camera_stream = CameraStreamMQTT(camera, mqtt_connection, CAMERA_TOPIC, IMG_PATH)

    while True:
        try:
            camera_stream.send_picture()
            time.sleep(5)
        except Exception:
            mqtt_connection.disconnect()
            print(traceback.format_exc())
            break

if __name__ == '__main__':
    main()
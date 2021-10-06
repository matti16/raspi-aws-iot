import time
import base64
import schedule

from picamera import PiCamera
from raspi_aws_iot.mqtt import MQTTConnection

class Camera:
    def __init__(self, img_path):
        self.camera = PiCamera()
        self.camera.resolution = (1280, 720)
        self.camera.vflip = True
        self.camera.contrast = 10
        time.sleep(3)
        self.img_path = img_path

    def _capture_img(self):
        self.camera.capture(self.img_path)
    
    def get_img(self):
        self._capture_img()
        with open(self.img_path, "rb") as image_file:
            binary_img = image_file.read()
        return binary_img

    

class CameraStreamMQTT:
    def __init__(self, camera: Camera, mqtt: MQTTConnection, topic):
        self.camera = camera
        self.mqtt = mqtt
        self.topic = topic
    
    def upload_picture(self):
        binary_img = self.camera.get_img()
        self.mqtt.send_message(self.topic, binary_img)

    def schedule_stream(self, interval_min=1):
        print(f"Scheduling camera strean every {interval_min} minutes")
        schedule.every(interval_min).minutes.do(self.upload_picture)

        



    

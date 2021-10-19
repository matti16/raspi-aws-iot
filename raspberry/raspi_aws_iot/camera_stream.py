import os
import time

from datetime import datetime

from picamera import PiCamera
from raspi_aws_iot.mqtt import MQTTConnection
from raspi_aws_iot.utils import LastSentUtils

class Camera:
    def __init__(self, camera_path, resolution):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.vflip = True
        self.camera.contrast = 10
        time.sleep(3)
        self.camera_path = camera_path
        self.img_path = f"{self.camera_path}/tmp.jpg"

    def _capture_img(self):
        self.camera.capture(self.img_path)
    
    def get_img(self):
        self._capture_img()
        with open(self.img_path, "rb") as image_file:
            img_bytes = image_file.read()
        return img_bytes

    

class CameraStreamMQTT:
    def __init__(self, camera: Camera, mqtt: MQTTConnection, topic):
        self.camera = camera
        self.mqtt = mqtt
        self.topic = topic
        self.last_sent_utils = LastSentUtils(f"{camera.camera_path}/last_sent.txt")
    
    def upload_picture(self):
        img_bytes = self.camera.get_img()
        self.mqtt.send_message(self.topic, img_bytes)

    def remove_last_sent(self):
        self.last_sent_utils.remove_last_sent()

    def send_picture(self, interval_min=1):
        if self.last_sent_utils.check_upload(interval_min):
            self.upload_picture()
            self.last_sent_utils.update_last_sent()
        



    

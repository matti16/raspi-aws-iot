import os
import time

from datetime import datetime

from picamera import PiCamera
from raspi_aws_iot.mqtt import MQTTConnection

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
        self.last_sent_file = f"{camera.camera_path}/last_sent.txt"
        self.date_fmt = "%Y-%m-%d %H:%M:%S"

        directory = os.path.dirname(self.last_sent_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def upload_picture(self):
        img_bytes = self.camera.get_img()
        self.mqtt.send_message(self.topic, img_bytes)

    def remove_last_sent(self):
        if not os.path.exists(self.last_sent_file):
            os.remove(self.last_sent_file)

    def check_upload(self, interval_min):
        if os.path.exists(self.last_sent_file):
            last_sent = open(self.last_sent_file, "r").read()
            last_sent = datetime.strptime(last_sent, self.date_fmt)
            now = datetime.now()
            return (now - last_sent).seconds > interval_min * 60
        else:
            return True    

    def send_picture(self, interval_min=1):
        if self.check_upload(interval_min):
            self.upload_picture()
        
            with open(self.last_sent_file, "w") as f:
                now = datetime.now()
                f.write(now.strftime(self.date_fmt))
        



    

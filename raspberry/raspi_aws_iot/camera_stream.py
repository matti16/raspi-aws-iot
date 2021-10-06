import os
import time
import base64

from datetime import datetime
import json

from picamera import PiCamera
from raspi_aws_iot.mqtt import MQTTConnection

class Camera:
    def __init__(self, img_path):
        self.camera = PiCamera()
        self.camera.resolution = (690, 360)
        self.camera.vflip = True
        self.camera.contrast = 10
        time.sleep(3)
        self.img_path = img_path

    def _capture_img(self):
        self.camera.capture(self.img_path)
    
    def get_img(self):
        self._capture_img()
        with open(self.img_path, "rb") as image_file:
            encoded_string = base64.encodebytes(image_file.read()).decode('utf-8')
        return encoded_string

    

class CameraStreamMQTT:
    def __init__(self, camera: Camera, mqtt: MQTTConnection, topic, last_sent_file: str):
        self.camera = camera
        self.mqtt = mqtt
        self.topic = topic
        self.last_sent_file = last_sent_file
        self.date_fmt = "%Y-%m-%d %H:%M:%S"

        directory = os.path.dirname(last_sent_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def upload_picture(self):
        encoded_pic = self.camera.get_img()
        msg = {"img": encoded_pic}
        msg = json.dumps(msg)
        self.mqtt.send_message(self.topic, msg)

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
            print(f"Sending camera stream")
            self.upload_picture()
        
            with open(self.last_sent_file, "w") as f:
                now = datetime.now()
                f.write(now.strftime(self.date_fmt))
        



    

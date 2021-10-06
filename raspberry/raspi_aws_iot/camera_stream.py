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
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    

class CameraStreamMQTT:
    def __init__(self, camera: Camera, mqtt: MQTTConnection, topic):
        self.camera = camera
        self.mqtt = mqtt
        self.topic = topic
    
    def upload_picture(self):
        encoded_pic = self.camera.get_img()
        msg = {
            "img": encoded_pic
        }
        self.mqtt.send_message(self.topic, msg)

    def schedule_stream(self, interval_min=1):
        schedule.every(interval_min).minutes.do(self.upload_picture)

        



    

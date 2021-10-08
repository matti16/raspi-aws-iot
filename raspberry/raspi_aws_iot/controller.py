from raspi_aws_iot.messages import Message, MsgType
import json
from gpiozero import LED


class Controller:
    def __init__(self, leds, camera=None):
        self.leds = {}
        for name, l in leds.items():
            self.leds[name] = LED(l)
        self.camera = camera

    def parse_msg(self, msg: str):
        msg = Message.parse_obj(json.loads(msg))
        if msg.msg_type == MsgType.LED:
            self.control_leds(msg.msg_body.leds, msg.msg_body.status)
        elif msg.msg_type == MsgType.CAMERA:
            self.control_reset_camera()

    def control_leds(self, leds, statues):
        for i, l in enumerate(leds):
            if l in self.leds:
                if statues[i]:
                    self.leds[l].on()
                else:
                    self.leds[l].off()
    
    def control_reset_camera(self):
        self.camera.remove_last_sent()

        
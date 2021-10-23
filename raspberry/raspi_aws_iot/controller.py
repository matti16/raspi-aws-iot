from raspi_aws_iot.messages import Message, MsgType
import json
import time
from gpiozero import LED, OutputDevice


class Controller:
    def __init__(self, leds, watering=[], camera=None, moistures=None):
        self.leds = {}
        for name, l in leds.items():
            self.leds[name] = LED(l)
        
        self.waterings = []
        for w in watering:
            self.waterings.append(OutputDevice(w, active_high=False, initial_value=True))

        self.camera = camera
        self.moistures = moistures

    def parse_msg(self, msg: str):
        msg = Message.parse_obj(json.loads(msg))
        if msg.msg_type == MsgType.LED:
            self.control_leds(msg.msg_body.leds, msg.msg_body.status)
        if msg.msg_type == MsgType.WATERING:
            self.control_leds(msg.msg_body.pumps, msg.msg_body.durations)
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

    def control_reset_moistures(self):
        self.moistures.remove_last_sent()

    def control_waterings(self, pumps, durations):
        start = time.time()
        max_duration = max(durations)
        
        for i, p in enumerate(pumps):
            if durations[i] > 0:
                self.waterings[p].on()

        elapsed = time.time() - start
        while elapsed < max_duration:
            time.sleep(0.2)
            elapsed = time.time() - start
            for i, d in enumerate(durations):
                if elapsed >= d:
                    self.waterings[pumps[i]].off()
        
        for p in pumps:
            self.waterings[p].off()


        
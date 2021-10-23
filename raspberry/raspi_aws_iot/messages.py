from enum import Enum
from typing import Union, Optional
from pydantic import BaseModel

class MsgType(Enum):
    LED = "led"
    CAMERA = "camera"
    WATERING = "watering"


class LedCommand(BaseModel):
    leds: list
    status: list


class WateringCommand(BaseModel):
    pumps: list
    durations: list


class Message(BaseModel):
    msg_type: MsgType
    msg_body: Optional[Union[LedCommand, WateringCommand]] = None

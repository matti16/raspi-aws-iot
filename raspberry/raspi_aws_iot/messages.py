from enum import Enum
from typing import Union, Optional
from pydantic import BaseModel

class MsgType(Enum):
    LED = "led"
    CAMERA = "camera"


class LedCommand(BaseModel):
    leds: list
    status: list


class Message(BaseModel):
    msg_type: MsgType
    msg_body: Optional[Union[LedCommand]] = None

from enum import Enum
from typing import Union
from pydantic import BaseModel

class MsgType(Enum):
    LED = "led"


class LedCommand(BaseModel):
    leds: list
    statuses: list


class Message(BaseModel):
    msg_type: MsgType
    msg_body: Union[LedCommand]

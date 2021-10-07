import boto3
import json

from fastapi import FastAPI, Body
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, AnyStr

from config import *


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def send_mqtt_msg(msg):
    client = boto3.client('iot-data', region_name=REGION)
    response = client.publish(
        topic=IOT_TOPIC,
        qos=1,
        payload=json.dumps(msg)
    )
    return response
    

@app.post(f"{BASE_PATH}/cmd")
def cmd_handler(body: Dict[AnyStr, Any]):
    print(f"Received: {body}")
    body = {
        key.decode() if isinstance(key, bytes) else key:
        val.decode() if isinstance(val, bytes) else val
        for key, val in body.items()
    }
    send_mqtt_msg(body)
    return {"status": "OK"}

handler = Mangum(app)
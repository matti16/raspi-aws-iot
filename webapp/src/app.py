import boto3
import json

from fastapi import FastAPI, Body
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from .config import *


app = FastAPI(root_path=BASE_PATH)
app.add_middleware(CORSMiddleware, allow_origin_regex="*", allow_methods=["*"], allow_headers=["*"])

def send_mqtt_msg(msg):
    client = boto3.client('iot-data', region_name=REGION)
    response = client.publish(
        topic=IOT_TOPIC,
        qos=1,
        payload=json.dumps(msg)
    )
    return response
    

@app.post("/cmd")
def cmd_handler(body: Body(...)):
    print(f"Received: {body}")
    send_mqtt_msg(body)
    return {"status": "OK", "cmd": body}

handler = Mangum(app)
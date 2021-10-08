from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Dict, AnyStr, List

from config import BASE_PATH
from services import send_mqtt_msg, get_camera_images_from_s3
from models import CameraImageItem


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

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


@app.get(f"{BASE_PATH}/camera")
def get_camera_images() -> List[CameraImageItem]:
    result = get_camera_images_from_s3()
    return result



handler = Mangum(app)
from pydantic import BaseModel
import datetime

class CameraImageItem(BaseModel):
    device_id: str
    image_url: str
    last_modified_date: datetime.datetime
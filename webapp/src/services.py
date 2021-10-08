import boto3
import json

from config import REGION, IOT_TOPIC, DATA_BUCKET
from webapp.src.config import CAMERAS_PATH

from models import CameraImageItem

def send_mqtt_msg(msg):
    client = boto3.client('iot-data', region_name=REGION)
    response = client.publish(
        topic=IOT_TOPIC,
        qos=1,
        payload=json.dumps(msg)
    )
    return response


def get_camera_images_from_s3():
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = s3.Bucket(DATA_BUCKET)
    result = []
    for object_summary in bucket.objects.filter(Prefix=CAMERAS_PATH):
        key = object_summary.key
        if key.endswith(".jpg"):
            device_id = key.split("/")[2]
            summary_details = s3.ObjectSummary(DATA_BUCKET, key)
            last_modified_date = summary_details.last_modified

            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': DATA_BUCKET, 'Key': key},
                ExpiresIn=3600
            )

            result.append(CameraImageItem(
                device_id=device_id, 
                image_url=presigned_url, 
                last_modified_date=last_modified_date
            ))
    
    return result


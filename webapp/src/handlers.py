import boto3
import json
import os

REGION = os.getenv("REGION", "eu-west-1")
IOT_TOPIC = os.environ["IOT_TOPIC"]


def send_mqtt_msg(msg):
    client = boto3.client('iot-data', region_name=REGION)
    response = client.publish(
        topic=IOT_TOPIC,
        qos=1,
        payload=json.dumps(msg)
    )
    return response
    

def handler(event, context):
    print(f"Received event: {event}")
    body = json.loads(event["body"])
    
    print(f"Sending message: {body}")
    send_mqtt_msg(body)

    response = {
        "statusCode": 200,
        "body": body
    }
    print(f"Response: {response}")
    return response
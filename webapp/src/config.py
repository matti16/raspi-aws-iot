import os

REGION = os.getenv("REGION", "eu-west-1")
IOT_TOPIC = os.environ["IOT_TOPIC"]

BASE_PATH = "/api"

DATA_BUCKET = os.environ["DATA_BUCKET"]
CAMERAS_PATH = "camera/latest"

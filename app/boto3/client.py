import boto3

from app.core.config import SPACE_URL, SPACE_ACCESS_KEY_ID, SPACE_SECRET_ACCESS_KEY

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url=SPACE_URL,
    aws_access_key_id=SPACE_ACCESS_KEY_ID,
    aws_secret_access_key=SPACE_SECRET_ACCESS_KEY,
)

from minio import Minio
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, TEMPLATE_IMAGE_FILENAME_GET, BUCKET_NAME

try:
    client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)
    print("Connected to Minio")
    print("List of buckets = ", client.list_buckets())
except:
    print("Cannot connect to Minio")
    
    
def get_file(filename:str, bucket = BUCKET_NAME):
    client.fget_object(bucket, filename, TEMPLATE_IMAGE_FILENAME_GET)
    return TEMPLATE_IMAGE_FILENAME_GET
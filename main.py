from PIL import Image
import requests
from io import BytesIO
import sys
import boto3
from uuid import uuid4

AWS_ACCESS_KEY = ''
AWS_SECRET = ''
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET
)

url = sys.argv[1]
response = requests.get(url)
image = Image.open(BytesIO(response.content))

w, h = image.size
edge = min([w, h])
left = (w - edge) / 2
right = (w + edge) / 2
top = (h - edge) / 2
bottom = (h + edge) / 2

image = image.crop((left, top, right, bottom))
with BytesIO() as f:
    image.save(f, format='png')
    name = str(uuid4()) + '.png'
    f.seek(0)
    s3_client.upload_fileobj(f, 'flourish-directory-images', name, ExtraArgs={'ContentType': 'image/png'})

print('https://flourish-directory-images.s3.eu-west-2.amazonaws.com/' + name)

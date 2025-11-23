import os
import boto3
import logging
from io import BytesIO
from PIL import Image

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

# Environment variables
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
MAX_WIDTH     = int(os.environ.get('MAX_WIDTH', '800'))
MAX_HEIGHT    = int(os.environ.get('MAX_HEIGHT', '600'))

def resize_image(image: Image.Image) -> Image.Image:
    """
    Resize the given PIL Image to fit within (MAX_WIDTH, MAX_HEIGHT)
    preserving aspect ratio.
    """
    original_size = image.size
    image.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.LANCZOS)
    logger.info(f"Resized image from {original_size} to {image.size}")
    return image

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    for record in event.get('Records', []):
        try:
            bucket = record['s3']['bucket']['name']
            key    = record['s3']['object']['key']
            logger.info(f"Processing file {key} from bucket {bucket}")

            # Only process valid image extensions
            valid_ext = ('.jpg', '.jpeg', '.png', '.webp')
            if not key.lower().endswith(valid_ext):
                logger.info(f"Skipping non-image file: {key}")
                continue

            # Download the image into memory
            resp = s3.get_object(Bucket=bucket, Key=key)
            body = resp['Body'].read()
            image = Image.open(BytesIO(body))
            image = image.convert('RGB')  # Normalize format

            # Resize
            resized = resize_image(image)

            # Save to bytes
            buffer = BytesIO()
            resized.save(buffer, format='JPEG', quality=85)
            buffer.seek(0)

            # Prepare destination key
            dest_key = f"resized/{key}"

            # Upload
            s3.put_object(
                Bucket = OUTPUT_BUCKET,
                Key    = dest_key,
                Body   = buffer,
                ContentType = 'image/jpeg'
            )
            logger.info(f"Uploaded resized image to {OUTPUT_BUCKET}/{dest_key}")

        except Exception as e:
            logger.error(f"Error processing {key} from {bucket}: {e}", exc_info=True)
            raise

    return {
        'statusCode': 200,
        'body'      : 'Processing complete'
    }

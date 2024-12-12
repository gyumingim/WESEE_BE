import base64
from PIL import Image
import io

def save_image_from_base64(base64_image, save_path):
    image_bytes = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(image_bytes))
    image.save(save_path)
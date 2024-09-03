import base64
import json
import os
from io import BytesIO
import requests
from PIL import Image

# Configuration
IMG_RES = 1080
API_URL = "http://localhost:8000/api/v1/chat_media"  

# Function to encode and resize the image
def encode_and_resize(image):
    W, H = image.size
    image = image.resize((IMG_RES, int(IMG_RES * H / W)))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return encoded_image

# Function to send the request to the API
def get_actions(image, objective):
    encoded_image = encode_and_resize(image)
    
    # Preparing the multipart form-data payload
    files = {
        "files": ("image.png", BytesIO(base64.b64decode(encoded_image)), "image/png")
    }
    data = {
        "user_id": "text",
        "session_id": "text",
        "chat_data": objective,
    }
    
    response = requests.post(API_URL, files=files, data=data)
    
    if response.status_code == 200:
        try:
            json_response = response.json()
            return json_response
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return {}
    else:
        print(f"Error: Received status code {response.status_code}")
        return {}

if __name__ == "__main__":
    # Load and process the image
    image = Image.open("image.png")
    actions = get_actions(image, "upvote the pinterest post")
    print(actions)

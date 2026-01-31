
import requests
import os

url = "http://127.0.0.1:8000/detect"
# Create a dummy image file
with open("test_image.txt", "w") as f:
    f.write("dummy image content")

# We need a real image or at least a file. The backend expects an image extension.
with open("test.png", "wb") as f:
    f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

files = {'file': ('test.png', open('test.png', 'rb'), 'image/png')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

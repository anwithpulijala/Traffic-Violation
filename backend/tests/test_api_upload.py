import requests
import os

url = "http://127.0.0.1:8000/detect"
file_path = "test.png"

# Ensure we have a dummy image
if not os.path.exists(file_path):
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024)) # Dummy 1KB file

files = [
    ("files", ("test_api_upload.png", open(file_path, "rb"), "image/png"))
]

print("Sending request to /detect...")
try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")

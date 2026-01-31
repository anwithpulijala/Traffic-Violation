import cv2
import numpy as np

# Create a dummy video
height, width = 640, 480
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('dummy_video.mp4', fourcc, 20.0, (width, height))

for _ in range(30):
    frame = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
    out.write(frame)

out.release()
print("Dummy video created: dummy_video.mp4")

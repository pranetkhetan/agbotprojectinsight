import numpy as np
import cv2

ip = input('Enter IP Address: ')
port = input('Enter port: ')
address = "http://" + ip + ":" + port + "/"
video_capture = cv2.VideoCapture(address)  
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 25, 25])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = np.sum(mask > 0)
    total_pixels = image.shape[0] * image.shape[1]
    green_percentage = (green_pixels / total_pixels) * 100
    print(f"Percentage of green pixels is {green_percentage:.1f}%")
    cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

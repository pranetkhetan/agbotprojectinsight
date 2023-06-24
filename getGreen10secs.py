import numpy as np
import cv2
import time
import paramiko
import os

ip = input('Enter IP Address: ')
port = input('Enter port: ')
address = "http://" + ip + ":" + port + "/"
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username='pi', password='wedidnotstartthefire01')
scp = ssh.open_sftp()

video_capture = cv2.VideoCapture(address)
index = 0
while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 25, 25])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    binary_image = np.zeros_like(image)
    binary_image[mask > 0] = (255, 255, 255)
    
    # Create an in-memory file to hold the image data
    _, img_encoded = cv2.imencode('.jpg', binary_image)
    
    # Transfer the image data to Raspberry Pi using scp
    remote_path = "processed/" + str(index) + ".jpg"
    with scp.open(remote_path, 'wb') as remote_file:
        remote_file.write(img_encoded)
    print("Transferred image to Raspberry Pi:", remote_path)

    index = index + 1
    time.sleep(10)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

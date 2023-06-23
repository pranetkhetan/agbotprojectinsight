import numpy as np
import cv2

# Load YOLOv4
model = cv2.dnn_DetectionModel("yolov4.weights", "yolov4.cfg")
model.setInputSize(608, 608)  # Set input size (you can adjust this value)
model.setInputScale(1.0 / 255)  # Set input scale
model.setInputSwapRB(True)  # Set color ordering (OpenCV uses BGR by default)

# Enable GPU acceleration
model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Set classes for YOLO
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

ip = input('Enter IP Address: ')
port = input('Enter port: ')
address = "http://" + ip + ":" + port + "/"
video_capture = cv2.VideoCapture(address)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Perform object detection using YOLO
    class_ids, confidences, boxes = model.detect(frame, confThreshold=0.5)  # Adjust the confidence threshold if needed

    # Apply green pixel detection on the original frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_green = np.array([30, 25, 25])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = np.sum(mask > 0)
    total_pixels = image.shape[0] * image.shape[1]
    green_percentage = (green_pixels / total_pixels) * 100
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # Apply non-maximum suppression to remove overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.7, nms_threshold=0.5)

    # Draw bounding boxes, labels, and scores on the original frame
    for i in indices:
        box = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = (0, 255, 0)  # Green color for bounding boxes
        cv2.rectangle(frame, box, color, 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('YOLO Object Detection', frame)
    cv2.imshow('Masked Image', masked_image)
    print(f"Percentage of green pixels is {green_percentage:.1f}%")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

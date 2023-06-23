import numpy as np
import cv2

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Enable GPU acceleration
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Set classes for YOLO
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Get output layer names of YOLO network
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

ip = input('Enter IP Address: ')
port = input('Enter port: ')
address = "http://" + ip + ":" + port + "/"
video_capture = cv2.VideoCapture(address)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Resize frame for input to YOLO
    resized_frame = cv2.resize(frame, (416, 416))
    height, width, channels = resized_frame.shape

    # Perform object detection using YOLO
    blob = cv2.dnn.blobFromImage(resized_frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    # Iterate over detected objects
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Scale bounding box coordinates back to the original frame size
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Calculate top-left corner coordinates of bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Store class id, confidence, and box coordinates
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Apply non-maximum suppression to remove redundant overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Perform green pixel detection on the original frame
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 25, 25])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    green_pixels = np.sum(mask > 0)
    total_pixels = image.shape[0] * image.shape[1]
    green_percentage = (green_pixels / total_pixels) * 100
    masked_image = cv2.bitwise_and(image, image, mask=mask)

    # Draw bounding boxes, labels, and scores on the original frame
    for i in indices:
        i = indices[0]
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = (0, 255, 0)  # Green color for bounding boxes
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow('YOLO Object Detection', frame)
    cv2.imshow('Masked Image', masked_image)
    print(f"Percentage of green pixels is {green_percentage:.1f}%")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

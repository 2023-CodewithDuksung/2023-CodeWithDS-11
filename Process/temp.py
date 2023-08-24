from coordinates import machine, person
import os
from PIL import Image

print(machine)
print('-------------------------------------')
print(person)
frame_folder = "detected/frame"
file_list = os.listdir(frame_folder)
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

for file_name in file_list:
    _, file_extension = os.path.splitext(file_name)
    if file_extension.lower() in image_extensions:
        image_path = os.path.join(frame_folder, file_name)
        try:
            image = Image.open(image_path)
            image.show()  # 이미지 뷰어로 열기
            image.close()  # 이미지 뷰어가 닫힐 때까지 대기
        except Exception as e:
            print(f"Error opening {image_path}: {e}")

"""########################

detected_people = []  # 감지된 사람 정보를 저장할 리스트
min_duration = 3.0  # 최소 머무르는 시간 설정 (3초 이상)
last_detected_time = 0  # 마지막으로 인식된 시간을 저장할 변수

frame_num = 0  # 프레임 번호 초기화

MachineA = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_num += 1  # 프레임 번호 증가

    height, width = frame.shape[0], frame.shape[1]
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(net.getUnconnectedOutLayersNames())

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # 0은 person 클래스
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.1, 0.4)

    detected_people_in_frame = []  # 현재 프레임에서 감지된 사람 정보를 저장할 리스트

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), font, 1, color, 2)
            detected_people_in_frame.append((frame_num, x, y, w, h))  # 프레임 번호와 사람 위치 추가

    if detected_people_in_frame:
        current_time = time.time()
        if current_time - last_detected_time >= min_duration:
            detected_people.append(detected_people_in_frame)
            last_detected_time = current_time

    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 감지된 사람 정보 출력
for people in detected_people:
    for frame_num, x, y, w, h in people:
        if 200 < x < 400 and 400 < y < 500:
            MachineA += 1
            print("==================================================")
            print(f"Frame {frame_num} - Person detected at ({x}, {y}) for {min_duration:.2f} seconds - MachineA Num = {MachineA}")
            MachineA = 0
"""
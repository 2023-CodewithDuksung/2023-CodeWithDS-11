from detection import final_result
import requests

# frame 별로 운동 기구 좌표 뽑기
coordinates = final_result
print(type(coordinates))
machine = []
person = []
for i in range(len(coordinates)):
    machine_frame = []
    person_frame = []

    for j in range(len(coordinates[i]['machine']['predictions'])):
        x1 = coordinates[i]['machine']['predictions'][j]['x']
        y1 = coordinates[i]['machine']['predictions'][j]['y']
        x2 = x1 + coordinates[i]['machine']['predictions'][j]['width']
        y2 = y1 + coordinates[i]['machine']['predictions'][j]['height']
        class_name = coordinates[i]['machine']['predictions'][j]['class']

        machine_frame.append({'class': class_name, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

    machine.append(machine_frame)

    for l in range(len(coordinates[i]['detection'])):
        if coordinates[i]['detection'][l]['class_id'] == 0:  # person 객체만
            x1 = coordinates[i]['detection'][l]['coordinates'][0]
            y1 = coordinates[i]['detection'][l]['coordinates'][1]
            x2 = coordinates[i]['detection'][l]['coordinates'][2]
            y2 = coordinates[i]['detection'][l]['coordinates'][3]
            person_frame.append({'class_idx': 0, 'class_name': 'person', 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2})

    person.append(person_frame)


print(machine)
print('-------------------------------------')
print(person)

""" ####### 1번째
overlapping_pairs = []

for frame_idx in range(len(coordinates)):
    frame_overlaps = []

    for machine_box in machine[frame_idx]:
        machine_x1, machine_y1, machine_x2, machine_y2 = machine_box['x1'], machine_box['y1'], machine_box['x2'], machine_box[
            'y2']
        machine_area = machine_x2 * machine_y2
        frame_overlapping_person = []

        for person_box in person[frame_idx]:
            person_x1, person_y1, person_x2, person_y2 = person_box['x1'], person_box['y1'], person_box['x2'], \
            person_box['y2']
            person_area = (person_x2 - person_x1) * (person_y2 - person_y1)

            overlap_x1 = max(machine_x1, person_x1)
            overlap_y1 = max(machine_y1, person_y1)
            overlap_x2 = min(machine_x2, person_x2)
            overlap_y2 = min(machine_y2, person_y2)

            overlap_area = max(0, overlap_x2 - overlap_x1) * max(0, overlap_y2 - overlap_y1)
            overlap_ratio = overlap_area / min(machine_area, person_area)

            if overlap_ratio >= 0.5:  # Overlap threshold (50%)
                frame_overlapping_person.append(person_box)

        frame_overlaps.append({'machine': machine_box, 'overlapping_person': frame_overlapping_person})

    overlapping_pairs.append(frame_overlaps)

# Print overlapping pairs for each frame
for frame_idx, frame_pairs in enumerate(overlapping_pairs, start=1):
    print(f"Frame {frame_idx} - Overlapping Pairs:")
    for pair in frame_pairs:
        machine_box = pair['machine']
        overlapping_person = pair['overlapping_person']
        print(f"Machine: {machine_box}, Overlapping Person(s): {overlapping_person}")

"""


""" ####### 2번째
def calculate_overlap_area(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'], coords1['x2'], coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'], coords2['x2'], coords2['y2']

    x_overlap = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
    y_overlap = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))

    overlap_area = x_overlap * y_overlap
    return overlap_area


def check_overlap(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'],coords1['x2'],coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'],coords2['x2'],coords2['y2']

    area_coords1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area_coords2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    overlap_area = calculate_overlap_area(coords1, coords2)
    overlap_ratio = overlap_area / min(area_coords1, area_coords2)

    return overlap_ratio >= 0.5  # Overlap ratio is 50% or more


for m in machine:
    for p in person:
        for machine_coords in m:
            for person_coords in p:
                if check_overlap(machine_coords, person_coords):
                    print("Machine and person overlap:", machine_coords, person_coords)
"""

""" 3번쨰
def calculate_overlap_area(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'], coords1['x2'], coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'], coords2['x2'], coords2['y2']

    x_overlap = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
    y_overlap = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))

    overlap_area = x_overlap * y_overlap
    return overlap_area


def check_overlap(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'],coords1['x2'],coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'],coords2['x2'],coords2['y2']

    area_coords1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area_coords2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    overlap_area = calculate_overlap_area(coords1, coords2)
    overlap_ratio = overlap_area / min(area_coords1, area_coords2)

    return overlap_ratio >= 0.5  # Overlap ratio is 50% or more




for frame_idx, machine_coords in enumerate(machine):
    for person_idx, person_coords in enumerate(person[frame_idx]):
        for machine_idx, machine_box in enumerate(machine_coords):
            for person_box in person_coords:
                if check_overlap(machine_box, person_box):
                    print(f"Overlap detected in frame {frame_idx+1}: Machine {machine_idx+1} and Person {person_idx+1}")
"""

""""""
# 4번째
def calculate_overlap_area(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'], coords1['x2'], coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'], coords2['x2'], coords2['y2']

    x_overlap = max(0, min(x2_1, x2_2) - max(x1_1, x1_2))
    y_overlap = max(0, min(y2_1, y2_2) - max(y1_1, y1_2))

    overlap_area = x_overlap * y_overlap
    return overlap_area


def check_overlap(coords1, coords2):
    x1_1, y1_1, x2_1, y2_1 = coords1['x1'], coords1['y1'],coords1['x2'],coords1['y2']
    x1_2, y1_2, x2_2, y2_2 = coords2['x1'], coords2['y1'],coords2['x2'],coords2['y2']

    area_coords1 = (x2_1 - x1_1) * (y2_1 - y1_1)
    area_coords2 = (x2_2 - x1_2) * (y2_2 - y1_2)

    overlap_area = calculate_overlap_area(coords1, coords2)
    overlap_ratio = overlap_area / min(area_coords1, area_coords2)

    return overlap_ratio >= 0.5  # Overlap ratio is 50% or more


frame_num = 0
using_person = 0

# 클래스 이름과 숫자 매핑
class_mapping = {
    "leg extension": 1,
    "Lat Pull Down": 2,
    "chest fly machine": 3,
    "Seated Cable Rows": 4,
    "leg press": 5
}

for machine_frame in machine:
    using_person_list = [0, 0, 0, 0, 0]
    for machine_type in machine_frame:
        name = machine_type['class']
        machine_id = class_mapping[name]

        for p in person[frame_num]:
            if check_overlap(machine_type, p):
                using_person_list[machine_id - 1] += 1
    for i in range(5):
        print(f"frame:{frame_num} machine_id:{i + 1} people:{using_person_list[i]}\n")


    frame_num += 1




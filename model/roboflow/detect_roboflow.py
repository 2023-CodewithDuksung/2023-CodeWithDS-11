from roboflow import Roboflow
from PIL import Image

# 입력 이미지 정의
#frame_path = 'D:/Portfolio/Project/LaiON/YOLO/Process/materials/'
#frame_name = 'FitnessCenterShortPart.png'

# 출력 이미지
#save_path = 'D:\Portfolio\Project\LaiON\YOLO\Process\detected\machine'

def _create_model():
    rf = Roboflow(api_key="4mBmzqpaUvli0GAKDJum") # 고민정 workspace_private_api_key
    project = rf.workspace().project("gym-equipment-object-detection") # 사용하는 프로젝트명 : gym-equipment-object-detection (by others)
    # 데이터셋 클래스 13개
    return project.version(1).model
"""
def _resize_image(frame_name, frame_path, w=384, h=640):
    # 이미지 경로
    image_path = frame_path + frame_name
    new_width = w
    new_height = h

    # 이미지 열기 및 리사이즈
    image = Image.open(image_path)
    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
    save_path = "../../materials/resized/" + "resized_" + frame_name

    # 리사이즈된 이미지 저장
    resized_image.save(save_path)

    # 리사이즈된 이미지 경로와 크기 출력
    print("Resized Image Path:", save_path)
    print("New Image Size:", resized_image.size)
    return save_path
"""

# 모델 설정 및 추론
def inference(frame_name, frame_path='../../detected/frame/', w=384, h=640, confidence=17, overlap=70): # confidence : 신뢰도 값 이상인 것만 포함 # overlap : 감지된 객체들 간에 최소한 70%의 겹침이 있으면 하나의 객체로 합침
    model = _create_model()
    #resized_path = _resize_image(frame_name, frame_path, w, h)
    prediction = model.predict(frame_path + frame_name, confidence=confidence, overlap=overlap) # 로컬 이미지에 대한 추론
    # prediction = model.predict("YOUR_IMAGE.jpg", hosted=True)                                 # 호스팅된 이미지에 대해 파일 이름
    # prediction = model.predict("https://...", hosted=True)                                    # 이미지 URL에 대한 추론
    return prediction

"""
def get_coordinates(prediction):
    res = prediction.json()
    coordinates = {}
    for i in range(len(res['prediction'])) :
        coordinates['x']
"""







"""
### main
prediction = inference('FitnessCenterShortPart.png')
print(prediction.json()) # 추론 결과 JSON으로 변환
prediction.save('../../detected/machine/FitnessCenterShortPart.png') # 추론 결과 저장
prediction.plot() # 추론 결과 그래프로 시각화
"""

# 결과 print 예시
"""
{
	'predictions': 
		[
			{	
				'x': 558, 
				'y': 336, 
				'width': 713, 
				'height': 625, 
				'confidence': 0.26858317852020264, 
				'class': 'Chest Press machine', 
				'image_path': 
				'../../materials/FitnessCenterShortPart.png', 
				'prediction_type': 'ObjectDetectionModel'
			}, 
			{
				'x': 611, 
				'y': 336, 
				'width': 607, 
				'height': 625, 
				'confidence': 0.22181010246276855, 
				'class': 'leg extension', 
				'image_path': '../../materials/FitnessCenterShortPart.png', 
				'prediction_type': 'ObjectDetectionModel'
			}
		], 
	'image': 
		{
			'width': '1174', 
			'height': '658'
		}
}
"""
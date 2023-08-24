from model.yolov5 import detect
from model.roboflow import detect_roboflow
import os


# yolov5 설정
opt = detect.parse_opt()
opt.vid_stride = 128  # 예시: 128프레임마다 1프레임만 사용


video_path = str(detect.ROOT / '../../materials/') 
video_name = 'FitnessCenterShort.mp4'
result_path = str(detect.ROOT / '../../detected/')
result_name = 'yolo_FitnessCenterShort.mp4'

# yolov5 입력 영상 경로
opt.source = os.path.join(video_path, video_name)
#opt.source = 'materials/FitnessCenterShort.mp4'
# yolov5 출력 영상 저장 경로
opt.project='detected'
opt.name = 'person'



final_result = detect.main(opt)

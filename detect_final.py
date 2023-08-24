"""
model/yolov5/detect.py와 동일한 코드
"""
# YOLOv5 🚀 by Ultralytics, AGPL-3.0 license
"""
Run YOLOv5 detection inference on images, videos, directories, globs, YouTube, webcam, streams, etc.

Usage - sources:
    $ python detect.py --weights yolov5s.pt --source 0                               # webcam
                                                     img.jpg                         # image
                                                     vid.mp4                         # video
                                                     screen                          # screenshot
                                                     path/                           # directory
                                                     list.txt                        # list of images
                                                     list.streams                    # list of streams
                                                     'path/*.jpg'                    # glob
                                                     'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                     'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python detect.py --weights yolov5s.pt                 # PyTorch
                                 yolov5s.torchscript        # TorchScript
                                 yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                 yolov5s_openvino_model     # OpenVINO
                                 yolov5s.engine             # TensorRT
                                 yolov5s.mlmodel            # CoreML (macOS-only)
                                 yolov5s_saved_model        # TensorFlow SavedModel
                                 yolov5s.pb                 # TensorFlow GraphDef
                                 yolov5s.tflite             # TensorFlow Lite
                                 yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
                                 yolov5s_paddle_model       # PaddlePaddle
"""

import argparse
import os
import platform
import sys
from pathlib import Path
import time

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from ultralytics.utils.plotting import Annotator, colors, save_one_box

from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from utils.torch_utils import select_device, smart_inference_mode


#### 고민정 : 영상 시각화
import cv2
from PIL import Image
from model.roboflow import detect_roboflow

@smart_inference_mode()
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
        #### 고민정 : 객체 검출 시각화 결과 저장
        save_img=True,  # save inference images (default: True)
        save_dir=ROOT / 'runs/detect',  # save directory (default: 'runs/detect')

):
    source = str(source)
    save_img = not nosave and not source.endswith('.txt')  # save inference images
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Directories
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    bs = 1  # batch_size
    if webcam:
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot:
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs

    ##### 고민정 : 바운딩 박스 좌표 출력 및 반환 + 탐지된 객체 클래스 및 정수 매칭
    detection = []

    ##### 고민정 : 반환
    result = []

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:  # 프레임당

        #### 고민정 : 출력 및 반환
        LOGGER.info('프레임 인덱스 : ' + s)
        result_detection = {}

        #### 고민정 프레임 인덱스 및 총 프레임 출력
        frame_idx = int(s[(s.find('(') + 1):(s.find('/', (s.find('(') + 1)))])
        frame_total = int(s[(s.find('/', s.find('/') + 1) + 1):s.find(')')])


        # 프레임을 이미지 파일로 저장
        ret, frame = vid_cap.read()
        frame_filepath = 'detected/frame/'
        frame_filename = f"frame_{frame_idx:04d}.jpg"
        roboflow_path = frame_filepath + frame_filename
        cv2.imwrite(roboflow_path, frame)
        prediction = detect_roboflow.inference(frame_filename, frame_filepath)
        result_detection['machine'] = prediction.json()


        #### 고민정 : 반환
        result_detection['frame_idx'] = frame_idx
        result_detection['frame_total'] = frame_total




        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        #### 고민정 : 인퍼런스 시간(밀리초)
        LOGGER.info(f"Inference 단계에서의 소요 시간 : {dt[1].dt * 1E3:.1F}ms")
        """
        Inference?
        모델이 입력 이미지나 프레임을 처리하여 객체를 탐지하고 분류하는 단계.
        모델이 이미 학습되었고, 실제로 이미지나 비디오 프레임에 대한 예측을 수행하는 과정.
        Inference Time = 모델이 한 프레임을 처리하는데 걸리는 시간.
        """
        #### 고민정 : 출력
        new_s = ""
        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1

            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  ##### im.jpg # 현재 비디오 및 이미지의 경로
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string ##### 384x640 : 이미지 크기
            #### 고민정 : 출력
            new_s += '%gx%g ' % im.shape[2:]  # print string ##### 384x640 : 이미지 크기
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                #### 고민정 :반환
                result_detection['detection_object'] = [{} for _ in range(80)]
                result_detection['detection_num'] = 0

                # Print results
                for c in det[:, 5].unique():
                    #### 고민정 : 객체 개수 = 80
                    # print("클래스 개수" + str(len(names)))

                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  #### 클래스별 탐지된 객체 수

                    #### 고민정 : 반환
                    cl_info = {}
                    cl_info[names[int(c)]] = n
                    result_detection['detection_object'][int(c)][names[int(c)]] = n.item()  #### tensor(1.35).item() = 1.35
                    result_detection['detection_num'] += 1

                    #### 고민정 : 출력
                    new_s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  #### 클래스별 탐지된 객체 수
                #### 고민정 : 반환
                result_detection['detection'] = []

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                        with open(f'{txt_path}.txt', 'a') as f:
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # Add bbox to image
                        c = int(cls)  # integer class
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                        annotator.box_label(xyxy, label, color=colors(c, True))

                        ##### 고민정 : 바운딩 박스 좌표 출력 및 반환 + 탐지된 객체 클래스 및 정수 매칭
                        detection_info = {
                            "class_id": c,
                            "class_name": names[c],
                            "coordinates": [t.item() for t in xyxy],  #### xyxy : tensor -> 정수 변환
                            "confidence": conf.item()
                        }
                        detection.append(detection_info)
                        result_detection['detection'].append(detection_info)
                        LOGGER.info(
                            f"-Detected {detection_info['class_name']} ({detection_info['class_id']}) with confidence {detection_info['confidence']:.2f} : [{detection_info['coordinates'][0]:.2f}, {detection_info['coordinates'][1]:.2f}, {detection_info['coordinates'][2]:.2f}, {detection_info['coordinates'][3]:.2f}]")

                    if save_crop:
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

            # Stream results
            im0 = annotator.result()
            if view_img:
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image':
                    cv2.imwrite(save_path, im0)
                else:  # 'video' or 'stream'
                    if vid_path[i] != save_path:  # new video
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # release previous video writer
                        if vid_cap:  # video #### video 출력
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # stream
                            fps, w, h = 30, im0.shape[1], im0.shape[0]
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                    vid_writer[i].write(im0)

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}")


        #### 고민정 : 반환
        result.append(result_detection)

    # Print results : 마지막 줄
    t = tuple(x.t / seen * 1E3 for x in dt)  # speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img:
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update:
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

    return result


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'data/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='show results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
    parser.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
    parser.add_argument('--nosave', action='store_true', help='do not save images/videos')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--visualize', action='store_true', help='visualize features')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    parser.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    parser.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
    parser.add_argument('--vid-stride', type=int, default=1, help='video frame-rate stride')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(vars(opt))
    return opt


def main(opt):
    check_requirements(ROOT / 'requirements.txt', exclude=('tensorboard', 'thop'))
    detections = run(**vars(opt))


    print("########################################################################################")
    print(detections)
    return detections

    """
    for detection in detections:
        class_name = detection['class_name']
        class_id = detection['class_id']
        confidence = detection['confidence']
        coordinates = detection['coordinates']

        x1 = coordinates[0].item()
        y1 = coordinates[1].item()
        x2 = coordinates[2].item()
        y2 = coordinates[3].item()

        print(f"{class_name} ({class_id}) with confidence {confidence:.2f} : [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")

        print(f"Detected {class_name} ({class_id}) with confidence {confidence:.2f} : [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")
    """

"""
if __name__ == '__main__':
    opt = parse_opt()
    #### 고민정 : 프레임 수 조절
    opt.vid_stride = 16  # 예시: 16프레임마다 1프레임만 사용

    #### 고민정 : 입력 영상 경로
    opt.source = 'D:\Portfolio\Project\LaiON\YOLO\Process\materials\FitnessCenterShort.mp4'
    #### 고민정 : 출력 영상 저장 경로
    opt.project=ROOT / '../../detected' # ROOT = '프로젝트폴더/model/yolov5'
    opt.name = 'person'

    main(opt)
"""


"""
########################################################################################### 반환값 예시 :

	{
		'frame_idx': 1, 
		'frame_total': 411, 
		'object': [
				{'person': 1}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 				{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, 				{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'chair': 6}, {}, {}, 				{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {'refrigerator': 1}, {}, {}, {}, 				{}, {}, {}, {}
		], 
		'detection_num': 3, 
		'detection': [
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [351.0, 268.0, 547.0, 571.0], 
				'confidence': 0.29409998655319214
			}, 
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [1045.0, 184.0, 1143.0, 334.0], 
				'confidence': 0.31974121928215027}, 
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [844.0, 115.0, 958.0, 339.0], 
				'confidence': 0.47231048345565796}, 
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [944.0, 178.0, 1059.0, 305.0], 
				'confidence': 0.5053549408912659
			}, 
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [1115.0, 116.0, 1168.0, 155.0], 
				'confidence': 0.5087709426879883
			}, 
			{
				'class_id': 56, 
				'class_name': 'chair', 
				'coordinates': [1098.0, 154.0, 1167.0, 221.0], 
				'confidence': 0.5664835572242737}, 
			{
				'class_id': 72, 
				'class_name': 'refrigerator', 
				'coordinates': [1.0, 30.0, 209.0, 644.0], 
				'confidence': 0.6504184603691101
			}, 
			{
				'class_id': 0, 
				'class_name': 'person', 
				'coordinates': [370.0, 85.0, 723.0, 549.0], 
				'confidence': 0.8136065602302551
			}
		]
	}, 

"""
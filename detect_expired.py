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
from random import random

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
):
    source = str(source)  # 소스의 경로를 문자열로 변환
    save_img = not nosave and not source.endswith('.txt')  # .txt로 끝나지 않거나 nosave(결과물 저장하지 않음)가 아니면 저장
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS) # 확장자가 이미지 또는 비디오일 경우 true
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://')) # source가 url인 경우 true
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)# 웹캠 스트림인 경우, source가 숫자로만 구성되어 있거나 .streams로 끝나는 경우, 또는 URL이지만 이미지 또는 비디오 파일이 아닌 경우, true로 설정
    screenshot = source.lower().startswith('screen') # source 경로가 stream으로 시작하는 경우 true
    if is_url and is_file:
        source = check_file(source)  # 파일 다운로드

    # Directories : 결과 저장할 디렉토리 생성
    save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
    (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

    # Load model : 디바이스 선택, 모델 로딩, 이미지 사이즈 확인
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader : 데이터 로더 설정과 감지 결과 처리
    bs = 1  # batch_size
    if webcam: # 웹캠인지
        view_img = check_imshow(warn=True)
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        bs = len(dataset)
    elif screenshot: # 스크린샷인지
        dataset = LoadScreenshots(source, img_size=imgsz, stride=stride, auto=pt)
    else: # 그 외 이미지 및 비디오인지
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    vid_path, vid_writer = [None] * bs, [None] * bs


    detections = [] ############################################################### 고민정 : 객체 박스 좌표
    # Run inference # 추론 속도 높이기 위해 모델 초기화
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset: # 파일 경로, 이미지 데이터, 원본 이미지 데이터, 비디오 캡처 객체, 로깅 및 추력을 위한 문자열 : 데이터셋(이미지, 비디오, 웹캠, 스크린샷 등)에서 프레임 순환
        with dt[0]:
            im = torch.from_numpy(im).to(model.device) # 이미지 데이터를 PyTorch 텐서로 변환
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0 # 픽셀값 [0,1]로 정규화
            if len(im.shape) == 3: # 이미지 차원이 (H,W,C)인 경우 ex.JPEG 이미지, 3차원을 4차원으로 확장
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False # 시각화용 디렉토리 생성. visualize에 해당 디렉토리 지정
            pred = model(im, augment=augment, visualize=visualize) # model에 입력 이미지 넣어 추론 -> 감지 결과 pred에 저장. augment(데이터 증강 사용 여부)

        # NMS=비최대 억제 : NMS 사용하여 중복된 박스 제거 및 최종 예측 결과 얻기
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size >= 1
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            p = Path(p)  # to Path
            save_path = str(save_dir / p.name)  # im.jpg
            txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            imc = im0.copy() if save_crop else im0  # for save_crop
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det): # det(감지된 객체 정보 배열) 객체 좌표(xyxy), 신뢰도(confg), 클래스(cls) 추출
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # 정규화된 x,y,w,h
                        line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # (x1, y1, x2, y2) 좌표를 (x, y, w, h) 상대적 좌표로 변환 및 정규화
                        with open(f'{txt_path}.txt', 'a') as f: # 개체의 클래스, 좌표, 신뢰도를 텍스트 파일에 저장
                            f.write(('%g ' * len(line)).rstrip() % line + '\n')

                    if save_img or save_crop or view_img:  # 셋 중 하나라도 활성화되어있다면 이미지에 박스를 추가 또는 저장
                        c = int(cls)  # 클래스의 정수값
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}') # label에 클래스 이름, 신뢰도를 포함한 레이블을 생성
                        annotator.box_label(xyxy, label, color=colors(c, True)) # 이미지에 박스와 레이블 추가
                    if save_crop: # true? 감지된 개체 잘라서 저장!
                        save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                    detection_info = {
                        'class': names[int(cls)],
                        'class_idx': int(cls),
                        'confidence': conf,
                        'coordinates': xyxy
                    }
                    detections.append(detection_info)

                    color = colors(int(detection_info['class_idx']))

            # Stream results
            im0 = annotator.result() # 이미지 + 박스, 레이블 = im0
            if view_img: # 윈도우에 결과 이미지 표시 및 1밀리초 대기
                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'image': # 이미지라면
                    cv2.imwrite(save_path, im0) # 이미지 파일로 저장
                else:  # 비디오 또는 스트림이라면
                    if vid_path[i] != save_path:  # 이전 path와 현재 path가 다르면 새로운 비디오 파일 생성
                        vid_path[i] = save_path
                        if isinstance(vid_writer[i], cv2.VideoWriter):
                            vid_writer[i].release()  # 이전 VideoWriter 객체 닫고 해제
                        if vid_cap:  # 비디오라면
                            fps = vid_cap.get(cv2.CAP_PROP_FPS)
                            w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                            h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        else:  # 스트림이라면
                            fps, w, h = 30, im0.shape[1], im0.shape[0] # 비디오의 초당 프레임 수 설정
                        save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                        vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h)) # 비디오 프레임의 가로(w), 세로(h)
                    vid_writer[i].write(im0) # 각 프레임마다 im0 이미지를 비디오 파일에 쓰기

        # Print time (inference-only)
        LOGGER.info(f"{s}{'' if len(det) else '(no detections), '}{dt[1].dt * 1E3:.1f}ms")

    # Print results
    t = tuple(x.t / seen * 1E3 for x in dt)  # 작업 단계별 속도(Porfile 객체 속성) / 감지된 이미지의 총 수 * 1E3 for x in dt -> speeds per image
    LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
    if save_txt or save_img: # 저장된 텍스트 파일의 리스트 -> 개수와 경로 출력
        s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
        LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
    if update: # 모델을 업데이트 하기 위해 첫번째 가중치 파일에서 옵티마이저 정보를 제거한다. SourceChangeWarning 수정하기 위해서
        strip_optimizer(weights[0])  # update model (to fix SourceChangeWarning)

    return detections


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
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # 이미지 크기 옵션이 하나의 숫자로 지정된 경우, 그 값을 두 배로 확장
    print_args(vars(opt))
    return opt # 옵션에 대한 정보는 opt 객체에 저장되고 반환된다


# 시각화

def plot_one_box(box, img, color=None, label=None, line_thickness=None):
    """
    Plot one bounding box on image.
    box: list, tuple, or array representing [x1, y1, x2, y2] coordinates of the box
    img: numpy array representing the image
    color: color of the box (BGR format)
    label: label to display on the box
    line_thickness: thickness of the box's outline
    """
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]  # default random color if not provided
    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))  # top-left and bottom-right coordinates
    cv2.rectangle(img, c1, c2, color, thickness=tl)  # draw rectangle
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled rectangle
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)  # label


# main
def main(opt):
    check_requirements(ROOT / 'requirements.txt', exclude=('tensorboard', 'thop'))
    detections = run(**vars(opt))

    # Initialize vid_writer to None
    vid_writer = None

    for detection in detections:
        class_name = detection['class']
        confidence = detection['confidence']
        coordinates = detection['coordinates']

        class_idx = names.index(class_name)

        print(
            f"Detected {class_name} with confidence {confidence:.2f} at coordinates [{x1:.2f}, {y1:.2f}, {x2:.2f}, {y2:.2f}]")

        color = colors(class_idx)

        # 시각화 관련 코드를 추가합니다.
        im = cv2.imread(opt.source) if isinstance(opt.source, str) else dataset.get_frame(int(detection['frame']))
        label = f"{class_name} {confidence:.2f}"
        plot_one_box(coordinates, im, label=label, color=color)

        # 동영상 저장 관련 코드를 추가합니다.
        if not opt.nosave:
            save_path = str(Path(opt.source).stem) + '_output.mp4'
            if vid_writer is None:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                vid_writer = cv2.VideoWriter(save_path, fourcc, dataset.fps, (im.shape[1], im.shape[0]))
            vid_writer.write(im)

    if vid_writer is not None:
        vid_writer.release()

if __name__ == '__main__':
    opt = parse_opt()
    opt.nosave = False  # Set nosave to False
    main(opt)

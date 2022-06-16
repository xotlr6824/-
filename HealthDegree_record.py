import sys
import cv2
import math
import time
from cv2 import CAP_PROP_POS_FRAMES
from cv2 import detail_DpSeamFinder
import progressbar
from matplotlib import image
import io

#-- 파츠명 선언

BODY_PARTS_BODY_25 = {
                 "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                 "LShoulder": 5, "LElbow": 6, "LWrist": 7, "MidHip": 8,
                 "RHip": 9, "RKnee": 10, "RAnkle": 11, "LHip": 12,
                 "LKnee": 13, "LAnkle": 14, "REye": 15, "LEye": 16,
                 "REar": 17, "LEar": 18, "LBigToe": 19, "LSmallToe": 20,
                 "LHeel": 21, "RBigToe": 22, "RSmallToe": 23,"RHeel": 24, "Background": 25
                     }
POSE_PAIRS_BODY_25 = [["Nose", "Neck"], ["Nose", "REye"], ["Nose", "LEye"], ["Neck", "RShoulder"], ["Neck", "LShoulder"],
                      ["Neck", "MidHip"], ["MidHip", "RHip"], ["MidHip", "LHip"], ["RHip", "RKnee"], ["LHip", "LKnee"],
                      ["RShoulder", "RElbow"], ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"], 
                      ["RKnee", "RAnkle"], ["LKnee", "LAnkle"], ["REye", "REar"], ["LEye", "LEar"], ["LAnkle", "LHeel"], 
                      ["LBigToe", "LHeel"], ["LSmallToe", "LHeel"], ["RAnkle", "RHeel"], ["RBigToe", "RHeel"], ["RSmallToe", "RHeel"]]

BODY_PARTS_NUM = {0: "Nose", 1: "Neck", 2: "RShoulder", 3: "RElbow", 4: "RWrist",
                      5: "LShoulder", 6: "LElbow", 7: "LWrist", 8: "MidHip", 9: "RHip",
                      10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee", 14: "LAnkle",
                      15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe",
                      20: "LSmallToe", 21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel", 25: "Background"}

POSE_PAIRS_NUM = [[0, 1], [0, 15], [0, 16], [1, 2], [1, 5], [1, 8], [8, 9], [8, 12], [9, 10], [12, 13], [2, 3],
                      [3, 4], [5, 6], [6, 7], [10, 11], [13, 14], [15, 17], [16, 18], [14, 21], [19, 21], [20, 21],
                      [11, 24], [22, 24], [23, 24]]


def VideoWrite():
    try:
        print("카메라 구동")
        cap = cv2.VideoCapture(0)
    except:
        print("카메라 구동실패")
        return

    # 폭, 높이 값을 카메라속성에 맞춤
    # cap.set(probID, 속성값) 은 출력될 값들을 지정해주는 것이고
    # cap.get(probID) 는 해당 속성에 대한 값을 받아오는 것임.
    # 아래의 폭과 높이는 웹캠의 속성을 그대로 가져와 사용하는것.
    width = int(cap.get(3))
    height = int(cap.get(4))

    # 코덱정보를 나타냄 아래의 두줄과 같이 사용할 수 있음.
    # 둘중 어느것을 쓰든 상관없음.
    # 여러가지의 코덱종류가 있지만 윈도우라면 DIVX 를 사용
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    # fourcc = cv2.VideoWriter_fourcc('D','I','V','X')

    # 비디오 저장을 위한 객체를 생성해줌.
    out = cv2.VideoWriter('RecordVideo.mp4',fourcc,20.0,(width, height))
    

    while(True):
        ret, frame = cap.read()

        if not ret:
            print("비디오 읽기 오류")
            break
        cap.set(CAP_PROP_POS_FRAMES,50)
        # 비디오 프레임이 정확하게 촬영되었으면 화면에 출력하여줌
        cv2.imshow('video',frame)
        # 비디오 프레임이 제대로 출력되면 해당파일에 프레임을 저장
        out.write(frame)

        # ESC키값을 입력받으면 녹화종료 메세지와 함께 녹화종료
        k= cv2.waitKey(1)
        if(k == 27):
            print('녹화 종료')
            break

    # 비디와 관련 장치들을 다 닫아줌.
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def calculate_elbow_degree(point_1, point_2, frame):
    if (points[6] is not None) and (points[7] is not None):
    # 역탄젠트 구하기 / 손목,팔꿈치 각도
        dx = point_1[0] - point_2[0]
        dy = point_1[1] - point_2[1]
        rad = math.atan2(abs(dy), abs(dx))

    # radian 을 degree 로 변환
        deg = rad * 180 / math.pi

    # degree 가 70'보다 작으면 팔이 덜 펴졌다고 판단
        if deg < 70:
            string = "팔Bend Down"
            cv2.line(frame, points[6], points[7], (0, 0, 255), 6)
            cv2.putText(frame, string, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255))
            print(f"[degree] {deg} ({string})")
            print("팔을 더 올리세요")
        else:
            string = "팔Stand"
            cv2.line(frame, points[6], points[7], (0, 255, 0), 6)
            cv2.putText(frame, string, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255))
            print(f"[degree] {deg} ({string})")



VideoWrite()

threshold = 0.1

#-- 모델 파일 불러오기
protoFile = "prototxt 파일 경로" 
weightsFile = "caffemodel 파일 경로" 

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

cap = cv2.VideoCapture('/Users/siksik/pythontest/RecordVideo.mp4')
width = int(cap.get(3))
height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
n_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
widgets = ["--[INFO]-- Analyzing Video: ", progressbar.Percentage(), " ",
           progressbar.Bar(), " ", progressbar.ETA()]
pbar = progressbar.ProgressBar(maxval = n_frames,
                               widgets=widgets).start()
p=0
inputHeight = 640
inputWidth = 480
inputScale = 1.0/255

prev_time = 0
fps = 5
    
# 비디오 저장을 위한 객체를 생성해줌.
output = cv2.VideoWriter('ResultVideo.mp4',fourcc,20.0,(width, height))

while True:
    hasFrame, frame = cap.read()
    current_time = time.time() - prev_time

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    inp = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
    
    net.setInput(inp)
    out = net.forward()

    points = []
    for i in range(len(BODY_PARTS_BODY_25)):
        heatMap = out[0, i, :, :]

        _, conf, _, point = cv2.minMaxLoc(heatMap)
        x = int((frameWidth * point[0]) / out.shape[3])
        y = int((frameHeight * point[1]) / out.shape[2])


        if conf > threshold:
            cv2.circle(frame, (x, y), 3, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
            cv2.putText(frame, "{}".format(i), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1, lineType=cv2.LINE_AA)
            points.append((x, y))
        else:
            points.append(None)

    for pair in POSE_PAIRS_NUM:
        partFrom = pair[0] 
        partTo = pair[1] 
        if points[partFrom] and points[partTo]:
            
            # 왼쪽 팔꿈치, 손목
            if partFrom == 6 and partTo == 7:
                calculate_elbow_degree(points[6],points[7],frame)
            # 오른쪽 팔꿈치, 손목
            #elif partFrom == 4 and partTo == 5:
            #    calculate_elbow_degree(points[4],points[5],frame)
            else:  # 초록색 선
                cv2.line(frame, points[partFrom], points[partTo], (0, 255, 0), 3)
    
    p += 1
    pbar.update(p)
    
    #프레임 조절, 프레임 팅김 현상 줄이기
    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency() / 1000
    cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0)) #-- 프레임 출력
    if (hasFrame is True) and (current_time > 1./fps) :
        prev_time = time.time()
        cv2.imshow('video',frame)
        output.write(frame)

        if cv2.waitKey(1) > 0:
            break


print('save complete')
output.release()
pbar.finish()
cap.release()
cv2.destroyAllWindows()

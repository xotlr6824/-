import cv2
import math
import time


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

threshold = 0.1

#-- 모델 파일 불러오기
protoFile = "prototxt 파일 경로 " 
weightsFile = "caffemodel 파일 경로" 

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

#-- 캠 사용
cap = cv2.VideoCapture(0)

inputHeight = 368
inputWidth = 368
inputScale = 1.0/255

prev_time = 0
fps = 5

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
        
    #프레임 조절, 프레임 팅김 현상 줄이기
    t, _ = net.getPerfProfile()
    freq = cv2.getTickFrequency() / 1000
    cv2.putText(frame, '%.2fms' % (t / freq), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0)) #-- 프레임 출력
    if (hasFrame is True) and (current_time > 1./fps) :
        prev_time = time.time()
        cv2.imshow('video',frame)

        if cv2.waitKey(1) > 0:
            break

cap.release()
cv2.destroyAllWindows()

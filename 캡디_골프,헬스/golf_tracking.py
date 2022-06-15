from ast import Import
import cv2 as cv
import numpy as np
import cv2
import tensorflow as tf

# 모델 위치
model_filename ='모델 경로'

# 케라스 모델 가져오기
model = tf.keras.models.load_model(model_filename)

# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 이미지 처리하기
def preprocessing(frame):
    #frame = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    #print(frame_reshaped)
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

list_ball_location = []
history_ball_locations = []
isDraw = True

def draw_ball_location(img_color, locations):
    for i in range(len(locations)-1):

        if locations[0] is None or locations[1] is None:
            continue

        cv.line(img_color, tuple(locations[i]), tuple(locations[i+1]), (0, 255, 255), 3)

    return img_color

##########경로 색추적

def BallTracking(cap,isDraw):
    while True:
        ret,img_color = cap.read()
        img_color = cv.flip(img_color, 1)


        img_hsv = cv.cvtColor(img_color, cv.COLOR_BGR2HSV)

    
        #파랑색 범위
        lower_blue = np.array([100,100,120])          
        upper_blue = np.array([150,255,255])
        img_mask = cv.inRange(img_hsv, lower_blue, upper_blue)
    
        kernel = cv.getStructuringElement( cv.MORPH_RECT, ( 5, 5 ) )
        img_mask = cv.morphologyEx(img_mask, cv.MORPH_DILATE, kernel, iterations = 3)

        nlabels, labels, stats, centroids = cv.connectedComponentsWithStats(img_mask)

        max = -1
        max_index = -1 

        for i in range(nlabels):
 
            if i < 1:
                continue

            area = stats[i, cv.CC_STAT_AREA]

            if area > max:
                max = area
                max_index = i


        if max_index != -1:


            center_x = int(centroids[max_index, 0])
            center_y = int(centroids[max_index, 1]) 
            left = stats[max_index, cv.CC_STAT_LEFT]
            top = stats[max_index, cv.CC_STAT_TOP]
            width = stats[max_index, cv.CC_STAT_WIDTH]
            height = stats[max_index, cv.CC_STAT_HEIGHT]


            cv.rectangle(img_color, (left, top), (left + width, top + height), (0, 0, 255), 5)
            cv.circle(img_color, (center_x, center_y), 10, (0, 255, 0), -1)

            if isDraw:
                list_ball_location.append((center_x, center_y))
        
            else:
                history_ball_locations.append(list_ball_location.copy())
                list_ball_location.clear()


        img_color = draw_ball_location(img_color, list_ball_location)

        for ball_locations in history_ball_locations:
            img_color = draw_ball_location(img_color, ball_locations)

        preprocessed = preprocessing(img_color)
        prediction = predict(preprocessed)

        #스윙이 끝났다고 판단되면 추적경로 그림 지우기
        if (prediction[0,1] >0.9): 
            list_ball_location.clear()
            history_ball_locations.clear()
            cv.destroyAllWindows()
            break
        else:
            cv.imshow('Blue', img_mask)
            cv.imshow('Result', img_color)

        key = cv.waitKey(1)
        if key == 27: # esc
            break
        elif key == 32: # space bar키 누르면 경로 지우기
            list_ball_location.clear()
            history_ball_locations.clear()
        elif key == ord('v'):
            isDraw = not isDraw
#현재상태
status = 'ready'
count = 0

while True:
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    if cv2.waitKey(100) > 0: 
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

    if (prediction[0,2] >= 0.8 ):
        BallTracking(capture,isDraw)
        status = 'ready'

    elif (prediction[0,1] >= 0.8  ):
        #ready 상태에서 swing하면 카운트 +1
        if(status == 'ready'):
            count+=1
        
        status = 'swing'

    cv2.imshow("GOLF_SWING", frame)


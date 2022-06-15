# -
opencv / openpose / teachable machine

골프의 스윙 경로를 추적하여 그림으로 나타내 확인 할 수 있는 방법

teachable machine으로 골프 스윙 경로를 시작할 시점을 판단할 모델을 만들었다.
pose model은 json파일만 지원을 하여 image model로 생성하여 아쉬운 점이 있다.
0:swing
1:swing finish // 스윙경로 지울 시점
2:swing start // 스윙경로 생성 시점

https://user-images.githubusercontent.com/48917101/173853618-1ae59bf1-ab60-422a-9fbf-6cecd48d9dc8.mp4


model 생성 후 swing start라 예측되면 파랑색을 추적하여 경로를 그리게 된다.
스윙 후 finish라 판단되면 경로를 지우고 돌아간다.

결과

https://user-images.githubusercontent.com/48917101/173851027-ea5f25ea-b85c-4535-979a-d29c8ffc988b.mp4


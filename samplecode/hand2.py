import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

video_source = "/dev/video0"
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
# For webcam input:
cap = cv2.VideoCapture(gstreamer_pipeline(display_width=640, display_height=360), cv2.CAP_GSTREAMER)

print("Camera start")

with mp_hands.Hands() as hands:
    while True:
        _, image = cap.read()
        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        image = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            # 左右の手が見えている場合、cnt==2
            cnt = len(results.multi_hand_landmarks)
    #　　　 ①
            for idx in range(cnt) :
                hand_landmarks = results.multi_hand_landmarks[idx]
    #　　　　　 ②
    #　　　　　 ③
    #　　　　　 ④
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS)
    #　　　 ⑤
        cv2.imshow('MediaPipe Hands', image)
        # cv2.flip(image, 1) しません。
        k = cv2.waitKey(5)
        if k == ord('q') or k == 27:# q または、ESC で終了
            break
cap.release()
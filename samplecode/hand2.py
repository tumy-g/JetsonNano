import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
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
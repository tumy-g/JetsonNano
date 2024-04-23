import time
import sys
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

# 静止画像の場合：
# with mp_hands.Hands(
#     static_image_mode=True,
#     max_num_hands=2,
#     min_detection_confidence=0.5) as hands:
#   for idx, file in enumerate(file_list):
#     # 画像を読み取り、利き手が正しく出力されるようにy軸を中心に反転
#     image = cv2.flip(cv2.imread(file), 1)
#     # 処理する前にBGR画像をRGBに変換
#     results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#     # 利き手を出力し、画像に手のランドマークを描画
#     print('Handedness:', results.multi_handedness)
#     if not results.multi_hand_landmarks:
#       continue
#     image_height, image_width, _ = image.shape
#     annotated_image = image.copy()
#     for hand_landmarks in results.multi_hand_landmarks:
#       print('hand_landmarks:', hand_landmarks)
#       print(
#           f'Index finger tip coordinates: (',
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
#           f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
#       )
#       mp_drawing.draw_landmarks(
#           annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
#     cv2.imwrite(
#         '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))

# Webカメラ入力の場合：
cap = cv2.VideoCapture(gstreamer_pipeline(display_width=640, display_height=360), cv2.CAP_GSTREAMER)
print("start camera")
time.sleep(2)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    ret, image = cap.read()
    if not ret:
      print("Ignoring empty camera frame.")
      # ビデオをロードする場合は、「continue」ではなく「break」を使用してください
      continue

    # 後で自分撮りビューを表示するために画像を水平方向に反転し、BGR画像をRGBに変換
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # パフォーマンスを向上させるために、オプションで、参照渡しのためにイメージを書き込み不可としてマーク
    image.flags.writeable = False
    results = hands.process(image)

    # 画像に手のアノテーションを描画
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
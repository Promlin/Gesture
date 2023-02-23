import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) # Выбор камеры для использования

mpHands = mp.solutions.hands
hands = mpHands.Hands() # Settings to start using module with base settings
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read() # we get frame of picture
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Converting image to RGB
    results = hands.process(imgRGB) # to find hands
    # print(results.multi_hand_landmarks) # printing if there are no hands or its position

    # drawing position points for each hand
    # https://mediapipe.dev/images/mobile/hand_landmarks.png
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms)



    cv2.imshow("Image", img) # rum a webcam
    cv2.waitKey(1)
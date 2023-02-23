import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)  # Choosing the cam to use

mpHands = mp.solutions.hands
hands = mpHands.Hands()  # Settings to start using module with base settings
mpDraw = mp.solutions.drawing_utils

pTime = 0  # previous time
cTime = 0  # current time

while True:
    success, img = cap.read()  # we get frame of picture
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converting image to RGB
    results = hands.process(imgRGB)  # to find hands
    # print(results.multi_hand_landmarks) # printing if there are no hands or its position

    # drawing the lines of hand
    # https://mediapipe.dev/images/mobile/hand_landmarks.png
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                # we need to convert float position to pixel position in the img
                h, w, c = img.shape # high and weight of frame
                cx, cy = int(lm.x*w), int(lm.y*h) # pixel of each dot of the hand
                print(id, cx, cy)
                cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED) #drawing a circle around a point

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    # setting fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # Addinf fps label to the picture
    cv2.putText(img,"fps: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img) # rum a webcam
    cv2.waitKey(1)
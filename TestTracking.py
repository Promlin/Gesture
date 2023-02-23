import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

pTime = 0  # previous time
cTime = 0  # current time

cap = cv2.VideoCapture(0)  # Choosing the cam to use
detector = htm.handDetector()

while True:
    success, img = cap.read()  # we get frame of picture
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])

    # setting fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Addinf fps label to the picture
    cv2.putText(img, "fps: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    cv2.imshow("Image", img)  # rum a webcam
    cv2.waitKey(1)
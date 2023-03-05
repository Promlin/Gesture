import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

# Importing images
folderPath = "Header"
myList = os.listdir(folderPath)  # Supposed to change images
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.85)

while True:
    # Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flipping the image

    # Find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # print(lmList)

        # tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        # Checking which fingers are up

        fingers = detector.fingersUp()
        # print(fingers)

        # If selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 30), (255, 0, 0), cv2.FILLED)
            print("Selection mode")
            # Checking the color
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                if 550 < x1 < 750:
                    header = overlayList[1]
                if 800 < x1 < 950:
                    header = overlayList[2]
                if 1050 < x1 < 1200:
                    header = overlayList[3]

        # If drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
            print("Drawing mode")


    # SEtting the header image
    img[0:125, 0:1280] = header
    cv2.imshow("Image", img)
    cv2.waitKey(1)




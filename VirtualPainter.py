import cv2
import numpy as np
import os
import HandTrackingModule as htm

############
brushThickness = 15
eraserThicknesss = 100
############

# Importing images
folderPath = "Header"
myList = os.listdir(folderPath)  # Supposed to change images
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
# print(len(overlayList))
header = overlayList[0]
drawColor = (255, 0, 0)

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.85)

xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    # Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flipping the image

    # Find hand landmarks
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img, draw=False)

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
            xp, yp = 0, 0
            print("Selection mode")
            # Checking the color
            if y1 < 125:
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (0, 0, 255)
                if 500 < x1 < 650:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)
                if 700 < x1 < 850:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)
                if 1000 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)

            cv2.rectangle(img, (x1, y1 - 30), (x2, y2 + 30), drawColor, cv2.FILLED)

        # If drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drawing mode")

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThicknesss)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThicknesss)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    # Drawing in the canvas
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)  # getting gray image
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)  # inverting image
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)  # adding inverse image and main image (showing black image)
    img = cv2.bitwise_or(img, imgCanvas)  #


    # SEtting the header image
    img[0:125, 0:1280] = header
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)

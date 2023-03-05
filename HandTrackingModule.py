import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        # Settings to start using module with base settings
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

        self.tipIds = [4, 8, 12, 16, 20]  # indexes for different fingers

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converting image to RGB
        self.results = self.hands.process(imgRGB)  # to find hands
        # print(results.multi_hand_landmarks) # printing if there are no hands or its position

        # drawing the lines of hand
        # https://mediapipe.dev/images/mobile/hand_landmarks.png
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)


        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # we need to convert float position to pixel position in the img
                h, w, c = img.shape # high and weight of frame
                cx, cy = int(lm.x*w), int(lm.y*h) # pixel of each dot of the hand
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (0, 0, 255), cv2.FILLED)  # drawing a circle around a point

        return self.lmList

    def fingersUp(self):
        fingers = []

        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # For fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    pTime = 0  # previous time

    cap = cv2.VideoCapture(0)  # Choosing the cam to use
    detector = handDetector()

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

        # Adding fps label to the picture
        cv2.putText(img, "fps: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Image", img)  # rum a webcam
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

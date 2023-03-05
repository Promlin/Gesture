import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################
wCam, hCam = 640, 480
############################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

# region ToChange
# Место подключение библиотеки для управления звуком на пк,
# в случае с дроном здесь должно быть подключение управления скоростью (?) дрона
# https://github.com/AndreMiras/pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange()) # -65.25 - 0.0 (min - max)
volRange = volume.GetVolumeRange() # Получение диапазона максимального и минимального значений
minVol = volRange[0]  # Определение минимума
maxVol = volRange[1]  # Определение максимума
vol = 0
volBar = 400
volPer = 0
# endregion

while True:
    success, img = cap.read()

    # Finding hand
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)  #Getting list of hand positions
    if len(lmList) != 0:

        # Filter based on size

        # Find distance between iindex and Thum

        # Convert volume
        # Reduce resolution to make it smoother
        #Check fingers up


        # print(lmList[4], lmList[8]) # Position of the special point

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # finding the center between fingers

        cv2.circle(img, (x1, y1), 12, (255, 0, 255), cv2.FILLED) # drawing the circle around the point
        cv2.circle(img, (x2, y2), 12, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 12, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3) # drawing the line between fingers

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # region ToChange2
        # Hand range min = 50 - max = 300
        # Volume ranhge - 65 - 0
        # Надо преобразовать так чтобы минимум звука стал минимум жеста и так же с макс
        # По большому счету здесь просто надо подставить минимальную и максимальную скорость на место 50 и 300
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        # endregion

        # when the distance between the fingers is less than 50 then the center point becomes green
        if length < 50:
            cv2.circle(img, (cx, cy), 12, (0, 255, 0), cv2.FILLED)

    # Bar to show changing of value
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    # Addinf fps label to the picture
    cv2.putText(img, "fps: " + str(int(fps)), (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

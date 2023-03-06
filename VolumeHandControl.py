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

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

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
volRange = volume.GetVolumeRange()  # Получение диапазона максимального и минимального значений
minVol = volRange[0]  # Определение минимума
maxVol = volRange[1]  # Определение максимума
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

# endregion

while True:
    success, img = cap.read()

    # Finding hand
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=True)  # Getting list of hand positions
    if len(lmList) != 0:

        # Filter based on size
        area = (bbox[2] - bbox[0]) * (bbox[2] - bbox[1]) // 100
        print(area)
        if 250 < area < 1000:
            print("yes")
            # Find distance between index and Thum
            length, img, lineInfo = detector.findDistance(4, 8, img)
            # print(length)

            # Convert volume
            # region ToChange2
            # Hand range min = 50 - max = 250
            # Volume ranhge - 65 - 0
            # Надо преобразовать так чтобы минимум звука стал минимум жеста и так же с макс
            # По большому счету здесь просто надо подставить минимальную и максимальную скорость на место 50 и 250
            volBar = np.interp(length, [50, 250], [400, 150])
            volPer = np.interp(length, [50, 250], [0, 100])
            # endregion

            # Reduce resolution to make it smoother
            smoothness = 5
            volPer = smoothness * round(volPer / smoothness)

            # Check fingers up
            fingers = detector.fingersUp()

            # if pinky is down set volume
            if not fingers[4]:
                # region ToChange
                # Заменить установку громкости на установление значения скорости
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)  # Afford to send percentage volume
                # endregion

                # Change color after setting value
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 12, (0, 255, 0), cv2.FILLED)
                colorVol = (0, 255, 0)
            else:
                colorVol = (255, 0, 0)

    # Drawings
    # Bar to show changing of value
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
    cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
    cv2.putText(img, "Vol Set: " + str(cVol), (400, 40), cv2.FONT_HERSHEY_PLAIN, 2, colorVol, 3)

    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Addinf fps label to the picture
    cv2.putText(img, "fps: " + str(int(fps)), (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)

# Gesture
Educational project for the university, consisting of hand detection, gesture detection and gesture control 

Using "Murtaza's Workshop" YouTube videos and MediaPipe

https://www.youtube.com/@murtazasworkshop

https://google.github.io/mediapipe/solutions/hands

# The project is currently doing the following:
1. Detection of hands and key points

The detection of hands and key points is performed in the HandTracking.software file, based on the MediaPipe library. With the help of dots - markers, a check is also performed on which fingers are raised at a time and which are lowered

![image](https://user-images.githubusercontent.com/48473061/223932338-bf149615-1f60-4dd6-bc8b-1c1f22cad63c.png)

[Screenshot with drawn markers]

2. Сounting the number of fingers raised

The FingerSounder.py file counts the fingers that the user shows at the camera and displays the image with the corresponding number of fingers and the number of fingers raised

[screenshot of the demo window]

3. Drawing on the screen in augmented reality mode

The VirtualPainter.py file implements the connection of the user interface for color selection and drawing using gestures in augmented reality mode.
The program includes two modes of operation: color selection mode and drawing mode. To select a color, raise your index and middle fingers and point them at the brush with the desired color. To draw, you only need to lift your index finger, and moving it across the area will leave a colored line behind or erase it.

[screenshot of the demo window]

4. Adjust PC Volume with Gestures

The VolumeHandControl.py file implements computer volume control by bringing the thumb and forefinger closer and further away. Setting the value is done by lowering the little finger.

[screenshot of the demo window]

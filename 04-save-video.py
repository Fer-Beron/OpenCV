import cv2
import mediapipe as mp
import time
from copy import deepcopy


cap = cv2.VideoCapture(0)
mpManos = mp.solutions.hands
manos = mpManos.Hands()
mpDraw = mp.solutions.drawing_utils

# SALIDA (Graba video y obtengo el alto y ancho)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('videograbado.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width,frame_height))

itera = True
temporizando = False
numeronombre = 0

xiniciorect = (frame_width-200)
xfinrect = frame_width

# Se ejecuta el bucle hasta que se presiona la tecla ESCAPE (27)
while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    original = deepcopy(image)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = manos.process(imageRGB)
    itera = not itera

    # Comprobando si se detecta una mano
    afuera = True
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if (xiniciorect < cx < xfinrect) and (0 < cy < 200):
                    if itera:
                        cv2.rectangle(image, (xiniciorect, 0), (xfinrect, 200), (0, 255, 0), -1)
                    afuera = False

            mpDraw.draw_landmarks(image, handLms, mpManos.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=(57, 110, 151),
                                  thickness=2, circle_radius=2),
                                  mpDraw.DrawingSpec(color=(82,155,212), thickness=2, circle_radius=2))
        if afuera:
            cv2.rectangle(image, (xiniciorect, 0), (xfinrect, 200), (0, 0, 255), 2)
    cv2.rectangle(original, (xiniciorect, 0), (xfinrect, 200), (90, 90, 81), 2)
    cv2.imshow("Analisis", image)
    cv2.imshow("Original", original)
    tecla = cv2.waitKey(1)

    if tecla == 27:
        break
    elif tecla == 32:
        iniciotemp = time.time()
        out.write(original)
        temporizando = True
    if temporizando and (time.time()-iniciotemp) <= 5:
        out.write(original)
    elif temporizando and (time.time()-iniciotemp) > 5:
        temporizando = False

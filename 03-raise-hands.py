import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)
mpManos = mp.solutions.hands
manos = mpManos.Hands()
mpDraw = mp.solutions.drawing_utils

# Se ejecuta el bucle hasta que se presiona la tecla ESCAPE (27)
while True:
    success, image = cap.read()
    image = cv2.resize(image, (800, 700))
    image = cv2.flip(image,1)
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = manos.process(imageRGB)

    # Comprobando si se detecta una mano
    afuera = True
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if (600 < cx < 800) and (0 < cy < 200):
                    cv2.rectangle(image, (600, 0), (800, 200), (0, 255, 0), 2)
                    afuera = False

            mpDraw.draw_landmarks(image, handLms, mpManos.HAND_CONNECTIONS, mpDraw.DrawingSpec(color=(57, 110, 151),
                                  thickness=2, circle_radius=2), mpDraw.DrawingSpec(color=(82, 155, 212), thickness=2,
                                                                                    circle_radius=2))
        if afuera:
            cv2.rectangle(image, (600, 0), (800, 200), (0, 0, 255), 2)
    cv2.imshow("Output", image)

    if cv2.waitKey(1) == 27:
        break

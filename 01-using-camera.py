import cv2

cap = cv2.VideoCapture(0)

# Se ejecuta el bucle hasta que se presiona la tecla ESCAPE (27)
while True:
    ret, frame = cap.read()

    cv2.imshow('Camara Notebook', frame)

    if cv2.waitKey(1) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()

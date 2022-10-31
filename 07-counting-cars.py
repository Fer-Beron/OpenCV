import cv2
import numpy as np
import sqlite3
from datetime import datetime
from time import sleep

# Inicialización de variables
min_width = 80
min_height = 80
cars = 0
offset = 15
line_position = 500
delay = 30
detected_cars = []
conn = None

# Creación del modelo de datos. Se recrea la DB cada vez que se corre el programa.
conn = sqlite3.connect("cars.db")
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS car_detection""")
cur.execute("""CREATE TABLE car_detection(car_number INTEGER, detected_date TEXT, capture BLOB )""")
conn.commit()

# Inserción en la DB de cada auto detectado.
sql = "INSERT INTO car_detection (car_number, detected_date, capture) VALUES (?, ?, ?)"


def center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


cap = cv2.VideoCapture('cars.mp4')
substraction = cv2.bgsegm.createBackgroundSubtractorMOG()

# Se ejecuta el bucle hasta que se presiona la tecla ESCAPE (27)
while True:
    ret, frame1 = cap.read()
    time = float(1 / delay)
    sleep(time)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = substraction.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilated = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilated = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    outline, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame1, (25, line_position), (1250, line_position), (255, 255, 0), 3)

    for (i, c) in enumerate(outline):
        (x, y, w, h) = cv2.boundingRect(c)
        validate_outline = (w >= min_width) and (h >= min_height)
        if not validate_outline:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 255), 2)
        centro = center(x, y, w, h)
        detected_cars.append(centro)
        cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

        for (x, y) in detected_cars:
            if (line_position + offset) > y > (line_position - offset):
                cars += 1
                cv2.line(frame1, (25, line_position), (1250, line_position), (0, 127, 255), 3)
                detected_cars.remove((x, y))
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                capture = sqlite3.Binary(frame1)
                cur.execute(sql, [cars, timestamp, capture])
                print("Detected car : " + str(cars))

    cv2.putText(frame1, "Detected : " + str(cars), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 20), 5)
    cv2.imshow("Counting Cars with OpenCV. Press ESC to exit", frame1)

    if cv2.waitKey(1) == 27:
        break

conn.commit()
cv2.destroyAllWindows()
cap.release()

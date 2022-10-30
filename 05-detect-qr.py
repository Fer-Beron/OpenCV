import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

# Se ejecuta el bucle hasta que se presiona la tecla ESCAPE (27)
while True:
    ret, frame = cap.read()
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)
    frame = aruco.drawDetectedMarkers(frame, corners)
    # Showing arucos
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()

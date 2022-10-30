import cv2

img_path = 'monumento.jpg'

img_raw = cv2.imread(img_path)

roi = cv2.selectROI (img_raw)

print(roi)

roi_cropped = img_raw[int(roi[1]):int(roi[1]+roi[3]),int(roi[0]):int(roi[0]+roi[2])]

cv2.imshow('ROI', roi_cropped)

cv2.imwrite('monumento_cutted.jpeg', roi_cropped)

cv2.waitkey(0)

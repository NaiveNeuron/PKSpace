import cv2
import datetime
import os

OUTPUT_DIR = '/home/pi/data'
DIR = '%Y-%m-%d'
FILE = '%H:%M:%S.png'

cap = cv2.VideoCapture(0)

#  warmup camera
for i in range(15):
    _, _ = cap.read()

ret, frame = cap.read()
grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(grayimg, 80, 255, cv2.THRESH_BINARY)
_, thresh_inv = cv2.threshold(grayimg, 80, 255, cv2.THRESH_BINARY_INV)
nonzero = cv2.countNonZero(thresh)
nonzero_inv = cv2.countNonZero(thresh_inv)

if nonzero - nonzero_inv > 0:
    now = datetime.datetime.now()
    current_date = now.strftime(DIR)
    current_time = now.strftime(FILE)
    if not os.path.exists(os.path.join(OUTPUT_DIR, current_date)):
        os.makedirs(os.path.join(OUTPUT_DIR, current_date))
    cv2.imwrite(os.path.join(OUTPUT_DIR, current_date, current_time), frame)

cap.release()

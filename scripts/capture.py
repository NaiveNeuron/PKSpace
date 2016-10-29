import cv2
import datetime
import os
import sys
import optparse

OUTPUT_DIR = '/home/pi/data'
DIR = '%Y-%m-%d'
FILE = '%H:%M:%S.png'


def capture_and_save(warmup=15):
    cap = cv2.VideoCapture(0)

    #  warmup camera
    for i in range(15):
        _, _ = cap.read()

    ret, frame = cap.read()
    if not ret:
        print('Failed to capture frame, closing...')
        return

    grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(grayimg, 60, 255, cv2.THRESH_BINARY)
    nonzero = cv2.countNonZero(thresh)

    if thresh.size - nonzero < thresh.size // 3:
        now = datetime.datetime.now()
        current_date = now.strftime(DIR)
        current_time = now.strftime(FILE)
        if not os.path.exists(os.path.join(OUTPUT_DIR, current_date)):
            os.makedirs(os.path.join(OUTPUT_DIR, current_date))
        cv2.imwrite(os.path.join(OUTPUT_DIR, current_date, current_time), frame)
    cap.release()

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-w', '--warmup',
                      dest='warmup',
                      help='Warmup camera by capturing given number of frames',
                      default='15')
    options, _ = parser.parse_args(sys.argv[1:])
    capture_and_save(warmup=options.warmup)

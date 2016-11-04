import cv2
import datetime
import os
import click


DIR = '%Y-%m-%d'
FILE = '%H:%M:%S.png'


def matches(frame, threshold):
    grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(grayimg, threshold, 255, cv2.THRESH_BINARY)
    nonzero = cv2.countNonZero(thresh)

    return thresh.size - nonzero < thresh.size // 3


@click.command()
@click.option('--warmup', default=15,
              help='Warmup camera by capturing given number of frames')
@click.option('--threshold', default=60,
              help='Threshold value for grayscale to binary image')
@click.option('--path', default='.',
              help='Path where to save captured images')
@click.option('--image', default='',
              help='Specify path and get True/False for bright/dark image')
def capture_and_save(warmup, threshold, path, image):
    if image != '':
        print(matches(cv2.imread(image, 1), threshold))
        return

    cap = cv2.VideoCapture(0)

    #  warmup camera
    for i in range(warmup):
        _, _ = cap.read()

    ret, frame = cap.read()
    if not ret:
        print('Failed to capture frame, closing...')
        return

    if matches(frame, threshold):
        now = datetime.datetime.now()
        current_date = now.strftime(DIR)
        current_time = now.strftime(FILE)

        if not os.path.exists(os.path.join(path, current_date)):
            os.makedirs(os.path.join(path, current_date))
        cv2.imwrite(os.path.join(path, current_date, current_time), frame)

    cap.release()


if __name__ == '__main__':
    capture_and_save()

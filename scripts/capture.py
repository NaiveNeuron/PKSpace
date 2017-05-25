import cv2
import numpy as np
import datetime
import os
import click


DIR = '%Y-%m-%d'
FILE = '%H:%M:%S.png'


# taken from
# https://github.com/jrosebr1/imutils/blob/master/imutils/convenience.py#L41
def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def matches(frame, threshold, proportion=3):
    grayimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(grayimg, threshold, 255, cv2.THRESH_BINARY)
    nonzero = cv2.countNonZero(thresh)

    return thresh.size - nonzero < thresh.size // proportion


@click.command()
@click.option('--warmup', default=15,
              help='Warmup camera by capturing given number of frames')
@click.option('--threshold', default=60,
              help='Threshold value for grayscale to binary image')
@click.option('--path', default='.',
              help='Path where to save captured images')
@click.option('--image', default='',
              help='Specify path and get True/False for bright/dark image')
@click.option('--rotate', default=0,
              help='Rotate image (0 to 360 degrees)')
@click.option('--print-path', default=False,
              help='Boolean value whether to print path of the captured image')
def capture_and_save(warmup, threshold, path, image, rotate, print_path):
    if image:
        msg = "Matches image {0} with threshold {1}: {2}"
        print(msg.format(image, threshold,
                         matches(cv2.imread(image, 1), threshold)))
        return

    cap = cv2.VideoCapture(0)

    #  warmup camera
    for i in range(warmup):
        _, _ = cap.read()

    ret, frame = cap.read()
    if not ret:
        print('Failed to capture frame, closing...')
        return

    current_date = ''
    current_time = ''
    if matches(frame, threshold):
        now = datetime.datetime.now()
        current_date = now.strftime(DIR)
        current_time = now.strftime(FILE)

        if rotate > 0:
            frame = rotate_bound(frame, rotate)

        if not os.path.exists(os.path.join(path, current_date)):
            os.makedirs(os.path.join(path, current_date))
        cv2.imwrite(os.path.join(path, current_date, current_time), frame)

    cap.release()

    if print_path:
        print(os.path.join(current_date, current_time) if current_time else '')


if __name__ == '__main__':
    capture_and_save()

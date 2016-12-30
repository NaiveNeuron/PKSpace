import cv2
import datetime
import os
import click


DIR = '%Y-%m-%d'
FILE = '%H:%M:%S.png'


def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, M, (w, h))


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
def capture_and_save(warmup, threshold, path, image, rotate):
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

    if matches(frame, threshold):
        now = datetime.datetime.now()
        current_date = now.strftime(DIR)
        current_time = now.strftime(FILE)

        if rotate > 0:
            frame = rotate_image(frame, rotate)

        if not os.path.exists(os.path.join(path, current_date)):
            os.makedirs(os.path.join(path, current_date))
        cv2.imwrite(os.path.join(path, current_date, current_time), frame)

    cap.release()


if __name__ == '__main__':
    capture_and_save()

import cv2 as cv
import numpy as np


def get_LUV_features(image):
    '''
    Args:
        image(numpy.ndarray): Image from which LUV channels are extracted

    Returns:
        List of L,U,V channels respectively
    '''
    luv = cv.cvtColor(image, cv.COLOR_BGR2LUV)
    return cv.split(luv)


def get_gradient_matrix(image):
    '''
    Calculates gradient magnitude and angles matrices of given image

    Args:
        image(numpy.ndarray): Image from which matricies are calculated

    Returns:
        mag(numpy.ndarray): matrix of gradient magnitudes
        angles(numpy.ndarray): matrix of gradient angles
    '''
    gx = cv.Sobel(image, cv.CV_32F, 1, 0,)
    gy = cv.Sobel(image, cv.CV_32F, 0, 1,)
    mag, angles = cv.cartToPolar(gx, gy, angleInDegrees=True)
    return mag, angles


def get_oriented_gradients(angles, mag, bins, bin_size):
    '''
    Calculate oriented gradients from angles and magnitude

    Args:
        angles(numpy.ndarray): Matrix of gradient directions
                               (angles from <0, 360>)
        mag(numpy.ndarray): Matrix of gradient magnitudes
        bins(list): List of angles
        bins(int): Range of individual angle

    Returns:
        (numpy.ndarray): Array of idividual oriented gradient channels
    '''
    channels = []
    angles %= 180
    for b in bins:
        orient = ((b - bin_size) < angles) & (angles < (b + bin_size))
        channel = cv.bitwise_and(mag, mag, mask=orient.astype('uint8'))
        channels.append(channel)
    return np.asarray(channels)


def icf(image, bins, bin_size):
    '''
    Calculate integral channel features

    Args:
        image(numpy.ndarray): Image from which calculate ICF
        bins(list): List of angles
        bins(int): Range of individual angle

    Returns:
        (numpy.ndarray): Integral channel features
    '''
    channels = get_LUV_features(image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (3, 3), 0)
    mag, angles = get_gradient_matrix(gray)
    mag = cv.convertScaleAbs(mag)
    channels.append(mag)
    channels.extend(get_oriented_gradients(angles, mag, bins, bin_size))
    return map(lambda ch: cv.integral(ch), channels)

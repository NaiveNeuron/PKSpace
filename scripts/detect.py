#!/usr/bin/env python
import cv2 as cv
import click
import numpy as np


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              required=True)
@click.option('--background',
              type=click.Path(exists=True),
              required=True)
def main(filename, background):
    img = cv.imread(filename)
    cv.imshow('original', img)
    img_bg = cv.imread(background)

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_img_background = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)

    diff = cv.absdiff(gray_img, gray_img_background)
    _, diff = cv.threshold(diff, 45, 255, cv.THRESH_BINARY)
    diff = cv.erode(diff, np.ones((3, 3), np.uint8))
    diff = cv.dilate(diff, np.ones((7, 7), np.uint8), iterations=2)
    cv.imshow('adsf', diff)
    bg_mask = cv.bitwise_not(diff)
    img_a = img.copy()
    img_a[:, :, 0] = cv.bitwise_and(cv.split(img)[0], cv.bitwise_not(bg_mask))
    img_a[:, :, 1] = cv.bitwise_and(cv.split(img)[1], cv.bitwise_not(bg_mask))
    img_a[:, :, 2] = cv.bitwise_and(cv.split(img)[2], cv.bitwise_not(bg_mask))

    im = cv.cvtColor(img_a, cv.COLOR_RGB2LAB)
    cv.imshow('lab', im)
    im = im.reshape((-1, 3))

    # convert to np.float32
    im = np.float32(im)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 3, 1.0)
    k = 5
    ret, label, center = cv.kmeans(im, k, criteria, 10,
                                   cv.KMEANS_RANDOM_CENTERS)

    lt = label.reshape(img.shape[:2])
    lt = lt == 0
    t = lt.astype('uint8') * 255
    cv.imshow('adf', cv.bitwise_and(img_a, img_a, mask=cv.bitwise_not(t)))
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))
    cv.imshow('kmeans', res2)

    cv.imshow('diff rgb', img_a)
    cv.imwrite('diff.png', img_a)
    cv.imshow('diff', bg_mask)
    cv.waitKey(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python
import cv2 as cv
import click
import numpy as np


def preprocess(img):
    img_eq = exposure.equalize_hist(img)
    return img_eq


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              required=True)
@click.option('--background',
              type=click.Path(exists=True),
              required=True)
def main(filename, background):
    img = cv.imread(filename)
    img_background = cv.imread(background)

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('gray_img', gray_img)
    # gray_img = cv.equalizeHist(gray_img)
    cv.imshow('gray_img after equalization', gray_img)
    gray_img_background = cv.cvtColor(img_background, cv.COLOR_BGR2GRAY)
    cv.imshow('gray_img_background', gray_img_background)
    # gray_img_background = cv.equalizeHist(gray_img_background)
    cv.imshow('gray_img_background after equalization', gray_img_background)

    diff = cv.absdiff(gray_img, gray_img_background)

    cv.imshow('img', img)
    cv.imshow('img_background', img_background)
    cv.imshow('diff', diff)

    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray_img)
    cv.imshow('clahe img', cl1)
    cl2 = clahe.apply(gray_img_background)
    cv.imshow('clahe img_background', cl2)

    cl_diff = cv.absdiff(cl1, cl2)
    cv.imshow('clahe diff', cl_diff)

    cl_diff_cleared = cv.medianBlur(cl_diff, 3)
    cv.imshow('clahe diff medianBlur', cl_diff_cleared)

    cl_diff_cleared_bilateral = cv.bilateralFilter(cl_diff, 9, 75, 75)
    cv.imshow('clahe diff bilateralFilter', cl_diff_cleared_bilateral)

    diff_cleared = cv.medianBlur(diff, 3)
    cv.imshow('diff medianBlur', diff_cleared)

    diff_cleared_bilateral = cv.bilateralFilter(diff, 9, 75, 75)
    cv.imshow('diff bilateralFilter', diff_cleared_bilateral)

    kernel = np.ones((3, 3), np.uint8)

    erosion = cv.erode(diff_cleared_bilateral, kernel, iterations=1)
    cv.imshow('diff eroded', erosion)

    th2 = cv.adaptiveThreshold(erosion, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                               cv.THRESH_BINARY, 5, 3)

    thresholded = cv.adaptiveThreshold(erosion, 255,
                                       cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv.THRESH_BINARY, 15, 2)

    cv.imshow('threshold', thresholded)
    cv.imshow('threshold mean', th2)

    kernel = np.ones((2, 2), np.uint8)
    cv.imshow('threshold mean dilated', cv.dilate(th2, kernel, iterations=1))
    cv.waitKey(0)


if __name__ == '__main__':
    main()

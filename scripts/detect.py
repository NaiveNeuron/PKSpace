#!/usr/bin/env python
import cv2 as cv
import click
import numpy as np
import pymeanshift as pms


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
    matfyz_mask = cv.cvtColor(cv.imread('matfyz_mask.png'), cv.COLOR_BGR2GRAY)
    _, matfyz_mask = cv.threshold(matfyz_mask, 200, 255, cv.THRESH_BINARY)
    matfyz_mask = cv.bitwise_not(matfyz_mask)

    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_img_background = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)

    diff = cv.absdiff(gray_img, gray_img_background)
    _, diff = cv.threshold(diff, 45, 255, cv.THRESH_BINARY)
    diff = cv.erode(diff, np.ones((3, 3), np.uint8))
    diff = cv.dilate(diff, np.ones((7, 7), np.uint8), iterations=4)
    bg_mask = cv.bitwise_not(diff)
    img_a = img.copy()
    img_a[:, :, 0] = cv.bitwise_and(cv.split(img)[0], cv.bitwise_not(bg_mask))
    img_a[:, :, 1] = cv.bitwise_and(cv.split(img)[1], cv.bitwise_not(bg_mask))
    img_a[:, :, 2] = cv.bitwise_and(cv.split(img)[2], cv.bitwise_not(bg_mask))
    img_a[:, :, 0] = cv.equalizeHist(cv.split(img_a)[0])
    img_a[:, :, 1] = cv.equalizeHist(cv.split(img_a)[1])
    img_a[:, :, 2] = cv.equalizeHist(cv.split(img_a)[2])
    img_a = cv.bitwise_and(img_a, img_a, mask=matfyz_mask)
    img_a = cv.GaussianBlur(img_a, (3, 3), 2)

    # kernel = [[0, 0, 0, 1,  5],
    #           [0, 0, 1, 5, -1],
    #           [0, 1, 5, -1, 0],
    #           [1, 5, -1, 0, 0],
    #           [5, -1, 0, 0, 0]]
    # kernel = np.array(kernel)
    # kernel = kernel / float(np.sum(kernel))
    # print(kernel)

    # test = np.zeros((500, 500))
    # test[200:300, 200:300] = np.ones((100, 100))
    # cv.imshow('test', test)

    # kernel_image = cv.cvtColor(img_a, cv.COLOR_BGR2GRAY) / 255.0
    # cv.imshow('kernel_image', kernel_image)
    # dst = cv.filter2D(test, cv.CV_64F, kernel) * 255
    # dst = sig.convolve2d(kernel_image, kernel, 'same') * 255
    # cv.imshow('after kernel', dst)
    # cv.imshow('diff kernel', cv.absdiff(cv.cvtColor(img_a, cv.COLOR_BGR2GRAY),
    #                                     dst.astype('uint8')))

    (x, y, z) = pms.segment(img_a, spatial_radius=10, range_radius=10,
                            min_density=200)
    # canny = cv.Canny(x, 150, 255)
    # canny = cv.dilate(canny, np.ones((3, 3), np.uint8))
    # canny = cv.erode(canny, np.ones((3, 3), np.uint8))
    sobelx = cv.Sobel(cv.cvtColor(x, cv.COLOR_BGR2GRAY), -1, 1, 0, ksize=3)
    sobely = cv.Sobel(cv.cvtColor(x, cv.COLOR_BGR2GRAY), -1, 0, 1, ksize=3)
    cv.imshow('sobelx', sobelx)
    cv.imshow('sobely', sobely)
    # print(z)
    # cv.imshow('x', x)
    # for i in range(0, z):
    #     cv.imshow('k: {}'.format(i), cv.bitwise_and(img_a, img_a,
    #               mask=((y == i).astype('uint8') * 255)))
    #     cv.waitKey(0)

    # h, w = img_a.shape[:2]
    # mask = np.zeros((h+2, w+2), np.uint8)
    # connectivity = 4
    # mask[:] = 0
    # flags = connectivity
    # flags |= cv.FLOODFILL_MASK_ONLY
    # flags |= 255 << 8
    # for i in xrange(0, 50):
    #     seed = np.rand
    #     cv.floodFill(img_a, mask, self.seed, (255, 255, 255), (self.lo,)*3,
    #                  (self.hi,)*3, flags)

    cv.imshow('img RGB', img_a)
    cv.waitKey(0)

if __name__ == '__main__':
    main()

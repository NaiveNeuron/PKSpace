#!/usr/bin/env python
import cv2 as cv
import click
import numpy as np
import glob
import pymeanshift as pms


def masks_from_folder(folder, img_ext='.png'):
    glob_selector = '{}/pk*{}'.format(folder, img_ext)
    for file in glob.glob(glob_selector):
        mask_filename = '{}'.format(file)
        yield mask_filename


@click.command()
@click.option('--filename',
              type=click.Path(exists=True),
              required=True)
@click.option('--background',
              type=click.Path(exists=True),
              required=True)
@click.option('--threshold',
              nargs=24,
              type=float,
              required=True)
def main(filename, background, threshold):
    img = cv.imread(filename)
    img_background = cv.imread(background)
    park_mask = cv.imread('../masks/mask_big.png', 0)
    _, park_mask = cv.threshold(park_mask, 200, 255, cv.THRESH_BINARY)
    diff_i = cv.bitwise_and(img, img, mask=park_mask.astype('uint8'))
    diff_b = cv.bitwise_and(img_background, img_background,
                            mask=park_mask.astype('uint8'))
    (diff_i, _, _) = pms.segment(diff_i, spatial_radius=5, range_radius=5,
                                 min_density=100)
    (diff_b, _, _) = pms.segment(diff_b, spatial_radius=10, range_radius=10,
                                 min_density=300)
    cv.imshow('mean bg', diff_b)
    diff = cv.absdiff(diff_i, diff_b)
    cv.imshow('diff', diff)
    free_spots = 0
    pk_var = []
    masks = []
    for mask_filename in masks_from_folder('../masks'):
        mask = cv.imread(mask_filename, 0)
        _, mask = cv.threshold(mask, 200, 255, cv.THRESH_BINARY)
        masks.append(mask)
        pk_space = cv.bitwise_and(diff, diff, mask=mask)
        pk_var.append(np.std(pk_space[np.nonzero(pk_space)]))

    for i, var in enumerate(pk_var):
        if var < threshold[i]:
            free_spots += 1
            mask = cv.cvtColor(masks[i], cv.COLOR_GRAY2RGB)
            mask[:, :, 0] = 0
            mask[:, :, 2] = 0
            img = cv.addWeighted(img, 1, mask, 0.2, 0)

    print('Free spots: {}'.format(free_spots))
    cv.imshow('Free spots: {}'.format(free_spots), img)
    cv.imwrite('img.png', img)
    cv.waitKey(0)


if __name__ == '__main__':
    main()

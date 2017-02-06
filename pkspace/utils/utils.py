import os

import cv2

from pkspace.utils import loaders


def load_dataset(loader, path, split):
    return loader.load(path, split)


def visual(x_train, y_train):
    for picture in x_train:
        cv2.imshow('image', picture)
        cv2.waitKey(0)


if __name__ == '__main__':
    loader = loaders.PKspaceLoader()
    a, b, c, d = load_dataset(loader, 'labeled_data/2017-01-10', 0.2)

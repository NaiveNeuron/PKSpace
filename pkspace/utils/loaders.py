import glob
import json
import os
import xml.etree.ElementTree
import cv2
import numpy as np


class Loader:
    def load(self, path, split):
        pass


class PKspaceLoader(Loader):
    def __get_spaces__(self, src, desc):
        finsize = (80, 80)
        spaces = []
        answers = []
        for space in desc.get('spots'):
            points = space.get('points')
            angle = space.get('rotation')
            nove_pole = np.hstack(
                (np.asarray(points), np.ones((len(points), 1))))

            center = np.mean(nove_pole, 0)[:2]
            center = (center[0],center[1])
            rows, cols, tmp = src.shape

            min_x, min_y = cols, rows
            max_x, max_y = 0, 0
            rad = np.math.radians(angle)
            for x, y in points:
                dx = (x - center[0])
                dy = (y - center[1])
                a = center[0]
                b = center[1]
                cos = np.cos(rad)
                sin = np.sin(rad)

                x_rotated = (dx * cos) - (dy * sin) + a
                y_rotated = (dx * sin) + (dy * cos) + b
                min_x = max(min(min_x, int(x_rotated)), 0)
                min_y = max(min(min_y, int(y_rotated)), 0)
                max_x = min(max(max_x, int(x_rotated)), cols)
                max_y = min(max(max_y, int(y_rotated)), rows)

            m = cv2.getRotationMatrix2D(center, -angle, 1)
            # nove_pole = m.dot(nove_pole.T).T
            # nove_pole[:, 0] = np.clip(nove_pole[:, 0], 0, cols)
            # nove_pole[:, 1] = np.clip(nove_pole[:, 1], 0, rows)
            # nove_pole = nove_pole.astype('uint8')
            # minima = nove_pole.min(axis=0)
            # maxima = nove_pole.max(axis=0)
            # print(nove_pole)
            # min_x, min_y = minima[:2]
            # max_x, max_y = maxima[:2]

            rotated = cv2.warpAffine(src, m, (cols, rows))
            roi = rotated[min_y:max_y, min_x:max_x]
            fin = cv2.resize(roi, finsize).flatten()
            spaces.append(fin)
            answers.append(space.get('occupied', -1))
        return spaces, answers

    def load(self, path, split, extension='.png'):
        all_parking_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, extension)):
            img = cv2.imread(file)
            jsonfile = open("{}.json".format(os.path.splitext(file)[0]))
            desc = json.load(jsonfile)
            spaces, answers = self.__get_spaces__(img, desc)
            all_parking_spaces.append(spaces)
            all_answers.append(answers)
        all_parking_spaces = np.asarray(all_parking_spaces)
        all_answers = np.asarray(all_answers)
        assert split < 1, 'split needs to be smaller than 1'
        train_size = int(np.ceil(len(all_parking_spaces) * split))
        indices = np.random.permutation(len(all_parking_spaces))
        x_train = all_parking_spaces[indices[:train_size]]
        y_train = all_answers[indices[:train_size]]
        x_test = all_parking_spaces[indices[:-train_size]]
        y_test = all_answers[indices[:-train_size]]
        return x_train, x_test, y_train, y_test


class PKlotLoader(Loader):
    def __get_spaces__(self, src, tabroot):
        fin_size = (80, 80)
        spaces = []
        answers = []
        for space in tabroot:
            center = int(space[0][0].get('x')), int(space[0][0].get('y'))
            h, w = int(space[0][1].get('h')), int(space[0][1].get('w'))
            m = cv2.getRotationMatrix2D(center, int(space[0][2].get('d')), 1)
            rows, cols, tmp = src.shape
            dst = cv2.warpAffine(src, m, (cols, rows))
            roi = dst[
                int(center[1] - h / 2):int(center[1] + h / 2),
                int(center[0] - w / 2):int(center[0] + w / 2)]
            fin = cv2.resize(roi, fin_size).flatten()
            answers.append(space.get('occupied', 1))
            spaces.append(fin)
        return spaces, answers

    def load(self, path, split, extension='.jpg'):
        all_parking_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, extension)):
            img = cv2.imread(file)
            e = xml.etree.ElementTree.parse(
                "{}.xml".format(os.path.splitext(file)[0]))
            root = e.getroot()
            spaces, answers = self.__get_spaces__(img, root)
            all_parking_spaces.append(spaces)
            all_answers.append(answers)
        all_parking_spaces = np.asarray(all_parking_spaces)
        all_answers = np.asarray(all_answers)
        assert split < 1, 'split needs to be smaller than 1'
        train_size = int(np.ceil(len(all_parking_spaces) * split))
        indices = np.random.permutation(len(all_parking_spaces))
        x_train = all_parking_spaces[indices[:train_size]]
        y_train = all_answers[indices[:train_size]]
        x_test = all_parking_spaces[indices[:-train_size]]
        y_test = all_answers[indices[:-train_size]]
        return x_train, x_test, y_train, y_test

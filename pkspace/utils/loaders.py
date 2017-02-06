import glob
import json
import os
import xml.etree.ElementTree

import cv2
import numpy as np
import scipy.ndimage


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
            nove_pole = np.hstack((np.asarray(points), np.ones((len(points), 1))))
            sum_x, sum_y = 0, 0
            for x, y in points:
                sum_x += x
                sum_y += y
            center = np.ceil(sum_x / len(points)), np.ceil(sum_y / len(points))
            # if(center[0]!=int(np.mean(nove_pole,0)[0]) or center[1]!=int(np.mean(nove_pole, 0)[1])):
            #     print(center[0],np.mean(nove_pole,0),center[1],np.mean(nove_pole,0))
            rows, cols, tmp = src.shape
            min_x, min_y = rows,cols
            max_x, max_y = 0, 0
            for x, y in points:
                xrotated = ((x - center[0]) * np.cos(np.math.radians(angle))) - (
                (y - center[1]) * np.sin(np.math.radians(angle))) + center[0]
                yrotated = ((x - center[0]) * np.sin(np.math.radians(angle))) + (
                (y - center[1]) * np.cos(np.math.radians(angle))) + center[1]
                min_x, min_y = max(min(min_x, int(xrotated)), 0), max(min(min_y, int(yrotated)), 0)
                max_x, max_y = max(max_x, int(xrotated)), max(max_y, int(yrotated))

            M = cv2.getRotationMatrix2D(center, -angle, 1)
            # nove_pole = M.dot(nove_pole.T).T
            #
            # nove_pole[:, 0] = np.clip(nove_pole[:, 0], 0, rows)
            # nove_pole[:, 1] = np.clip(nove_pole[:, 1], 0, cols)
            # nove_pole = nove_pole.astype('uint8')
            # minima = nove_pole.min(axis=0)
            # maxima = nove_pole.max(axis=0)
            # # print(nove_pole)
            # min_x, min_y = minima[:2]
            # max_x, max_y = maxima[:2]

            rotated = cv2.warpAffine(src, M, (cols, rows))
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
            with open("{}.json".format(os.path.splitext(file)[0])) as data_file:
                desc = json.load(data_file)
            spaces, answers = self.__get_spaces__(img, desc)
            all_parking_spaces.append(spaces)
            all_answers.append(answers)
        all_parking_spaces = np.asarray(all_parking_spaces)
        all_answers = np.asarray(all_answers)
        assert split < 1, print('split needs to be smaller than 1')
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
            M = cv2.getRotationMatrix2D(center, int(space[0][2].get('d')), 1)
            rows, cols, tmp = src.shape
            dst = cv2.warpAffine(src, M, (cols, rows))
            roi = dst[int(center[1] - h / 2):int(center[1] + h / 2), int(center[0] - w / 2):int(center[0] + w / 2)]
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
            e = xml.etree.ElementTree.parse("{}.xml".format(os.path.splitext(file)[0]))
            root = e.getroot()
            spaces, answers = self.__get_spaces__(img, root)
            all_parking_spaces.append(spaces)
            all_answers.append(answers)
        all_parking_spaces = np.asarray(all_parking_spaces)
        all_answers = np.asarray(all_answers)
        assert split < 1, print('split needs to be smaller than 1')
        train_size = int(np.ceil(len(all_parking_spaces) * split))
        indices = np.random.permutation(len(all_parking_spaces))
        x_train = all_parking_spaces[indices[:train_size]]
        y_train = all_answers[indices[:train_size]]
        x_test = all_parking_spaces[indices[:-train_size]]
        y_test = all_answers[indices[:-train_size]]
        return x_train, x_test, y_train, y_test

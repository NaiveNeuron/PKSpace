import glob
import json
import os
import xml.etree.ElementTree
import cv2
import numpy as np


class Loader:
    def load(self, path, split):
        pass


class PKSpaceLoader(Loader):
    def _get_spaces(self, src, desc, fin_size):
        spaces = []
        answers = []
        for space in desc['spots']:
            points = space['points']
            angle = space.get('rotation', 0)
            points = np.hstack(
                (np.asarray(points), np.ones((len(points), 1))))
            center = np.mean(points, 0)[:2]
            center = (center[0], center[1])
            rows, cols, _ = src.shape
            m = cv2.getRotationMatrix2D(center, -angle, 1)
            rotated = cv2.warpAffine(src, m, (cols, rows))

            points = m.dot(points.T).T
            points[:, 0] = np.clip(points[:, 0], 0, cols)
            points[:, 1] = np.clip(points[:, 1], 0, rows)
            min_x, min_y = points.min(axis=0).astype('uint32')
            max_x, max_y = points.max(axis=0).astype('uint32')

            roi = rotated[min_y:max_y, min_x:max_x]
            fin = cv2.resize(roi, fin_size).flatten()
            spaces.append(fin)
            answers.append(space['occupied'])
        return spaces, answers

    def load(self, path, split, extension='.png', size=(80, 80)):
        all_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, extension)):
            img = cv2.imread(file)
            file_name_base = os.path.splitext(file)[0]
            json_file = open("{}.json".format(file_name_base))
            desc = json.load(json_file)
            spaces, answers = self._get_spaces(img, desc, size)
            all_spaces.append(spaces)
            all_answers.append(answers)

        all_spaces = np.asarray(all_spaces)
        all_answers = np.asarray(all_answers)
        all_spaces = all_spaces.reshape(-1, all_spaces.shape[-1])
        all_answers = all_answers.reshape(-1)

        assert split < 1, 'split needs to be smaller than 1'

        train_size = int(np.ceil(len(all_spaces) * split))
        indices = np.random.permutation(len(all_spaces))
        x_train = all_spaces[indices[:train_size]]
        y_train = all_answers[indices[:train_size]]
        x_test = all_spaces[indices[:-train_size]]
        y_test = all_answers[indices[:-train_size]]
        return x_train, x_test, y_train, y_test


class PKLotLoader(Loader):
    def _get_spaces(self, src, tab_root, fin_size):
        spaces = []
        answers = []
        for space in tab_root:
            center = int(space[0][0]['x']), int(space[0][0]['y'])
            h, w = int(space[0][1]['h']), int(space[0][1]['w'])
            angle = float(space[0][2].get('d', 0))

            m = cv2.getRotationMatrix2D(center, angle, 1)
            rows, cols, _ = src.shape
            rotated = cv2.warpAffine(src, m, (cols, rows))

            min_x, max_x = int(center[0] - w / 2), int(center[0] + w / 2)
            min_y, max_y = int(center[1] - h / 2), int(center[1] + h / 2)
            roi = rotated[min_y:max_y, min_x, max_x]
            fin = cv2.resize(roi, fin_size).flatten()
            answers.append(space.get('occupied', 1))
            spaces.append(fin)
        return spaces, answers

    def load(self, path, split=0.5, extension='.jpg', size=(80, 80)):
        all_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, extension)):
            img = cv2.imread(file)
            xml_name_base = os.path.splitext(file)[0]
            e = xml.etree.ElementTree.parse("{}.xml".format(xml_name_base))
            root = e.getroot()
            spaces, answers = self._get_spaces(img, root, size)
            all_spaces.append(spaces)
            all_answers.append(answers)
        all_spaces = np.asarray(all_spaces)
        all_answers = np.asarray(all_answers)

        assert split < 1, 'split needs to be smaller than 1'

        train_size = int(np.ceil(len(all_spaces) * split))
        indices = np.random.permutation(len(all_spaces))

        x_train_days = all_spaces[indices[:train_size]]
        y_train_days = all_answers[indices[:train_size]]
        x_test_days = all_spaces[indices[:-train_size]]
        y_test_days = all_answers[indices[:-train_size]]

        x_train = x_train_days.reshape(-1, x_train_days.shape[-1])
        y_train = y_train_days.reshape(-1)
        x_test = x_test_days.reshape(-1, x_test_days.shape[-1])
        y_test = y_test_days.reshape(-1)
        return x_train, x_test, y_train, y_test

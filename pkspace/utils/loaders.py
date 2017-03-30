import glob
import json
import os
import xml.etree.ElementTree
import cv2
import numpy as np


class Loader:
    def load(self, path):
        pass

    def load_pic(self, pic_path, desc_path, fin_size):
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

            # rotating points and searching for minimal bounding rectangle
            points = m.dot(points.T).T
            points[:, 0] = np.clip(points[:, 0], 0, cols)
            points[:, 1] = np.clip(points[:, 1], 0, rows)
            min_x, min_y = points.min(axis=0).astype('uint32')
            max_x, max_y = points.max(axis=0).astype('uint32')

            roi = rotated[min_y:max_y, min_x:max_x]
            fin = cv2.resize(roi, fin_size).flatten()
            spaces.append(fin)
            answers.append(space.get('occupied'))
        return spaces, answers

    def load(self, path, extension='.png', size=(80, 80)):
        all_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, '*', extension)):
            file_name_base = os.path.splitext(file)[0]
            json_filename = "{}.json".format(file_name_base)
            spaces, answers = self.load_pic(file, json_filename, size)
            all_spaces.append(spaces)
            all_answers.append(answers)
        all_spaces = np.asarray(all_spaces)
        all_answers = np.asarray(all_answers)
        all_spaces = all_spaces.reshape(-1, all_spaces.shape[-1])
        all_answers = all_answers.reshape(-1)
        return all_spaces, all_answers

    def load_pic(self, pic_path, desc_path, fin_size=(80, 80)):
        img = cv2.imread(pic_path)
        json_file = open(desc_path)
        desc = json.load(json_file)
        return self._get_spaces(img, desc, fin_size)


class PKLotLoader(Loader):
    def _get_spaces(self, src, tab_root, fin_size):
        spaces = []
        answers = []
        for space in tab_root:
            center = int(space[0][0].get('x')), int(space[0][0].get('y'))
            h, w = int(space[0][1].get('h')), int(space[0][1].get('w'))
            angle = float(space[0][2].get('d', 0))

            m = cv2.getRotationMatrix2D(center, angle, 1)
            rows, cols, _ = src.shape
            rotated = cv2.warpAffine(src, m, (cols, rows))

            min_x = max(int(center[0] - w / 2), 0)
            min_y = max(int(center[1] - h / 2), 0)
            max_x = min(int(center[0] + w / 2), cols)
            max_y = min(int(center[1] + h / 2), rows)
            roi = rotated[min_y:max_y, min_x:max_x]
            fin = cv2.resize(roi, fin_size).flatten()
            answers.append(space.get('occupied', 1))
            spaces.append(fin)
        return spaces, answers

    def load(self, path, extension='.jpg', size=(80, 80)):
        all_spaces = []
        all_answers = []
        extension = "*{}".format(extension)
        for file in glob.glob(os.path.join(path, '*', '*', extension)):
            xml_filename = "{}.xml".format(os.path.splitext(file)[0])
            if os.path.isfile(xml_filename):
                spaces, answers = self.load_pic(file, xml_filename)
                all_spaces.append(spaces)
                all_answers.append(answers)
        all_spaces = np.asarray(all_spaces)
        all_answers = np.asarray(all_answers)
        all_spaces = all_spaces.reshape(-1, all_spaces.shape[-1])
        all_answers = all_answers.reshape(-1)
        return all_spaces, all_answers

    def load_pic(self, pic_path, desc_path, fin_size=(80, 80)):
        img = cv2.imread(pic_path)
        e = xml.etree.ElementTree.parse(desc_path)
        root = e.getroot()
        return self._get_spaces(img, root, fin_size)
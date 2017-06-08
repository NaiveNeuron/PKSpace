import json
import os
import re
import pickle
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from pkspace.utils.loaders import PKSpaceLoader # noqa
from configapp.default_settings import IMAGE_SUFFIX # noqa
import click # noqa


@click.command()
@click.option('--mask_path', required=True,
              help='Path of json file of the mask')
@click.option('--picture_path', required=True,
              help='Path of picture to be predicted')
@click.option('--model_path', required=True,
              help='Path where pretrained model is located')
@click.option('--predict_dir', default='.',
              help='Directory for storing predictions')
@click.option('--output', default=None,
              help='Name of file for predicted output')
def load_and_predict(mask_path, picture_path, model_path, predict_dir, output):
    for file in (mask_path, picture_path, model_path, predict_dir):
        if not os.path.exists(file):
            print(file, 'Path does not exist')
            return

    if output is None:
        basename = os.path.basename(picture_path)
        basename = re.sub(IMAGE_SUFFIX + '$', '.json', basename)
        dirname = os.path.basename(os.path.dirname(picture_path))
        output = os.path.join(dirname, basename)

    if os.path.splitext(mask_path)[-1] == '.json':
        loader = PKSpaceLoader()
        pictures, _ = loader.load_pic(picture_path, mask_path)
    else:
        print('Unknown description file')
        return

    with open(model_path, 'rb') as fp:
        model = pickle.load(fp)
    answers = model.predict(pictures)

    with open(mask_path, 'r') as fp:
        input_file = json.load(fp)

    count = 0
    for spot in input_file['spots']:
        spot['occupied'] = answers[count].item()
        count += 1

    with open(os.path.join(predict_dir, output), 'w') as fp:
        json.dump(input_file, fp)


if __name__ == '__main__':
    load_and_predict()

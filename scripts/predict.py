from __future__ import print_function
import json
import os
import re
import pickle
import sys
import click
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from pkspace.utils.loaders import PKSpaceLoader # noqa


@click.command()
@click.option('--mask_path', required=True, type=click.Path(exists=True),
              help='Path of json file of the mask')
@click.option('--picture_path', required=True, type=click.Path(exists=True),
              help='Path of picture to be predicted')
@click.option('--model_path', required=True, type=click.Path(exists=True),
              help='Path where pretrained model is located')
@click.option('--output', default=None,
              help='Name of file for predicted output')
@click.option('--img_suffix', default='.png',
              help='Suffix of predicted image')
def load_and_predict(mask_path, picture_path, model_path, output, img_suffix):
    if output is None:
        output = '{}_out.json'.format(os.path.splitext(picture_path)[-2])
    elif not output.endswith('.json'):
        output = re.sub(img_suffix + '$', '.json', output)

    if not os.path.exists(dirname(output)):
        os.makedirs(dirname(output))

    if os.path.splitext(mask_path)[-1] == '.json':
        loader = PKSpaceLoader()
        pictures, _ = loader.load_pic(picture_path, mask_path)
    else:
        print('Unknown description file.', file=sys.stderr)
        sys.exit(1)

    with open(model_path, 'rb') as fp:
        model = pickle.load(fp)
    answers = model.predict(pictures)

    with open(mask_path, 'r') as fp:
        input_file = json.load(fp)

    count = 0
    for spot in input_file['spots']:
        spot['occupied'] = answers[count].item()
        count += 1

    with open(output, 'w') as fp:
        json.dump(input_file, fp)


if __name__ == '__main__':
    load_and_predict()

import json
import os
import pickle
import sys
from os.path import dirname, abspath
sys.path.append(dirname(abspath(__file__)))
from pkspace.utils.loaders import PKSpaceLoader
import click


@click.command()
@click.option('--mask_path',
              help='Adress of json file of the mask')
@click.option('--picture_path',
              help='Adress of picture to be predicted')
@click.option('--model_path',
              help='Path where pretrained model')
@click.option('--output', default=None,
              help='Name of output file for predicted output')
def load_and_predict(mask_path, picture_path, model_path, output):
    for file in (mask_path, picture_path, model_path):
        if not os.path.exists(file):
            print(file, "Path does not exist")
            return
    if output is None:
        output = "{}_o.json".format(os.path.splitext(picture_path)[-2])

    if os.path.splitext(mask_path)[-1] == ".json":
        loader = PKSpaceLoader()
        pictures, _ = loader.load_pic(picture_path, mask_path)
    else:
        print("Unknown description file")
        return
    with open(model_path, "rb") as fp:
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

import os
import pickle
import click
from sklearn.metrics import classification_report
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.argument('dataset_dir')
@click.argument('model_file')
def test_model(loader, dataset_dir, model_file):
    if not os.path.isdir(dataset_dir):
        print('{} is not a directory')
        return

    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    with open(model_file, 'rb') as mp:
        model = pickle.load(mp)
    spaces, ground_answers = loader.load(dataset_dir)
    model_answers = model.predict(spaces)
    print(classification_report(ground_answers, model_answers))


if __name__ == '__main__':
    test_model()

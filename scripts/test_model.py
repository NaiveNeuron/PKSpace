import os
import pickle
import click
from sklearn.metrics import classification_report
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader


@click.command()
@click.option('--PKSpace', 'dataset_mode', flag_value='PKSpace',
              default=True)
@click.option('--PKLot', 'dataset_mode', flag_value='PKLot')
@click.option('--dataset_dir', required=True,
              help='Directory of dataset for model to be tested on')
@click.option('--model_file', required=True,
              help='Pickle file of exported model')
def test_model(dataset_mode, dataset_dir, model_file):
    if not os.path.isdir(dataset_dir):
        print('{} is not a directory')
        return

    if dataset_mode == 'PKSpace':
        loader = PKSpaceLoader()
    elif dataset_mode == 'PKLot':
        loader = PKLotLoader()

    with open(model_file, 'rb') as mp:
        model = pickle.load(mp)
    spaces, ground_answers = loader.load(dataset_dir)
    model_answers = model.predict(spaces)
    print(classification_report(ground_answers, model_answers))


if __name__ == '__main__':
    test_model()

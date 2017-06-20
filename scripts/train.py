import os
import click
import pickle
import sys
from sklearn.neural_network import MLPClassifier
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader
from pkspace.utils import trainer


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.option('--model_type', '-mt', type=click.Choice(['MLP']), default='MLP',
              help='Type of model to be trained')
@click.option('--model_path', '-pm', type=click.Path(exists=True),
              default=None,
              help='Path to trained model, to be used as a base in training')
@click.argument('dataset_dir', type=click.Path(exists=True))
@click.option('--output', '-o', default='out.pkl',
              help='Path to output file for trained model')
def train(loader, model_type, model_path, dataset_dir, output):
    if not os.path.isdir(dataset_dir):
        sys.stderr.write('{} is not a directory'.format(dataset_dir))
        sys.exit(1)

    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    if model_path is not None:
        with open(model_path, 'rb') as fp:
            model = pickle.load(fp)
    elif model_type == 'MLP':
        model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(15, 10))

    spaces, answers = loader.load(dataset_dir)
    trained_model = trainer.train(spaces, answers, model)
    with open(output, 'wb') as out:
        pickle.dump(trained_model, out)


if __name__ == '__main__':
    train()

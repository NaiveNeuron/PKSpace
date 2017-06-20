import os
import click
import sys
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.option('--model_type', '-mt', type=click.Choice(['MLP']), default='MLP',
              help='Type of model to be trained')
# @click.option('--hidden_later', '-hl', default=(15, 10),
#               help='Hidden layers of MLP, if MLP is chosen as model_type')
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

    spaces, answers = loader.load(dataset_dir)

    if model_path is not None:
        model = joblib.load(model_path)

        if not callable(getattr(model, 'partial_fit', None)):
            sys.stderr.write('{} is not further trainable'.format(model_path))
            sys.exit(1)

        trained_model = model.partial_fit(spaces, answers)

    elif model_type == 'MLP':
        model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(15, 10))

        trained_model = model.partial_fit(spaces, answers, [0, 1])

    joblib.dump(trained_model, output, protocol=0)


if __name__ == '__main__':
    train()

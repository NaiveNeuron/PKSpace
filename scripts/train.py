import os
import click
import sys
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.option('--model_type', '-t', type=click.Choice(['MLP']), default='MLP',
              help='Type of model to be trained')
@click.option('--hidden_layer', '-h', default="15 10",
              help='Hidden layers of MLP, if MLP is chosen as model_type')
@click.option('--model_path', '-p', type=click.Path(exists=True),
              default=None,
              help='Path to trained model, to be used as a base in training')
@click.argument('dataset_dir', type=click.Path(exists=True))
@click.option('--output', '-o', default='out.pkl',
              help='Path to output file for trained model')
def train(loader, model_type, hidden_layer, model_path, dataset_dir, output):
    if not os.path.isdir(dataset_dir):
        sys.stderr.write('{} is not a directory'.format(dataset_dir))
        sys.exit(1)

    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    if model_path is not None:
        model = joblib.load(model_path)

    elif model_type == 'MLP':
        layers = hidden_layer.split()
        try:
            layers = [int(x) for x in layers]
        except ValueError:
            sys.stderr.write("--hidden_layer must be ints separated by spaces")
        model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=layers)

    spaces, answers = loader.load(dataset_dir)
    trained_model = model.fit(spaces, answers)

    joblib.dump(trained_model, output, protocol=0)


if __name__ == '__main__':
    train()

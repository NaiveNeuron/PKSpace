import os
import click
import sys
from sklearn.externals import joblib
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sklearn.neural_network import MLPClassifier # noqa
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader # noqa


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.option('--model_type', '-t', type=click.Choice(['MLP']), default='MLP',
              help='Type of model to be trained')
@click.option('--hidden_layer', '-h', default=(15, 10), multiple=True,
              type=int,
              help='Hidden layers of MLP, if MLP is chosen as model_type')
@click.option('--model_path', '-p', default=None,
              type=click.Path(exists=True, dir_okay=False, file_okay=True,
                              resolve_path=True),
              help='Path to trained model, to be used as a base in training')
@click.argument('dataset_dir',
                type=click.Path(exists=True, file_okay=False, dir_okay=True,
                                resolve_path=True))
@click.option('--output', '-o', default='out.pkl', type=click.Path(),
              help='Path to output file for trained model')
def train(loader, model_type, hidden_layer, model_path, dataset_dir, output):
    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    if model_path is not None:
        model = joblib.load(model_path)

    elif model_type == 'MLP':
        model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=hidden_layer)

    spaces, answers = loader.load(dataset_dir)
    trained_model = model.fit(spaces, answers)

    joblib.dump(trained_model, output, protocol=0)


if __name__ == '__main__':
    train()

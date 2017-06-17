import os
import click
import pickle
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sklearn.neural_network import MLPClassifier
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader
from pkspace.utils import trainer


@click.command()
@click.option('--PKSpace', 'dataset_mode', flag_value='PKSpace',
              default=True)
@click.option('--PKLot', 'dataset_mode', flag_value='PKLot')
@click.option('--MLP', 'method', flag_value='MLP',
              default=True, help='Method to be used for prediction')
@click.option('--dataset_dir', required=True,
              help='Directory of dataset for model to be trained on')
@click.option('--output', default=None,
              help='Name of output file for trained model')
def train(dataset_mode, method, dataset_dir, output):
    if not os.path.isdir(dataset_dir):
        print('{} is not a directory')
        return

    if output is None:
        output = os.path.join(dataset_dir, 'out.pkl')
    if dataset_mode == 'PKSpace':
        loader = PKSpaceLoader()
    elif dataset_mode == 'PKLot':
        loader = PKLotLoader()

    if method == 'MLP':
        model = MLPClassifier(solver='lbfgs', hidden_layer_sizes=(15, 10), random_state=1)

    spaces, answers = loader.load(dataset_dir)
    trained_model = trainer.train(spaces, answers, model)
    with open(output, 'wb') as out:
        pickle.dump(trained_model, out)
if __name__ == '__main__':
    train()

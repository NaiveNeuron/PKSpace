import click
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.argument('dataset_dir',
                type=click.Path(exists=True, file_okay=False, dir_okay=True,
                                resolve_path=True))
@click.argument('model_file',
                type=click.Path(exists=True, file_okay=True, dir_okay=False,
                                resolve_path=True))
def test_model(loader, dataset_dir, model_file):
    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    model = joblib.load(model_file)
    spaces, ground_answers = loader.load(dataset_dir)
    model_answers = model.predict(spaces)
    print(classification_report(ground_answers, model_answers))


if __name__ == '__main__':
    test_model()

import json
import click
from collections import Counter
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from sklearn.metrics import f1_score, recall_score, precision_score
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pkspace.utils.loaders import PKSpaceLoader, PKLotLoader # noqa


@click.command()
@click.option('--loader', '-l', type=click.Choice(['PKLot', 'PKSpace']),
              default='PKSpace', help='Loader used to load dataset')
@click.argument('dataset_dir',
                type=click.Path(exists=True, file_okay=False, dir_okay=True,
                                resolve_path=True))
@click.argument('model_file',
                type=click.Path(exists=True, file_okay=True, dir_okay=False,
                                resolve_path=True))
@click.option("--machine_friendly", '-f', is_flag=True,
              help='prints serialized dictionary of results')
def test_model(loader, dataset_dir, model_file, machine_friendly):
    if loader == 'PKSpace':
        loader = PKSpaceLoader()
    elif loader == 'PKLot':
        loader = PKLotLoader()

    model = joblib.load(model_file)
    spaces, ground_answers = loader.load(dataset_dir)
    model_answers = model.predict(spaces)
    if machine_friendly:
        answer = {'avg': {}, 0: {}, 1: {}}
        metrics = [precision_score, recall_score, f1_score]
        classes_counter = Counter(ground_answers)

        for i in [0, 1]:
            for func in metrics:
                score = func(ground_answers, model_answers, pos_label=i)
                answer[i][func.__name__] = score
            class_support = classes_counter[i]

            # summing total support
            answer[i]['support'] = class_support
            old_sum_support = answer['avg'].get('support', 0)
            answer['avg']['support'] = old_sum_support + class_support

        # calculating weighted average for all functions
        for column in [x.__name__ for x in metrics]:
            col_sum = 0
            for ans_class in [0, 1]:
                row = answer[ans_class]
                col_sum += row[column] * row['support']
            answer['avg'][column] = col_sum / answer['avg']['support']
        print(json.dumps(answer))

    else:
        print(classification_report(ground_answers, model_answers))


if __name__ == '__main__':
    test_model()

from pkspace.utils import loaders


def load_dataset(loader, path, split):
    return loader.load(path, split)

if __name__ == '__main__':
    loader = loaders.PKspaceLoader()
    a, b, c, d = load_dataset(loader, 'labeled_data/2017-01-10', 0.2)
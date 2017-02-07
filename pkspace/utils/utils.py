from pkspace.utils import loaders


def load_dataset(loader, path):
    return loader.load(path)

if __name__ == '__main__':
    # loader = loaders.PKLotLoader()
    # a, b = load_dataset(loader, 'C:\\Users\\rstev\\PycharmProjects\\Rocnikovy\\PKLot\\UFPR04')
    loader = loaders.PKSpaceLoader()
    a, b = load_dataset(loader,
                              'C:\\Users\\rstev\\PycharmProjects\\Rocnikovy\\labeled_data')
    print(a.shape, b.shape)

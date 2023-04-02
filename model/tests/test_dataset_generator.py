import polars as pl

from model.dataset_generator import DatasetGenerator
from model import utils


def create_dfs():
    df1 = pl.DataFrame({'x': range(100), 'y': range(100, 200)})
    df2 = pl.DataFrame({'x': range(200, 300), 'y': range(300, 400)})
    df3 = pl.DataFrame({'x': range(400, 450), 'y': range(450, 500)})

    dfs = [df1, df2, df3]

    return dfs


def test_make_windows():
    dfs = create_dfs()
    train_dfs, val_dfs, test_dfs = utils.split_dfs(dfs, .7, .2)
    dataset_generator = DatasetGenerator(train_dfs, val_dfs, test_dfs)

    dataset_generator.make_windows(5, 5, 1, ['x'])
    
    assert len(dataset_generator.windows) == 3


def test_make_dataset():
    dfs = create_dfs()
    train_dfs, val_dfs, test_dfs = utils.split_dfs(dfs, .7, .2)
    dataset_generator = DatasetGenerator(train_dfs, val_dfs, test_dfs)
    dataset_generator.make_windows(5, 5, 1, ['x'])

    dataset_generator.make_datasets()
    
    assert dataset_generator.train
    assert dataset_generator.val
    assert dataset_generator.test

    # assert len(dataset_generator.train[0][0]) == 65
    # assert len(dataset_generator.train[1][0]) == 65
    # assert len(dataset_generator.train[1][0]) == 30
    # assert len(dataset_generator.train[0])


    # # assert len(dataset_generator.train.take(1)) == 62
    # things = 0
    # for item in dataset_generator.train:
    #     # print(item)
    #     # print(len(item))
    #     for thing in item:
    #         things += len(thing)

    # print(things)



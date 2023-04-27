import polars as pl

from src.dataset_generator import DatasetGenerator
from src import utils


def create_dfs():
    df1 = pl.DataFrame({'x': range(100), 'y': range(100, 200)})
    df2 = pl.DataFrame({'x': range(200, 300), 'y': range(300, 400)})
    df3 = pl.DataFrame({'x': range(400, 450), 'y': range(450, 500)})

    dfs = [df1, df2, df3]

    return dfs

def test_dataset_generator():
    dfs = create_dfs()
    train_dfs, val_dfs, test_dfs = utils.split_dfs(dfs, .7, .2)
    dataset_generator = DatasetGenerator(train_dfs, val_dfs, test_dfs, 5, 6, 1, ['x'])

    assert dataset_generator.train
    assert dataset_generator.val
    assert dataset_generator.test    

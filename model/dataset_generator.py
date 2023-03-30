import os
import polars as pl

from model import utils


class DatasetGenerator():
    def __init__(self, train_percent=.7, val_percent=.2):
        self.train_percent = train_percent
        self.val_percent = val_percent

        self.dfs = []
        self.train_dfs = []
        self.val_dfs = []
        self.test_dfs = []

    def load_data(self):
        filenames = os.listdir(os.path.join("data", "prices"))
        
        for filename in filenames:
            filepath = os.path.join("data", "prices", filename)

            df = pl.read_csv(filepath)

            self.dfs.append(df)

    def setup_data(self):
        for df in self.dfs:
            # drop columns
            df.drop_in_place('Date')

            # split data
            train_df, val_df, test_df = utils.split_train_val_test(df, self.train_percent, self.val_percent)

            # normalize data
            train_mean = train_df.mean()
            train_std = train_df.std()

            train_df = train_df.with_columns([
                (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
            ])

            val_df = val_df.with_columns([
                (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
            ])

            test_df = test_df.with_columns([
                (pl.col(label) - train_mean[label]) / train_std[label] for label in train_mean.columns
            ])

            # store dfs
            self.train_dfs.append(train_df)
            self.val_dfs.append(val_df)
            self.test_dfs.append(test_df)

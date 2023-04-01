import os
import polars as pl

from model import utils
from model.window_generator import WindowGenerator


class DatasetGenerator():
    def __init__(self, train_dfs, val_dfs, test_dfs):
        self.train_dfs = train_dfs
        self.val_dfs = val_dfs
        self.test_dfs = test_dfs

        self.num_dfs = len(train_dfs)

        self.windows = []

    def make_windows(self, input_width, label_width, shift, label_columns):
        for i in range(self.num_dfs):
            window = WindowGenerator(input_width, label_width, shift, label_columns=label_columns, train_df=self.train_dfs[i], val_df=self.val_dfs[i], test_df=self.test_dfs[i])
            
            self.windows.append(window)

    def make_datasets(self):
        # first df
        self.train = self.windows[0].train
        self.val = self.windows[0].val
        self.test = self.windows[0].test

        for i in range(1, self.num_dfs):
            train = self.windows[i].train
            val = self.windows[i].val
            test = self.windows[i].test

            self.train = self.train.concatenate(train)
            self.val = self.val.concatenate(val)
            self.test = self.test.concatenate(test)

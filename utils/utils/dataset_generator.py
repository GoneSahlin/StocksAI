import os
import polars as pl

import utils
from utils.window_generator import WindowGenerator


class DatasetGenerator():
    def __init__(self, train_dfs, val_dfs, test_dfs, input_width, label_width, shift, label_columns):
        self.train_dfs = train_dfs
        self.val_dfs = val_dfs
        self.test_dfs = test_dfs
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.label_columns = label_columns

        self.num_dfs = len(train_dfs)

        self.windows = []

        self._make_windows()
        self._make_datasets()

    def _make_windows(self):
        for i in range(self.num_dfs):
            window = WindowGenerator(self.input_width, self.label_width, self.shift, label_columns=self.label_columns, train_df=self.train_dfs[i], val_df=self.val_dfs[i], test_df=self.test_dfs[i])
            
            self.windows.append(window)

    def _make_datasets(self):
        # first df
        self.train = self.windows[0].train
        self.val = self.windows[0].val
        self.test = self.windows[0].test

        for i in range(1, self.num_dfs):
            train = self.windows[i].train
            val = self.windows[i].val
            test = self.windows[i].test

            self.train = self.train.concatenate(train)

            if val:
                self.val = self.val.concatenate(val)
            
            if test:
                self.test = self.test.concatenate(test)

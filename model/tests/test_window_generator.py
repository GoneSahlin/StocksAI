import pandas as pd

from model.window_generator import WindowGenerator


def create_df():
    df = pd.DataFrame({'x': [0,1,2,3,4], 'y': [5,6,7,8,9]})
    print(df)


def test_init():
    df = create_df()
    # window = WindowGenerator()

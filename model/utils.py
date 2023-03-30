def split_train_val_test(df, train_percent, val_percent):
    n = len(df)
    train_df = df[0:int(n*train_percent)]
    val_df = df[int(n*train_percent):int(n*(train_percent + val_percent))]
    test_df = df[int(n*(train_percent + val_percent)):]

    return train_df, val_df, test_df

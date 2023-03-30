from model.dataset_generator import DatasetGenerator


def test_load_data():
    dataset_generator = DatasetGenerator()

    dataset_generator.load_data()

    assert dataset_generator.dfs


def test_setup_data():
    dataset_generator = DatasetGenerator()
    dataset_generator.load_data()

    dataset_generator.setup_data()

    assert dataset_generator.train_dfs
    assert dataset_generator.val_dfs
    assert dataset_generator.test_dfs

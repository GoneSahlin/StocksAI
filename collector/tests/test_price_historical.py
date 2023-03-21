import price_historical


def test_get_driver():
    driver = price_historical.open_driver()

    assert driver


# def test_get_download_link():
#     driver = p


# def test_get_data():

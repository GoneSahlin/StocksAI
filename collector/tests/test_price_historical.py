import price_historical


def test_get_driver():
    driver = price_historical.open_driver()

    assert driver


def test_get_download_link():
    driver = price_historical.open_driver()

    link = price_historical.get_download_link(driver, 'F')

    print(link)

# def test_get_data():

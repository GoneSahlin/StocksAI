import price_historical


def test_get_driver():
    driver = price_historical.open_driver()

    assert driver

    driver.close()


def test_get_download_link():
    driver = price_historical.open_driver()

    link = price_historical.get_download_link(driver, 'F')

    driver.close()

    correct_link_start = "https://query1.finance.yahoo.com/v7/finance/download/F"

    assert link[:len(correct_link_start)] == correct_link_start


# def test_get_data():

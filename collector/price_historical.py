from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import requests
import polars as pl
from io import StringIO


def open_driver() -> webdriver.Firefox:
    # path to geckodriver and firefox
    driver_path = R"/usr/local/bin/geckodriver"    
    firefox_path = R"/bin/firefox"    

    # create options and service
    options = Options()
    options.binary_location = firefox_path
    options.add_argument("-headless")
    service = Service(executable_path=driver_path)

    # create a driver
    driver = webdriver.Firefox(options=options, service=service)

    # return driver
    return driver


def get_download_link(driver: webdriver.Firefox, ticker):
    # url
    url = "https://finance.yahoo.com/quote/" + ticker + "/history"

    # open page
    driver.get(url)

    # wait for page to load
    driver.implicitly_wait(1)

    # close pop-up if it occurs
    try:
        close = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
        close.click()
    except:
        pass

    # click on dropdown
    dropdown = driver.find_element(By.XPATH, "//div[@role='button'][@aria-label='']")
    dropdown.click()

    # click on max
    max = driver.find_element(By.XPATH, "//button[@data-value='MAX']")
    max.click()

    # click on apply
    apply = driver.find_element(By.XPATH, "//span[text()='Apply']/parent::*")
    apply.click()

    # click on download
    download = driver.find_element(By.XPATH, "//a[@download='" + ticker + ".csv']")
    link = download.get_attribute("href")

    return link


def get_data(link):
    try:
        response = requests.get(link, headers={'User-agent': 'Mozilla/5.0'})
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(e.response.text)
        

def clean_data(data: str) -> pl.DataFrame:
    df = pl.read_csv(StringIO(data))
    df = df.drop(["Open","High","Low","Close"])

    return df


def save_to_csv(ticker, df: pl.DataFrame):
    filepath = "../data/" + ticker + ".csv"
    
    df.write_csv(filepath)


def save_to_parquet(ticker, df: pl.DataFrame):
    filepath = "../data/" + ticker + "_prices.parquet"

    df.write_parquet(filepath)


def main():
    driver = open_driver()

    link = get_download_link(driver, "F")
    # get_download(driver, "AAPL")

    driver.close()

    data = get_data(link)
    data = clean_data(data)
    save_to_parquet("F", data)


if __name__ == "__main__":
    main()

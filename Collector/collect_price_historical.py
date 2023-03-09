from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import shutil
import time


def open_driver():
    # install geckodriver
    # path to geckodriver
    driver_path = R"/usr/local/bin/geckodriver"    

    # path to firefox executable
    firefox_path = R"/bin/firefox"    

    # create options
    options = Options()
    
    # set binary location
    options.binary_location = firefox_path    

    # create a service object and set executable_path to driver_path
    service = Service(executable_path=driver_path)

    # create a driver
    driver = webdriver.Firefox(options=options, service=service)

    # return driver
    return driver


def get_download(driver, ticker):
    # url
    url = "https://finance.yahoo.com/quote/" + ticker + "/history"

    # open page
    driver.get(url)

    # wait for page to load
    time.sleep(2)

    # close pop-up if it occurs
    try:
        close = driver.find_element(By.XPATH, "//button[@aria-label='Close']")
        close.click()
    except:
        pass

    # click on dropdown
    dropdown = driver.find_elements(By.XPATH, "//div[@role='button'][@aria-label='']")[1]
    dropdown.click()

    # click on max
    max = driver.find_element(By.XPATH, "//button[@data-value='MAX']")
    max.click()

    # click on apply
    apply = driver.find_element(By.XPATH, "//span[text()='Apply']")
    apply.click()

    # click on download
    download = driver.find_element(By.XPATH, "//a[@download='" + ticker + ".csv']")
    download.click()

    # move download
    time.sleep(4)
    src = r"/home/zach/Downloads/" + ticker + ".csv"
    dst = r"downloads"
    shutil.move(src, dst)


def main():
    driver = open_driver()

    get_download(driver, "F")
    get_download(driver, "AAPL")

    # close the driver
    driver.close()


if __name__ == "__main__":
    main()

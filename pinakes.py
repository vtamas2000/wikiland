from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import networkx as nx
import numpy as np
from graph import SuperGraph, NGraph
from utils import process_text


def main() -> None:
    driver_PATH = './chromedriver'
    brave_PATH = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    option = webdriver.ChromeOptions()
    option.binary_location = brave_PATH
    browser = webdriver.Chrome(executable_path=driver_PATH, options=option)

    browser.get('https://en.wikipedia.org/wiki/Lockheed_Hudson')

    body = browser.find_element(By.ID, 'mw-content-text').text

    print(process_text(body))


if __name__ == '__main__':
    main()
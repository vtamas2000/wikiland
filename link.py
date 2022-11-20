from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import os
import argparse

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number_of_next_pages', type=int, required=True, 
                        help='How many next pages you would like to go over')
    args = parser.parse_args()
    return args

def main() -> None:
    args = get_args()

    driver_PATH = './chromedriver'
    brave_PATH = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    option = webdriver.ChromeOptions()
    option.binary_location = brave_PATH
    browser = webdriver.Chrome(executable_path=driver_PATH, options=option)

    if len(os.listdir('data/branches')) == 0:
        browser.get('https://en.wikipedia.org/wiki/Special:AllPages/A')
        filenumbers = ['-1.pkl']
    else:
        filenumbers =[]
        for file in os.listdir('data/branches'):
            filenumbers.append(file.split('_')[1])
        load = open(f'data/branches/branch_{max(filenumbers)}', 'rb')
        start_page = pickle.load(load)[1]
        browser.get(start_page)
        print(f'Start at {start_page}')
    end_link = ''
    list_of_links = []
    for i in range(args.number_of_next_pages):
        link_objects = browser.find_elements(By.CLASS_NAME, 'mw-redirect')
        for link in link_objects:
            list_of_links.append(link.get_attribute('href'))

        next_page = browser.find_element(By.XPATH, '//div[@class="mw-allpages-nav"]/a[2]')
        if i == args.number_of_next_pages - 1:
            end_link = next_page.get_attribute('href')
        
        print(f'{len(link_objects)} links have been added for the {i}/{args.number_of_next_pages} page\n\n')
        print(next_page.get_attribute('href'))
        next_page.click()

    print(f'Ended at link {end_link}')
    print(f'Total of {len(list_of_links)} links have been added')
    file = open(f'data/branches/branch_{int(max(filenumbers).split(".")[0]) + 1}.pkl', 'wb')
    pickle.dump([list_of_links, end_link], file)
    

if __name__ == '__main__':
    main()
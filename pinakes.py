from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import networkx as nx
import numpy as np
from graph import SuperGraph, NGraph
from utils import process_text
from concurrent.futures import as_completed, ThreadPoolExecutor, ProcessPoolExecutor
from typing import List
from bs4 import BeautifulSoup
import requests
import time

# def get_page(url: str, exec_path: str, options: webdriver.ChromeOptions) -> List[str]:
#     browser = webdriver.Chrome(executable_path=exec_path, options=options)

#     browser.get(url)
#     body = browser.find_element(By.ID, 'mw-content-text').text
#     return process_text(body)


def get_text_from_url(url: str) -> str:
    return requests.get(url).text

def add_to_network(network: SuperGraph, urls: List[str]) -> SuperGraph:
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_htmls = [executor.submit(get_text_from_url, url) for url in urls]

        for future_html in as_completed(future_htmls):
            soup = BeautifulSoup(future_html.result(), 'html.parser')
            target = soup.find(id="mw-content-text")
            texts = target.find_all('p')
            all_texts = ''.join([text.get_text() + ' ' for text in texts])
            network.add_article(process_text(all_texts))

    return network


def main() -> None:

    file = open('data/branches/branch_0.pkl', 'rb')
    urls = pickle.load(file)[0]
    urls = urls[:500]

    max_processes = 6
    url_list = [list(url) for url in (np.array_split(urls, max_processes))]

    graphs = [SuperGraph(10) for _ in range(max_processes)]
    processed_graphs = []

    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_processes) as process_exec:
        future_graphs = [process_exec.submit(add_to_network, graph, url) for graph, url in zip(graphs, url_list)]
        for future_graph in as_completed(future_graphs):
            processed_graphs.append(future_graph.result())

    end = time.perf_counter()

    print(f'With Multiprocessing {end - start}')

    for graph in processed_graphs:
        print(graph)


    # pinakes = SuperGraph(max_distance=2)

    # start = time.perf_counter()
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     future_htmls = [executor.submit(get_text_from_url, url) for url in urls]

    #     for future_html in as_completed(future_htmls):
    #         soup = BeautifulSoup(future_html.result(), 'html.parser')
    #         target = soup.find(id="mw-content-text")
    #         texts = target.find_all('p')
    #         all_texts = ''.join([text.get_text() + ' ' for text in texts])
    #         pinakes.add_article(process_text(all_texts))
    
    # end = time.perf_counter()
    # print(pinakes)

    # print(f'With multithreading {end - start}')


    # start = time.perf_counter()
    # for url in urls:
    #     soup = BeautifulSoup(get_text_from_url(url), 'html.parser')
    #     target = soup.find(id="mw-content-text")
    #     texts = target.find_all('p')
    #     all_texts = ''.join([text.get_text() + ' ' for text in texts])
    #     a = process_text(all_texts)

    # end = time.perf_counter()

    # print(f'Without multithreading {end - start}')

    # html = requests.get('https://en.wikipedia.org/wiki/Autov%C3%ADa_A-62').text

    # soup = BeautifulSoup(html, 'html.parser')
    # target = soup.find(id="mw-content-text")
    # texts = target.find_all('p')
    # all_texts = ''.join([text.get_text() + ' ' for text in texts])
    
    
    # print(process_text(all_texts))
    


    # driver_PATH = './chromedriver'
    # brave_PATH = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    # option = webdriver.ChromeOptions()
    # option.binary_location = brave_PATH

    # file = open('data/branches/branch_0.pkl', 'rb')
    # urls = pickle.load(file)[0]
    
    # browser = webdriver.Chrome(executable_path=driver_PATH, options=option)
    # browser.get(urls[0])
    # body = browser.find_element(By.ID, 'mw-content-text').text
    # # print(body)
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     future_processed_texts = [executor.submit(get_page, url, driver_PATH, option) for url in urls]

    #     for processed_text in as_completed(future_processed_texts):
    #         try:
    #             print(processed_text.result())
    #         except KeyboardInterrupt:
    #             processed_text.cancel()

    # browser.get('https://en.wikipedia.org/wiki/Lockheed_Hudson')

    # body = browser.find_element(By.ID, 'mw-content-text').text

    # print(get_page(browser, 'https://en.wikipedia.org/wiki/Lockheed_Hudson'))


if __name__ == '__main__':
    main()
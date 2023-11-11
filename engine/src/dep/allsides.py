from browser.Selenium import Browser
from selenium.webdriver.common.by import By
import constants
from time import sleep
import os
import pandas as pd
import pickle as pkl

def loadBrowser():

    path = constants.SESSIONS_PATH
    if not os.path.exists(f'{path}mbfc'):
        os.mkdir(f'{path}mbfc')

    id = 'temp'

    if not os.path.exists(f'{path}mbfc/{id}'):
        print('Not logged in')
        os.mkdir(f'{path}mbfc/{id}')

    # TODO change this to the new way
    session = f'mbfc/{id}'

    browser = Browser(session)
    driver = browser.getDriver()
    return driver


driver = loadBrowser()
pages = pd.read_pickle('urls-allsides')
result = pd.read_pickle('pages-allsides')
# result = dict()


i = 0
for web in pages:
    print(web)
    web = pages[web]
    if web == '':
        print('No page found')
        continue

    if web in result:
        continue

    print(web)
    driver.get(web)

    try:
        page = driver.find_element(By.XPATH, '//div[@class="source-page-top"]')
        page = page.text
        result[web] = page

    except:
        try:
            h1 = driver.find_element(By.XPATH, '//h1[@class="page-title"]')
            result[web] = h1.text
        except:
            print('No page found')
            result[web] = ''
            continue

    sleep(5)
    i += 1 

    pkl.dump(result, open('pages-allsides', 'wb'))

    if i % 10 == 0:
        pkl.dump(result, open('pages-allsides', 'wb'))
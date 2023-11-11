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


# load webpage with selenium driver

driver = loadBrowser()

pages = pd.read_pickle('missed-mbfc')
# result = pd.read_pickle('pages-mbfc')

result = dict()

i = 0
for web in pages:
    web = pages[web]
    if web == '':
        print('No page found')
        continue

    if web in result:
        continue

    print(web)
    driver.get(web)
    sleep(2.5)
    try:
        title = driver.find_element(By.XPATH, '//header[@class="entry-header"]')
        print(title.text)
        content = driver.find_elements(By.XPATH, '//div[@id="main-content"]')
        print(len(content))
        page = title.text + '--'
        for c in content:
            if 'Detailed Report' in c.text:
                page = title.text + '--' + c.text
        
        result[web] = page
        if 'Detailed Report' in page:
            print('DONE -----------------------------')

    except:
        print('No page found')
        try:
            h1 = driver.find_element(By.XPATH, '//h1[@class="page-title"]')
        except:
            print('No page found')
            result[web] = ''
            continue

    i += 1 
    print('\n \n \n \n')

    pkl.dump(result, open('missed-pages-mbfc', 'wb'))


    if i % 10 == 0:
        pass
        # pkl.dump(result, open('pages-mbfc10', 'wb'))
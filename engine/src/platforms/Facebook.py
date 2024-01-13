import sys

from utils.util import convertStringToNumber; sys.path.append('..')
from platforms.Platform import Platform
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import *
from time import sleep
import constants
from datetime import datetime
import utils.monkey as monkey
import constants
import pickle as pkl

class Facebook(Platform):
    name = 'facebook'
    url='https://www.facebook.com'
    search_url='https://www.facebook.com/search/pages/?q=%s'
    creation_url='https://www.facebook.com/reg'

    def __init__(self, userId):
        super().__init__(Facebook.name, Facebook.url, userId)

    def createUser(self, info):
        self.loadPage(Facebook.creation_url)
        sleep(3)
        monkey.click()
        monkey.next()
        monkey.type(info["firstname"])
        monkey.next()
        monkey.type(info["lastname"])
        monkey.next()
        monkey.type(info["email"])
        monkey.next()
        monkey.type(info["email"])
        monkey.next()
        monkey.type(info["password"])
        monkey.next()
        monkey.type(info["DOB"].split(',')[0])
        monkey.next()
        monkey.type(info["DOB"].split(',')[1])
        monkey.next()
        monkey.type(info["DOB"].split(',')[2])
        monkey.next()
        monkey.next()

        if info["gender"] == 'F':
            monkey.press('space')
        else:
            monkey.press('right')

        input("WAITING")

        sleep(4)
        return True

    def joinCommunity(self):
        
        sleep(1)
        communities = self.driver.find_elements(By.XPATH, '//span[text()="Groups"]')

        sleep(2)
        for c in communities:
            try:
                c.click()
            except:
                pass
            sleep(1)

        debug('Clicked group putton')

        group = self._joinFromResults()

        return group

    def loggedIn(self):
        try:
            self.driver.find_elements(By.XPATH, '//span[text()="Groups"]')
            return True
        except:
            return False

    def getHomePage(self):
        sleep(1)
        home = self.driver.find_element(By.XPATH, '//a[@aria-label="Facebook"]')
        home.click()

    def _searchTermUrl(self, term):
        search_query = Facebook.search_url % (term)
        self.loadPage(search_query)

    def _searchTermBar(self, term):
        search_bar = self._getSearchBar()
        search_bar.send_keys(term)
        sleep(3)
        search_bar.send_keys(Keys.ENTER)

    def _getSearchBar(self):
        return self.driver.find_element(By.XPATH, "//input[@placeholder='Search Facebook']")
        
    def isJoinable(self, group):
        button = group.find_elements(By.XPATH, './/span[text()="Join"]')
        if len(button) == 0:
            debug('Already joined - Continue')
            return False
        else:
            if 'Public' in group.text:
                return True
            else:
                debug('Private Group - Continue')
                return False

    def _joinFromResults(self):

        results = self.driver.find_elements(By.XPATH, "//div[@style='border-radius: max(0px, min(8px, ((100vw - 4px) - 100%) * 9999)) / 8px;']")       
        debug(f'RESULTS: {len(results)}')

        i = 0
        for result in results: 

            i += 1

            lines = result.text.split('\n')

            info = result.find_element(By.XPATH, './/a[@role="presentation"]')
            name = info.text
            group_id = info.get_attribute('href')

            members = lines[1].split('·')[1]
            members = members.replace(' members', '')
            members = convertStringToNumber(members)

            description = lines[2]

            group_info = {'name': name, 'group_id': group_id, 'members': members, 'description': description, 'position': i}

            if not self.isJoinable(result):
                continue

            join_button = result.find_element(By.XPATH, './/span[text()="Join"]')
            join_button.click()

            debug('Joined')
            group_info['Joined'] = True
            input('WAITING')
            return group_info

        return None


    def _getPeopleResults(self):
        sleep(3)
        page = self.driver.find_element(By.XPATH, '//div[@aria-label="Search results"]')
        results = page.find_elements(By.XPATH, '//a[@role="presentation"]')
        possible_buttons = page.find_elements(By.XPATH, '//div[@role="button"]')
        buttons = []

        for b in possible_buttons:
            if len(b.text) > 2:
                buttons.append(b)

        people = [{'name':r.text, 'action': b.text, 'button': b} for r, b in zip(results, buttons)]

        return people

    def _joinNthUser(self, people, N=0):
        sleep(3)
        i = 0
        debug(people)
        for p in people:
            debug(p['action'])
            if p['action'] == 'Add friend':
                if i == N:
                    p['button'].click()
                    return p['name']
                else:
                    i += 1
        raise Exception('No more people to add')

    def followUser(self):
        sleep(1)
        people = self.driver.find_elements(By.XPATH, '//span[text()="People"]')[0]
        # people = self.driver.find_element(By.XPATH, '//button[text()="People"]')
        people.click()
        sleep(2)
        results = self._getPeopleResults()
        user = self._joinNthUser(results)
        return user
        # return community

    def _processPost(self, text):
            text = text.replace('\n', ' - ')
            text = text.split('·')
            print(text)

            post = dict()
            if 'Suggested for you' in text[0]:
                post['suggested'] = True
                post['name'] = text[0].split('-')[1]
            else:
                post['suggested'] = False
                post['name']= text[0].split('-')[0]

            print(post)
            return

    def getPagePosts(self, n=10):
        feed = self.driver.find_element(By.XPATH, '//div[@role="feed"]')
        
        posts = feed.find_elements(By.XPATH, '//div[@role="article"]')

        j = 0
        for post in posts:
            print(f'POST {j}')
            # texts = post.find_elements(By.XPATH, './/span[@dir="auto"]')
            # print(post.text)
            text = post.text
            self._processPost(text)
            j+=1
            # if type(texts) == list:
            #     for i, text in enumerate(texts):
            #         debug(f'{i}: {text.text}')
            # else:
            #     debug(f'0: {texts.text}')
            
        input()

        error('Not implemented: Facebook.getPagePosts()')
        pass
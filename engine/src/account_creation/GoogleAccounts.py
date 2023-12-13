import sys
sys.path.append('..')
from browser.Selenium import Browser
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.log import debug
from utils.util import wait; 
import utils.monkey as monkey

class GoogleAccount():
    def __init__(self, email, firstName, lastName, password, sms):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.sms = sms
        self.id = email.split('@')[0]

    def loadBrowser(self):
        session = f'{self.id}'
        browser = Browser(session)
        driver = browser.getDriver()
        wait(2)
        monkey.next()
        wait(1)
        monkey.space()
        return driver

    def create(self):
        driver = self.loadBrowser()
        driver.get('https://accounts.google.com/signin')
        wait(2)
        return
        monkey.type(self.email)
        wait(1)
        monkey.enter()
        wait(2)
        monkey.type(self.password)
        wait(1)
        monkey.enter()


        # get url of the page
        wait(2)
        url = driver.current_url
        debug(url)
        if 'speedbump' in url:
            btn = driver.find_element(By.XPATH, "//input[@name='confirm']")
            btn.click()

            wait(2)
            return

        input('CHECK PHONE NUMBER???')
        

        area, phone_number = self.sms.get_number()

        debug(area)
        debug(phone_number)

        wait(3)
        
        if area == 'USA':
            pass
        elif area == 'NL':
            for i in range(4):
                monkey.back()
                wait(0.2)
                monkey.type('n')

        elif area == 'UK':
            for i in range(5):
                monkey.back()
                wait(0.2)
                monkey.type('u')

        monkey.type(phone_number)
        wait(1)
        monkey.enter()

        wait(5)

        code = self.sms.get_code()
        while code == -1:
            wait(2)
            code = self.sms.get_code()
        
        monkey.type(code)
        wait(1)
        monkey.enter()

        input()




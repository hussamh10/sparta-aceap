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
        self.driver = browser.getDriver()

    def phoneNumberIncorrect(self):
        # get all text from spans 
        wait(3)
        spans = self.driver.find_elements(By.XPATH, "//span")
        for span in spans:
            if 'provide a phone number' in span.text.lower():
                debug("Error page")
                return True
            
        return False

    def input_number(self):
        area, phone_number = self.sms.get_number()

        wait(3)
        
        if area == 'USA':
            monkey.type("+1")
            monkey.type(phone_number)
        elif area == 'NL':
            monkey.type("+31")
            monkey.type(phone_number)
        elif area == 'UK':
            monkey.type("+44")
            monkey.type(phone_number)

        wait(1)
        monkey.enter()

        return
        
    def yellowSMSpage(self):
        failed = True
        while failed:
            debug('TRYING YELLOWPAGE')
            area, phone_number = self.sms.get_number()
            area_names = {'USA': 'united states', 'NL': 'netherlands', 'UK': 'united kingdom'}

            wait(1)
            monkey.back()
            wait(1)
            monkey.type(area_names[area])
            wait(1)
            monkey.next()
            wait(1)
            monkey.type(phone_number)
            wait(1)
            monkey.enter()
            wait(2)
            hasError = self.driver.find_elements(By.XPATH, "//span[@id='error']")
            if len(hasError) > 0:
                debug('Error page')
                failed = True
            else:
                failed = False

    def phoneNumberPage(self):
        h1 = self.driver.find_element(By.XPATH, "//h1").text

        if 'Verify' in h1:
            debug('Verify')
            self.yellowSMSpage()
            debug('GOT NUMBER')
            wait(4)
            inputs = self.driver.find_elements(By.XPATH, "//input[@id='smsUserPin']")
            if len(inputs) > 0:
                debug('WAITING FOR CODE')
                code = self.sms.get_code()
                while code == -1:
                    wait(2)
                    code = self.sms.get_code()
                inputs[0].click()
                wait(1)
                monkey.type(code)
                wait(1)
                monkey.enter()
                wait(3)
                btn = self.driver.find_element(By.XPATH, "//input[@name='confirm']")
                btn.click()
                wait(3)
            


    def create(self):
        self.loadBrowser()
        self.driver.get('https://accounts.google.com/signin')


        debug('waiting for signin')
        wait(2)
        monkey.click()
        wait(1)

        if 'myaccount.google.com' in self.driver.current_url:
            debug('Signed In')
            return

        email = self.driver.find_element(By.XPATH, "//input[@id='identifierId']")
        email.click()

        wait(1)

        monkey.type(self.email)
        wait(1)
        monkey.enter()
        wait(2)
        monkey.type(self.password)
        wait(1)
        monkey.enter()


        # get url of the page
        wait(2)
        url = self.driver.current_url
        debug(url)
        if 'myaccount.google.com' in url:
            debug('Signed In')
            return


        self.phoneNumberPage()
        wait(2)

        url = self.driver.current_url

        if 'myaccount.google.com' in url:
            debug('Signed In')
            return

        return
    
    def checkChromeSignedIn(self):
        self.loadBrowser()
        self.driver.get('https://accounts.google.com/signin')
        wait(2)
        if 'myaccount.google.com' in self.driver.current_url:
            signed = True
        else:
            signed = False

        wait(2)
        self.driver.quit()
        return signed
        

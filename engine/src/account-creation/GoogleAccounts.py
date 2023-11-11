import sys
sys.path.append('..')
from browser.Selenium import Browser
from utils.log import debug
from utils.util import wait; 
import utils.monkey as monkey
from JuicySMS import juicy

class GoogleAccount():
    def __init__(self, email, firstName, lastName, password, sms):
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.sms = sms

    def loadBrowser(self):
        session = 'new_account/'
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
        monkey.type(self.email)
        wait(1)
        monkey.enter()
        wait(2)
        monkey.type(self.password)
        wait(1)
        monkey.enter()

        # get url of the page
        url = driver.current_url
        if 'challenge' not in url:
            raise Exception('Did not get phone verification')
        

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




sms = juicy()
account = GoogleAccount('aceapxp001@spartaaceap.com', 'Anthony', 'Banthony', 'hehehahahoho', sms)
account.create()
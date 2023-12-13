import sys
sys.path.append('../src')
from utils.util import wait

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from account_creation.ChromeSignIns import createProflie, checkProflies, loadBrowser


email = 'aceap0003@gmail.com'
userId = 'googlesnew44'
password = 'hehehahahoho'

driver = loadBrowser(userId)
wait(1)
driver.get('https://www.twitter.com')

# click on button with id='continue-as'

input()
btn = driver.find_element(By.XPATH, '//div[@id="credential_picker_container"]')
btn.click()


btn = driver.find_element(By.XPATH, '//button[@id="continue-as"]')
btn.click()

input()
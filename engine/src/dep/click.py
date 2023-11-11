from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


#browser exposes an executable file
#Through Selenium test we will invoke the executable file which will then
#invoke actual browser
service = Service(ChromeDriverManager().install())
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
#get method to launch the URL
driver.get("https://www.tutorialspoint.com/about/about_careers.htm")
#to refresh the browser
driver.refresh()
# identifying the source element
sleep(3)
action = ActionChains(driver)
action.move_by_offset(12, 31)
sleep(3)
source= driver.find_element_by_xpath("//*[text()='Company']");
print(source.text)
action.move_to_element(source)
print('done')
sleep(10)
#to close the browser
driver.close()
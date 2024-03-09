from browser.Selenium import Browser
from time import sleep


b = Browser('dumptest')
d = b.getDriver()
d.get('https://www.x.com')

# get page source with lazy loading
for i in range(10):
    d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)
    page = d.page_source
    open(f'page{i}.html', 'w', encoding='utf8').write(page)

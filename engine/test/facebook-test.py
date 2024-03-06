import sys
sys.path.append('../src')
from utils.util import wait
from utils.shuffleIP import shuffle as shuffleIP
from platforms.Facebook import Facebook

shuffleIP()
info = {'firstname': 'ahmed', 'lastname': 'javed', 'email': 'spartaaceap+1@gmail.com', 'password': 'hehehahahoho', 'DOB': 'feb,12,1994', 'gender': 'M'}
user = Facebook('3')
user.loadBrowser()
# user.createUser(info)
user.loadWebsite()
input()
user.loadPage('https://www.bing.com/search?pglt=41&q=take+full+page+screenshot+chromedriver&cvid=2a8ae8eb3a634f878e4052d9472f701b&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQABhAMgYIAhAAGEAyBggDEAAYQDIGCAQQABhAMgYIBRAAGEAyBggGEAAYQDIGCAcQABhAMgYICBAAGEDSAQg5ODE3ajBqMagCALACAA&FORM=ANSPA1&PC=U531')
wait(5)
user.screenshot('abc.png')
input()
user.searchTerm('oscars')
wait(2)
user.likePost()

input()
import sys
sys.path.append('../src')
from utils.util import wait
from platforms.Facebook import Facebook

info = {'firstname': 'ahmed', 'lastname': 'javed', 'email': 'spartaaceap+2@gmail.com', 'password': 'hehehahahoho', 'DOB': 'feb,12,1994', 'gender': 'M'}
user = Facebook('2')
user.loadBrowser()
user.createUser(info)
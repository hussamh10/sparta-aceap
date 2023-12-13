import sys
sys.path.append('../src')
from utils.util import wait
from utils.log import debug
import names
import pandas as pd
import account_creation.database as DB
from account_creation.createGoogleAccounts import create_account
import json

class GoogleProfile:
    def __init__(self, fname, lname, email, id, xp):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.id = id
        self.xp = xp
        self.google_signin = False
        self.chrome_signin = False
        self.chrome_session = None

    def create_line(self):
        temp = '%s,%s,%s,hehehahahoho,,/,,sparta.aceap@gmail.com,,,,,,,,,aceap000,,,,,,,,,False,,False'
        return temp % (self.fname, self.lname, self.email)
    
    def create_dict(self):
        return {
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'id': self.id,
            'xp': self.xp,
            'google_signin': self.google_signin,
            'chrome_signin': self.chrome_signin,
            'chrome_session': self.chrome_session
        }
    
# ===============================

def create_user_csv(N, email_template, experiment_id):
    header = 'First Name [Required],Last Name [Required],Email Address [Required],Password [Required],Password Hash Function [UPLOAD ONLY],Org Unit Path [Required],New Primary Email [UPLOAD ONLY],Recovery Email,Home Secondary Email,Work Secondary Email,Recovery Phone [MUST BE IN THE E.164 FORMAT],Work Phone,Home Phone,Mobile Phone,Work Address,Home Address,Employee ID,Employee Type,Employee Title,Manager Email,Department,Cost Center,Building ID,Floor Name,Floor Section,Change Password at Next Sign-In,New Status [UPLOAD ONLY],Advanced Protection Program enrollment'
    users = []
    for i in range(total_users):
        eid = f"{email_template}{i}"
        user = GoogleProfile(names.get_first_name(), names.get_last_name(), f"{eid}@spartaaceap.com", eid, experiment_id)
        users.append(user)

    lines = []
    for user in users:
        line = user.create_line()
        lines.append(line)
    
    with open('google_users_temp.csv', 'w') as f:
        f.write('\n'.join([header] + lines))

    DB.add_google_accounts(users)

    return users


def create_users_google(users):
    for user in users:
        print(user.email)
        create_account(user)
        DB.update_google_signin(user)
    return
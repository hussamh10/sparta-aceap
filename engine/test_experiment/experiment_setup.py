import sys
sys.path.append('../src')
from utils.util import wait
from utils.log import debug
import names
import pandas as pd
import account_creation.database as DB
from account_creation.dep.createGoogleAccounts import create_account
import json
import utils.shuffleIP as IP

class GoogleProfile:
    def __init__(self, fname, lname, email, id, xp):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.id = id
        self.xp = xp
        self.google_account_setup = False
        self.google_signin = False
        self.chrome_signin = False
        self.chrome_session = None

    def create_line(self):
        temp = '%s,%s,%s,hehehahahoho,,/,,sparta.aceap@gmail.com,,,,,,,,,aceap000,,,,,,,,,False,,False'
        return temp % (self.fname, self.lname, self.email)
    
    def account_is_setup(self):
        self.google_account_setup = True
    
    def create_dict(self):
        return {
            'fname': self.fname,
            'lname': self.lname,
            'email': self.email,
            'id': self.id,
            'xp': self.xp,
            'google_account_setup': self.google_signin,
            'google_signin': self.google_signin,
            'chrome_signin': self.chrome_signin,
            'chrome_session': self.chrome_session
        }
    
# ===============================

def create_user_csv(N, email_template, experiment_id):
    header = 'First Name [Required],Last Name [Required],Email Address [Required],Password [Required],Password Hash Function [UPLOAD ONLY],Org Unit Path [Required],New Primary Email [UPLOAD ONLY],Recovery Email,Home Secondary Email,Work Secondary Email,Recovery Phone [MUST BE IN THE E.164 FORMAT],Work Phone,Home Phone,Mobile Phone,Work Address,Home Address,Employee ID,Employee Type,Employee Title,Manager Email,Department,Cost Center,Building ID,Floor Name,Floor Section,Change Password at Next Sign-In,New Status [UPLOAD ONLY],Advanced Protection Program enrollment'
    users = []
    for i in range(N):
        eid = f"{email_template}{i}"
        user = GoogleProfile(names.get_first_name(), names.get_last_name(), f"{eid}@spartaaceap.com", eid, experiment_id)
        users.append(user)

    lines = []
    for user in users:
        line = user.create_line()
        lines.append(line)
    
    csv_name = 'temp.csv'
    with open(csv_name, 'w') as f:
        f.write('\n'.join([header] + lines))

    return users

def create_users_google(users, db):
    for user in users:
        if db.google_signed_in(user):
            debug(f"SIGNED IN: {user}")
            continue
        debug(f"SIGNING IN: {user}")
        create_account(users[user])
        db.update_google_signin(user)
        IP.shuffle()
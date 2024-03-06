import sqlite3 as sql
from constants import *
import names
from account_creation.JuicySMS import juicy
from account_creation.GoogleAccounts import GoogleAccount
from utils import shuffleIP as IP
import pandas as pd

from utils.log import debug, error
from utils.util import wait, bigWait

class GoogleWorkspace():
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, 'google.db')
        pass

    def needUsers(self, config):
        num_users = len(config['treatments']) * config['replication']
        experiment_id = config['experiment_id']
        query = f'SELECT * FROM users WHERE exp="{experiment_id}" AND chrome_signin=1'
        # remove any rows from database where chrome_signin is NULL
        db = sql.connect(self.db_path)
        

        df = pd.read_sql(query, sql.connect(self.db_path))
        users = list(list(df.to_dict('records')))
        debug(f"Users required: {num_users}")
        if len(users) >= num_users:
            debug(f"Enough users already created: {users}")
            return False
        if len(users) == 0:
            debug(f"No users created yet")
            return True
        if len(users) < num_users:
            error(f"Not enough users created: {users}")
            return True
        
    def createUsers(self, config):
        csv_path = os.path.join(config['path'], 'google_users.csv')
        num_users = len(config['treatments']) * config['replication']
        i = input("Are users uploaded to Google Admin? (y/n) ")
        if i == 'n':
            debug("Users not uploaded to Google Admin yet")
            users = self.signUp(num_users, config['email_template'], config['experiment_id'], csv_path)
            input("*** Upload CSV to Google Admin and press enter to continue... ***")
            self.usersUploaded(users)
        else:
            debug("Users uploaded to Google Admin already")
            users = self.get_users(config['experiment_id'])

        self.chromeSignInAll(users)

        debug("Users created and chromed signed in")

    def userPlatformSigned(self, email, platform):
        db = sql.connect(self.db_path)
        query = f'UPDATE users SET {platform}=1 WHERE email="{email}"'
        db.execute(query)
        db.commit()
        db.close()

    def userAssigned(self, email, platform):
        db = sql.connect(self.db_path)
        query = f'UPDATE users SET {platform}=1 WHERE email="{email}"'
        db.execute(query)
        db.commit()
        db.close()

    def HasUsers(self, platform, experiment_id):
        platform = platform.lower()
        query = f'SELECT * FROM users WHERE exp="{experiment_id}" AND {platform} is NULL AND chrome_signin=1'
        df = pd.read_sql(query, sql.connect(self.db_path))
        users = list(df.to_dict('records'))
        return len(users) > 0
        
    def createUserLine(self, user):
        temp = '%s,%s,%s,hehehahahoho,,/,,sparta.aceap@gmail.com,,,,,,,,,aceap000,,,,,,,,,False,,False'
        return temp % (user['fname'], user['lname'], user['email'])

    def createUser(self, eid, experiment_id):
        user = dict()
        user['fname'] = names.get_first_name()
        user['lname'] = names.get_last_name()
        user['email'] = f"{eid}@spartaaceap.com"
        user['id'] = eid
        user['exp'] = experiment_id
        user['google_account_setup'] = False
        user['google_signin'] = False
        user['chrome_signin'] = False
        user['chrome_session'] = None
        user['reddit'] = 0
        user['twitter'] = 0
        user['youtube'] = 0
        user['tiktok'] = 0
        return user
        
    def get_users(self, experiment_id):
        query = f'SELECT * FROM users where exp="{experiment_id}"'
        users = pd.read_sql(query, sql.connect(self.db_path))
        users = users.to_dict('records')
        return users

        
    def signUp(self, N, email_template, experiment_id, path):
        header = 'First Name [Required],Last Name [Required],Email Address [Required],Password [Required],Password Hash Function [UPLOAD ONLY],Org Unit Path [Required],New Primary Email [UPLOAD ONLY],Recovery Email,Home Secondary Email,Work Secondary Email,Recovery Phone [MUST BE IN THE E.164 FORMAT],Work Phone,Home Phone,Mobile Phone,Work Address,Home Address,Employee ID,Employee Type,Employee Title,Manager Email,Department,Cost Center,Building ID,Floor Name,Floor Section,Change Password at Next Sign-In,New Status [UPLOAD ONLY],Advanced Protection Program enrollment'
        users = []
        for i in range(N):
            eid = f"{email_template}{i}"
            user = self.createUser(eid, experiment_id)
            users.append(user)

        lines = []
        for user in users:
            line = self.createUserLine(user)
            lines.append(line)
        
        with open(path, 'w') as f:
            f.write('\n'.join([header] + lines))

        return users

    def usersUploaded(self, users):
        db = sql.connect(self.db_path)
        for user in users:
            query = f'INSERT INTO users (fname, lname, email, id, exp, google_signin, chrome_signin, chrome_session, reddit, twitter, youtube, tiktok, facebook) VALUES ("{user["fname"]}", "{user["lname"]}", "{user["email"]}", "{user["id"]}", "{user["exp"]}", NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)'
            db.execute(query)
        db.commit()
        db.close()

    def checkChromeSignedIn(self, email):
        query = f'SELECT * FROM users WHERE email="{email}"'
        users = pd.read_sql(query, sql.connect(self.db_path))
        users = users.to_dict('records')
        user = users[0]
        email = user['email']
        fname = user['fname']
        lname = user['lname']
        id = user['id']
        password = 'hehehahahoho'

        GA = GoogleAccount(email, fname, lname, password, None)
        isSignedIn = GA.checkChromeSignedIn()
        GA.closeDriver()
        if isSignedIn:
            return True
        else:
            return False

    def isChromeSignedIn(self, user):
        query = f'SELECT * FROM users WHERE id="{user["id"]}"'
        users = pd.read_sql(query, sql.connect(self.db_path))
        users = users.to_dict('records')
        debug(users[0]['chrome_signin'])
        return users[0]['chrome_signin']
    
    def updateChromeSignIn(self, user):
        db = sql.connect(self.db_path)
        query = f'UPDATE users SET chrome_signin=1, chrome_session="{user["id"]}" WHERE id="{user["id"]}"'
        db.execute(query)
        db.commit()
        db.close()

    def createAccount(self, user):
        sms = juicy()
        account = GoogleAccount(user['email'], user['fname'], user['lname'], 'hehehahahoho', sms)
        account.create()
        return

    def chromeSignIn(self, email):
        query = f'SELECT * FROM users WHERE email="{email}"'
        users = pd.read_sql(query, sql.connect(self.db_path))
        users = users.to_dict('records')
        user = users[0]
        email = user['email']
        fname = user['fname']
        lname = user['lname']
        id = user['id']
        password = 'hehehahahoho'

        GA = GoogleAccount(email, fname, lname, password, None)
        GA.create()
        wait(3)
        GA.closeDriver()
        return

    def chromeSignInAll(self, users):
        for user in users:
            if self.isChromeSignedIn(user):
                debug(f"ALREADY SIGNED IN: {user}")
                continue
            debug(f"SIGNING IN: {user}")
            IP.shuffle()
            self.createAccount(user)
            self.updateChromeSignIn(user)
            bigWait()
            
    def getUser(self, platform, experiment_id):
        platform = platform.lower()
        query = f'SELECT * FROM users WHERE exp="{experiment_id}" AND {platform} is NULL'
        df = pd.read_sql(query, sql.connect(self.db_path))
        users = list(df.to_dict('records'))
        return users[0]['email'], users[0]['chrome_session']

    def getUnassignedUser(self, platform, experiment_id):
        platform = platform.lower()
        query = f'SELECT * FROM users WHERE exp="{experiment_id}" AND {platform}=0 AND chrome_signin=1'
        df = pd.read_sql(query, sql.connect(self.db_path))
        users = list(df.to_dict('records'))
        return users[0]['email'], users[0]['chrome_session']
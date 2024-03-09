import pandas as pd
import sqlite3
import os
from utils.log import debug


class DB:
    def __init__(self, database, expid):
        # if database not exists
        self.expid = expid
        self.database = database

        if not os.path.exists(self.database):
            debug('Database not found. Creating new database...')
            self.create_db(self.database)

    def create_db(self):
        create = '''CREATE TABLE "google_accounts" (
                    "index"	INTEGER,
                    "fname"	TEXT,
                    "lname"	BLOB,
                    "email"	NUMERIC,
                    "id"	INTEGER,
                    "xp"	TEXT,
                    "google_account_setup"	INTEGER DEFAULT 0,
                    "google_signin"	INTEGER DEFAULT 0,
                    "chrome_signin"	INTEGER DEFAULT 0,
                    "chrome_session"	TEXT,
                    "reddit_signin"	INTEGER DEFAULT 0,
                    "twitter_signin"	INTEGER DEFAULT 0)'''
    
        conn = sqlite3.connect(self.database)
        c = self.conn.cursor()
        c.execute(create)
        conn.commit()
        conn.close()

    def users_exists(self, n_users):
        conn = sqlite3.connect(self.database)
        df = pd.read_sql("SELECT * FROM google_accounts", conn)
        if len(df) == n_users:
            return True
        else:
            return False

    def add_google_accounts(self, users):
        conn = sqlite3.connect(self.database)

        dicts = []
        for user in users:
            user.account_is_setup()
            dicts.append(user.create_dict())
        df = pd.DataFrame(dicts)
        df.to_sql('google_accounts', conn, if_exists='replace')

    def google_signed_in(self, user_id):
        conn = sqlite3.connect(self.database)
        df = pd.read_sql(f"SELECT * FROM google_accounts WHERE id = '{user_id}'", conn)
        if df['google_signin'][0] == 1:
            return True
        else:
            return False

    def update_google_signin(self, user):
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(f"UPDATE google_accounts SET google_signin = 1 WHERE id = '{user}'")
        c.execute(f"UPDATE google_accounts SET chrome_signin = 1 WHERE id = '{user}'")
        c.execute(f"UPDATE google_accounts SET chrome_session = '{user}' WHERE id = '{user}'")
        conn.commit()
        conn.close()


    def get_google_accounts(self):
        #in pandas
        conn = sqlite3.connect(self.database)
        df = pd.read_sql(f"SELECT * FROM google_accounts WHERE xp = '{self.expid}'", conn)
        df.set_index('id', inplace=True)
        debug(df)
        df = df.to_dict('index')
        conn.close()
        return df
    
    def is_signed_in(self, platform, user_id):
        platform = platform.name
        conn = sqlite3.connect(self.database)
        df = pd.read_sql(f"SELECT * FROM google_accounts WHERE id = '{user_id}'", conn)
        if df[f'{platform}_signin'][0] == 1:
            return True
        else:
            return False

    def update_signin(self, platform, user_id):
        platform = platform.name
        conn = sqlite3.connect(self.database)
        c = conn.cursor()
        c.execute(f"UPDATE google_accounts SET {platform}_signin = 1 WHERE id = '{user_id}'")
        conn.commit()
        conn.close()
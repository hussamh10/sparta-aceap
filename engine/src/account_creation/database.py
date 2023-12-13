import pandas as pd
import sqlite3

def add_google_accounts(users):
    conn = sqlite3.connect('experiments.db')

    dicts = []
    for user in users:
        dicts.append(user.create_dict())
    df = pd.DataFrame(dicts)
    df.to_sql('google_accounts', conn, if_exists='replace')


def update_google_signin(user):
    conn = sqlite3.connect('experiments.db')
    c = conn.cursor()
    c.execute(f"UPDATE google_accounts SET google_signin = 1 WHERE id = '{user.id}'")
    c.execute(f"UPDATE google_accounts SET chrome_signin = 1 WHERE id = '{user.id}'")
    c.execute(f"UPDATE google_accounts SET chrome_session = '{user.id}' WHERE id = '{user.id}'")
    conn.commit()
    conn.close()

def get_google_accounts(expid):
    #in pandas
    conn = sqlite3.connect('experiments.db')
    df = pd.read_sql(f"SELECT * FROM google_accounts WHERE xp = '{expid}'", conn)
    df.set_index('id', inplace=True)
    df = df.to_dict('index')
    conn.close()
    return df

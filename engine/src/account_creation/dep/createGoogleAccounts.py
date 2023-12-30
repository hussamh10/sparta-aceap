from account_creation.JuicySMS import juicy
from account_creation.GoogleAccounts import GoogleAccount

def create_account(user):
    sms = juicy()
    account = GoogleAccount(user['email'], user['fname'], user['lname'], 'hehehahahoho', sms)
    account.create()
    return
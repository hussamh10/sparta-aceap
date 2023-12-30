from account_creation.GoogleAccounts import GoogleAccount
from account_creation.JuicySMS import juicy
from utils import shuffleIP as IP

IP.shuffle()
sms = juicy()
acc = GoogleAccount('xp3aceap3@spartaaceap.com', 'hussam', 'alzahrani', 'hehehahahoho', sms)
acc.create()
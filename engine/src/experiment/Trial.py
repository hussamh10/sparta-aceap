from utils.log import debug
from utils.util import wait
from time import sleep
from users.User import User
from platforms.Reddit import Reddit

class Trial():
    def __init__(self, action, topic, userid, platform, experiment_id):
        self.action = action
        self.topic = topic
        self.userid = userid
        self.platform = platform
        self.experiment_id = experiment_id

    def signUpUser(self):
        self.user = User(self.platform, self.userid, self.experiment_id)
        self.user.chromeSignUp()
        wait(4)

    def loadUser(self):
        self.user = User(self.platform, self.userid, self.experiment_id)
        self.user.chromeSignIn()

    def checkSignin(self):
        self.user = User(self.platform, self.userid, self.experiment_id)
        return self.user.checkSignin()

    def observe(self):
        dump = self.user.recordHome(self.experiment_id, scrolls=6, posts_n=10)
        return dump

    def closeDriver(self):
        self.user.closeDriver()

    def runExperiment(self):
        debug('User loaded')

        dump = 'No Treatment'
        if self.action == '':
            pass

        if self.action == 'comment':
            self.user.comment(self.topic, self.supplement, self.experiment_id)

        if self.action == 'open':
            debug('Opening post')
            dump = self.user.openPost(self.topic, self.experiment_id)

        if self.action == 'dislike':
            self.user.dislikePost(self.topic, self.experiment_id)

        if self.action == 'like':
            debug('Liking post')
            dump = self.user.likePost(self.topic, self.experiment_id)

        if self.action == 'join':
            self.user.joinCommunity(self.topic, self.experiment_id)

        if self.action == 'follow':
            self.user.followUser(self.topic, self.experiment_id)

        sleep(2)
        self.user.goHome()
        wait(3)
        return dump

    def quit(self):
        self.user.quit()
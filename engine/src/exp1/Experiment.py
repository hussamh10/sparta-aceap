from utils.log import debug
from time import sleep
from users.User import User
from platforms.Reddit import Reddit

class Experiment():
    def __init__(self, intention, belief, userid, platform, characteristics, experiment_name, supplement='', N=1):
        self.intention = intention
        self.belief = belief
        self.userid = userid
        self.platform = platform
        self.characteristics = characteristics
        self.supplement = supplement
        self.experiment_name = experiment_name
        self.N = N


    def loadUser(self):
        self.user = User(self.platform)
        self.user.loadUser(username=self.userid)

    def runExperiment(self):
        debug('Loading user')
        self.loadUser()
        debug('User loaded')

        for i in range(self.N):
            if self.intention == 'nothing':
                pass

            if self.intention == 'comment':
                self.user.comment(self.belief, self.supplement, self.experiment_name)

            if self.intention == 'open':
                self.user.openPost(self.belief, self.experiment_name)

            if self.intention == 'dislike':
                self.user.dislikePost(self.belief, self.experiment_name)

            if self.intention == 'like':
                debug('Liking post')
                self.user.likePost(self.belief, self.experiment_name)

            if self.intention == 'join':
                self.user.joinCommunity(self.belief, self.experiment_name)

            if self.intention == 'follow':
                self.user.followUser(self.belief, self.experiment_name)

            sleep(2)
            self.user.goHome()
        self.user.recordHome(self.experiment_name, scrolls=6, posts_n=10)

    def quit(self):
        self.user.quit()

class Replay(object):
    def __init__(self, old_replay = ''):
        self.replay = ''
        self.is_replay = False
        self._old_replay = old_replay

    def init_play(self):
        re1 = []
        for i in self._old_replay:
            re1.extend(i.split())
        self.replay = ''.join([ i + ' ' for i in re1 ])

    def replay_add(self,y):
        if not self.is_replay:
            self.replay += y
 
    def play_begin(self):
        self.init_play()
        self.is_replay = True

    def play_end(self):
        self.is_replay = False

from .board import Board
import re

class Board3(Board):
    def __init__(self, config):
        super(Board3, self).__init__(config)

    def play_replay(self):
        self.play_begin()
        for s1 in  self.replay.split():
            if s1[0] == '#':
                continue 
            flag,x,y = re.search('(\w+)_(\d+)_(\d+)',s1).groups()
            x = int(x)
            y = int(y)
            if flag == 'm':
                self.play_mark(x,y)
            elif flag == 'r':
                self.play_rm(x,y)
            yield False
        self.play_end()
        yield True


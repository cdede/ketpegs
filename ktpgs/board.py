from .b_group import Board2
from .cell import Cell
from .common import tips
from .b_random import BoardRan

class Darkerror(RuntimeError):
    pass

class Board(Board2):
    def __init__(self, config):
        super(Board, self).__init__(config)
        if config.map != '':
            maps = ''.join(config.map)
            self.map = config.map
        else:
            tmp1 = BoardRan(config)
            maps = str(tmp1)
        for x in range(self.w * self.h):
            x1,y1 = self.allcoords[x]
            self[x1,y1].map = maps[x]

        self.fill_group()
        self.lose = False
        self.dn_num = 0

    def _num_kind(self,kind):
        num = 0
        for i in self.grid:
            if int(i.map) == kind:
                num+=1
        return num

    @property
    def num_kinds(self):
        tmp = {}
        for i in range(self._kind):
            j = i + 1
            tmp[j] = self._num_kind(j)
        return tmp

    def __iter__(self):
        return iter(self.grid)

    def _clear_exposed(self):
        for x, y in self.allcoords:
            self[x,y].exposed=False
  
    def start(self):
        self.fill_group()

    def check_win(self):
        if self.win or self.lose:
            self.save_file('cur')
        if self.lose:
            return tips['lose'] 
        elif self.win:
            return tips['win'] 
        return ''

    def change_day(self):
        self.dn_num += 1
        self.replay_add('#DN_%d ' % self.dn_num)
        self.isday = not self.isday

    @property
    def status(self):
        return '%s: %dx%d %d/%d' % ('day' if self.isday else 'night', self.w, self.h, 
        self.b_oil_num,self.total_oil)

from .common import trans_lab
from .play_rep import Board3
class Board1(Board3):
    def __init__(self, config):
        super(Board1, self).__init__(config)
        self.mark_cell = None

    def swap(self,a0,a1):
        if a0.map == a1.map:
            return False
        t1,t2= a1.second,  a0.second
        a0.map, a1.map= a1.map,  a0.map
        a0.second, a1.second= t1,t2
        self.fill_group()
        return True

    def swap_cell(self,c1):
        if self.mark_cell is None:
            self.mark_cell = c1
            c1.not_marked()
            return False
        else:
            tmp1 = self.mark_cell
            self.mark_cell = None
            tmp1.not_marked()
            return self.swap(tmp1,c1)

    def play_mark(self,x,y):
        tmp = self[x, y]
        if tmp.is_oil :
            return
        if tmp.is_marked():
            if self.swap_cell(tmp):
                self.add_rand('swap')
            self.replay_add(trans_lab('m',x,y))


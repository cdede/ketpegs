from .neighbor import Board0
from .common import trans_lab
from .group import Group
from operator import  attrgetter

class Board2(Board0):
    def __init__(self, config):
        super(Board2, self).__init__(config)

    def clear(self,x,y):
        'right key'
        self.state[x,y].group.dead()

    def play_rm(self,x,y):
        self._history.add(str(self))
        t1 = self[x, y].clear()
        if t1 > 0:
            self.add_rand('clear')
            self.replay_add(trans_lab('r',x,y))

    def _clear_group(self):
        for x, y in self.allcoords:
            self[x,y].group=None

    def group(self,x,y,tag=0):
        tmp = self[x,y]
        if tmp.isnull():
            return Group()
        if tmp.group is None:
            g1 = Group()
            g1.add(tmp)
            return g1
        else:
            return tmp.group

    def fill_group(self,size=5):
        self.big_groups={}
        self._clear_group()
        self._clear_exposed()
        self.sort_null = []
        for x, y in self.allcoords:
            g1 = self.group(x,y)
            tmp1 = len(g1.cells)
            if tmp1 >= size :
                self.big_groups[g1.id]=g1
                for i in g1.cells:
                    i.exposed = True
            tmp2 = self[x,y]
            if tmp2.isnull():
                self.check_cell_oil(tmp2)
                if tmp2 not in self._always_null:
                    self.sort_null.append(tmp2)

        self.sort_null=sorted(self.sort_null,key=attrgetter('neighbor_num', 'x'))
        _mid_null = sum([i.neighbor_num for i in [self.sort_null[0],self.sort_null[-1]]])/4
        for i in range(len(self.sort_null)):
            tmp = self.sort_null[i]
            if tmp.neighbor_num >= _mid_null:
                self._mid_null = i
                break


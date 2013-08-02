import random
from .neighbor import Board0
class BoardRan(Board0):
    def __init__(self, config):
        random.seed(config.seed)
        super(BoardRan, self).__init__(config)
        self.oil_coords = [(x, y) for y in range(1,self.h-1)
                     for x in range(1,self.w-1)]
        self.all_cell = [(x, y) for y in range(self.h)
                     for x in range(self.w)]
        self.lst_1 = list(range(1,self._kind+1))
        self.fill_oil()
    
    def fill_oil(self):
        oil = '153207846'
        x,y = random.choice(self.oil_coords)
        for i in range(9):
            tmp = self[x,y].neighbor_me[i]
            tmp.map = oil[i]
            self.all_cell.remove((tmp.x,tmp.y))
        self.fill_other()

    def fill_other(self, num =11):
        if num == 0:
            return
        x,y = random.choice(self.all_cell)
        k1 = random.choice(self.lst_1)
        self[x,y].map = k1
        self.all_cell.remove((x,y))
        self.fill_other(num - 1)

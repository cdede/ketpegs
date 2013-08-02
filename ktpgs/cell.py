from .entropy import neighbor_entropy
from .common import  entropy_rule
class Cell(object):
    def __init__(self, x=0, y=0, map='0', board =None):
        self.x = x
        self.y = y
        self.board = board
        self.neighbor = None
        self.neighbor_me = None
        self.marked = False
        self.exposed = False
        self.hopes = []
        self.oil_num = 0
        self.map = '0'

    @property
    def map(self):
        return self._map

    @property
    def is_oil(self):
        return self.oil_num > 0

    @property
    def is_2(self):
        return self.second == 5

    @property
    def set_num(self):
        return len(set(self.entropy_lst))

    @map.setter
    def map(self,value):
        tmp = int (value)
        if tmp > 5 :
            self.second = 5
            tmp1 = str(tmp-5)
        else:
            self.second = 0
            tmp1 = value
 
        self._map = tmp1
        self.group = None
        self.exposed = False

    def dead(self):
        self.map ='0'
        self.second = 0

    def isnull(self):
        if self.map == '-1':
            return True
        return  self.map =='0'

    def __str__(self):
        return self.map

    def __int__(self):
        return int(self.map)

    def not_marked(self):
        if self.is_marked():
            self.marked = not self.marked
        return

    def is_marked(self):
        if self.isnull() or self.group.id in self.board.big_groups:
            return False
        return True

    def clear(self):
        if self.isnull() or self.group is None or not self.group.id in self.board.big_groups:
            return 0
        tmp = int(self.map)
        num =0
        for i in self.board.big_groups[self.group.id].cells:
            num +=1
            i.dead()
        self.board.fill_group()
        return num*tmp

    @property
    def neighbor_num(self):
        return neighbor_entropy(3, self.entropy_lst)

    @property
    def entropy_lst(self):
        return [entropy_rule[int(i.map) + i.second] for i in self.neighbor_me ]

    @property
    def symbol(self):
        letter = 'A' if self.second == 5 else 'a'
        if int(self) in range(self.board._kind+1):
            symbol = chr(ord(letter)+int(self)) if int(self) > 0 else '.' 
        if self.marked:
            symbol += '*'
        if self.exposed:
            symbol += '-'
        if self.is_oil:
            symbol += '+'
        return symbol

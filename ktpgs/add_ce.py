from .save_b import Board4
from .entropy import gen_kind_num

class Board5(Board4):
    def __init__(self, config):
        super(Board5, self).__init__(config)
        self._add_swap = config.add_swap
        self._add_clear = config.add_clear
        self._history = set()

    def add_rand(self,rand_mines):
        if type(rand_mines) == str:
            if rand_mines == 'swap':
                rand_mines = self._add_swap
            elif rand_mines == 'clear':
                rand_mines = self._add_clear
        for _ in range(rand_mines):
            try:
                tmp = self.sort_null[self._mid_null]
            except IndexError: 
                return True
            
            tmp.map = str(gen_kind_num(self.num_kinds,self._kind))
            tmp.second = 5 if tmp.map in '123' and rand_mines == self._add_clear else 0
            self._mid_null += 1

        if str(self) in self._history :
            return True
        try:
            self.fill_group()
        except IndexError: 
            return True
        return False



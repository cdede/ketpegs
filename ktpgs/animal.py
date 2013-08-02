import os
from .common import save_file, m12_rule
from .animal0 import Animal0

class Animal(Animal0):
    def __init__(self, seed):
        super(Animal, self).__init__(seed)

    def run_cus(self, str1):
        '''run custom '''
        if str1 == "":
            return
        num_a = str1[0]
        if num_a in m12_rule.keys():
            self.run_group(num_a)
            tmp = 1
        elif num_a == 'r':
            self.reverse()
            tmp = 1
        elif  num_a == 'l':
            try:
                num_b = str1[1]
            except IndexError:
                num_b = '-1'
            if num_b in [chr (i) for i in range(ord('1'), ord('9')+1)]:
                self.num_l = int(num_b)
                self.love()
                tmp = 2
            else:
                self.num_l = 1
                self.love()
                tmp = 1
        self.run_cus(str1[tmp:])

    def run_group(self, char):
        if char in m12_rule.keys():
            str1 = m12_rule[char]
            self.run_cus(str1)

    @property
    def cur(self):
        for i in range(len(self.lst)):
            if i != self.lst[i]:
                break
        return i

    @property
    def cur_where(self):
        for i in range(len(self.lst)):
            if  self.cur== self.lst[i]:
                return i + 1

    @property
    def will(self):
        t1 = self.cur + 1
        t2 = self.cur_where
        if self.cur >= 2:
            ret = '-1'
            if t1 == 3:
                if t2 in [4,5,10]:
                    ret = 'a'
                elif t2 in [6,7,8,11,12,9]:
                    ret = 'b'
            if t1 == 4:
                if t2 in [6,7,12,5,9,10]:
                    ret = 'c'
                elif t2 in [8,11]:
                    ret = 'd'
            if t1 == 5:
                if t2 in [7,12,10,8,9,11]:
                    ret = 'e'
                elif t2 in [6]:
                    ret = 'f'
        elif t1 ==1 :
            if t2 in [12]:
                ret =  'r'
            else:
                ret = 'l'
        elif t1 ==2 :
            ret = 'l'
        return ret

    @property
    def win(self):
        return self.cur == 11

    def set_map(self,map):
        for i in range(len(self.lst)):
            self.lst[i] = int(map[i],16) - 1
    
    def solve(self):
        s1 = ''
        while not self.win:
            t1 = self.will
            if t1 =='l':
                self.love()
            elif t1 =='r':
                self.reverse()
            else:
                self.run_group(t1)
            s1 += t1
        return s1

def solve_m12(seed):
    a=Animal(seed)
    a.randomize()
    t1 = a.lst
    return t1,a.solve()

import random
class Animal0(object):
    def __init__(self,seed,size = 6):
        self.seed = seed
        random.seed(seed)
        self.size = size*2
        self.num_l = 1
        self.reset()
        tmp2 = {}
        tmp1 = self.size +1

    def reset(self):
        self.lst = list(range(self.size))

    def reverse(self):
        self.lst.reverse()

    def love(self):
        if self.num_l == 1:
            s1 = ''
        else:
            s1 = str(self.num_l)

        for i in range(self.num_l):
            tmp = []
            size2 = self.size//2
            for i in range(self.size - 1 , size2 - 1, -1):
                tmp += [self.lst[i]]
            tmp2 = []
            for i in range(0, size2):
                tmp2 += [self.lst[i], tmp[i]]
            self.lst = tmp2
    
    def run(self,lst = []):
        for i in lst:
            self.reverse()
            self.love(i)

    def __getitem__(self, i):
        return self.lst[i]

    def randomize(self):
        '''randomize'''
        self.reset()
        num = 0
        while num < 200:
            num += 1
            tmp = random.random()
            if tmp > 0.67:
                self.love()
            else:
                self.reverse()


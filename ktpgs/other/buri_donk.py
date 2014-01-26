#!/usr/bin/env python
'''a game call m12
'''
import random
from hashlib import sha256
import string
MAX_NUM = 96
HASH_NUM = 14

def passgen(x):
    char=string.ascii_lowercase

    char_up=string.ascii_uppercase
    nums=string.digits
    sym='&_'
    password=''
    while len(password)!=x:
        if random.randrange(0,100)/2==0:
            password+=char[random.randrange(0,26)]
        elif random.randrange(0,100)/2==0:
            password+=char_up[random.randrange(0,26)]
        elif random.randrange(0,100)/2==0:
            password+=nums[random.randrange(0,9)]
        elif random.randrange(0,100)/2==0:
            password+=sym[random.randrange(0,2)]
    return password

class BuriDonk:
    '''the sporadic groups
    Mathieu groups M12
    '''
    def __init__(self):
        random.seed(open('/dev/urandom', 'rb').read(512))
        self.lst = [0,1]
        self.test = False

    def reset(self):
        sel0 = random.randint(0,1)
        sel1 = (sel0 + 1 ) %2
        self.sel = [sel0,sel1]
        self.make_password(MAX_NUM)


    def make_password(self, num1):
        '''change back'''
        for i in range(2):
            lst = {}
            lst['pass'] = passgen(num1+i)
            lst['hash'] = sha256(lst['pass'].encode('utf-8')).hexdigest()[:HASH_NUM]
            self.lst[self.sel[i]] = lst
        return 

    def show(self):
        '''show'''
        if  self.test :
            return
        for i in range(2):
            tmp = self.lst[i]['pass']
            print ('echo -n "' + tmp + '" |sha256sum')

    def loop(self):
        '''get input'''
        k = 0
        wins = 0
        while  k < 100:
            self.reset()
            if not self.test:
                print ('0  :',self.lst[0]['hash'])
                print ('1  :',self.lst[1]['hash'])
            str_1 = '0' if self.test  else input("What is your choice:   ")
            if len(str_1) == 1:
                if str_1 in '01':
                    i1 = int(str_1)
                    if self.sel[i1] == 0 :
                        if not self.test:
                            print ('you win')
                        wins += 1 
                    else:
                        if not self.test:
                            print ('you lose')

                if str_1 == 'q':
                    break
                if str_1 == 't':
                    self.test = True
                    continue
            k += 1
            self.show()
        print('win :' ,wins )


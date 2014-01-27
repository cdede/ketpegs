'''
OilMetals -> BayouWater -> AurousWood -> SeekFire -> DealBoard -> BoldBoard -> PegBoard
'''
import os
from operator import  attrgetter
import random
import re

from .entropy import gen_kind_num
from .common import ( save_file, split_str , 
        peg_neighbor,get_mid, check_cell_lst,trans_lab,
        )

from .base.log import  GameLog
from .cell import Cell
from .group import Group

class SaveHistory(object):
    def __init__(self, root):
        config = root.config
        self.work_path = config.work_path
        self._name = config.name
        self._seed = config.seed
        self.root = root

    @property
    def save(self):
        config ={}
        config['seed'] = self._seed
        config['name'] =self._name
        config['old_replay'] = split_str(self.root.tp1.replay, 70)
        return config

    def save_history(self,flag='',prefix = ''):
        if prefix == '':
            prefix = self._name
        os.chdir(self.work_path)
        w_l = 'win' if self.root.win else 'lose'
        fstr ='_'+w_l if flag == 'cur' else ''
        filename = "%s_%d_%d%s.json" % (prefix,self.root.b_oil_num,
                len(self.root.tp1.replay.split()),fstr)
        save_file(filename,self.save)
 
class TrapReplay(object):
    def __init__(self, root ):
        self.replay = ''
        self.is_replay = False
        self._old_replay = root.config.old_replay
        self.root = root

    def init_play(self):
        re1 = []
        for i in self._old_replay:
            re1.extend(i.split())
        self.replay = ''.join([ i + ' ' for i in re1 ])

    def replay_add(self,y):
        if not self.is_replay:
            self.replay += y
 
    def play_begin(self):
        self.init_play()
        self.is_replay = True

    def play_end(self):
        self.is_replay = False

    def play_replay(self):
        self.play_begin()
        for s1 in  self.replay.split():
            if s1[0] == '#':
                continue 
            flag,x,y = re.search('(\w+)_(\d+)_(\d+)',s1).groups()
            x = int(x)
            y = int(y)
            if flag == 'm':
                self.root.play_mark(x,y)
            elif flag == 'r':
                self.root.play_rm(x,y)
            yield False
        self.play_end()
        yield True

class IceEarth(object):
    def __init__(self, root):
        random.seed(root.config.seed)
        self.root = root

        self.oil_coords = [(x, y) for y in range(1,self.root.h-1)
                     for x in range(1,self.root.w-1)]
        self.all_cell = [(x, y) for y in range(self.root.h)
                     for x in range(self.root.w)]
        self.lst_1 = list(range(1,self.root._kind+1))
        self.fill_oil()
    
    def fill_oil(self):
        oil = '153207846'
        x,y = random.choice(self.oil_coords)
        for i in range(9):
            tmp = self.root[x,y].neighbor_me[i]
            tmp.map = oil[i]
            self.all_cell.remove((tmp.x,tmp.y))
        self.fill_other()

    def fill_other(self, num =11):
        if num == 0:
            return
        x,y = random.choice(self.all_cell)
        k1 = random.choice(self.lst_1)
        self.root[x,y].map = k1
        self.all_cell.remove((x,y))
        self.fill_other(num - 1)

    def __str__(self):
        return str(self.root)

class OilMetals(object):

    def __init__(self, config):
        self.log0 = GameLog()
        self.log0.log = 'init OilMetals'

        self.w, self.h = config.width, config.height
        self.total_oil = int(self.w*self.h/9)
        self.b_oil_num = 0
        self._old_oil = None
        self._always_null = []
        self.config = config
        self.tp1 = TrapReplay(self)

    @property
    def old_oil(self):
        return self._old_oil

    @old_oil.setter
    def old_oil(self, value):
        self._always_null = []
        if value == None:
            return
        self._old_oil = value
        x,y = value.x,value.y
        p = peg_neighbor
        for j4 in range(4):
            p4 = p[j4]
            p2 = p4[1]
            try :
                neighbor2 = self[x+p2[0],y+p2[1]]
                self._always_null.append( neighbor2)
            except:
                pass


    @property
    def win(self):
        return self.b_oil_num >= self.total_oil

    def check_cell_oil(self, tmp2):
        if tmp2.set_num == 9 and tmp2.neighbor_num == 0:
            if self.old_oil == None:
                self.old_oil = tmp2
     
            elif self.old_oil == tmp2:
                for i in tmp2.neighbor_me:
                    i.oil_num = 1
            elif self.old_oil != tmp2:
                for i in tmp2.neighbor_me:
                    i.oil_num += 1
                for i in self.old_oil.neighbor_me:
                    i.oil_num -= 1
                    if i.oil_num == 0:
                        i.dead()
                self.b_oil_num += 1
                self.tp1.replay_add('#O_%d ' % self.b_oil_num)
                self.old_oil = tmp2

class BayouWater(OilMetals):
    def __init__(self, config):
        super(BayouWater, self).__init__(config)
        self.log0.log = 'init BayouWater'

        self._kind = config.kind
        self.allcoords = [(x, y) for y in range(self.h)
                     for x in range(self.w)]
        self.grid = []
        for x in range(self.w * self.h):
            x1,y1 = self.allcoords[x]
            tmp = Cell(x1,y1,'0')
            tmp.board =self
            self.grid.append(tmp)
        self.fill_neighbor()

    def fill_neighbor(self,flag = 'cross'):
        for x, y in self.allcoords:
            tmp = self[x,y]
            if flag == 'cross':
                tmp2 = []
                for i in [[x+1,y],
                    [x-1,y],
                    [x,y+1],
                    [x,y-1]
                    ]:
                    ix,iy = i
                    try:
                        tmp2.append(tmp.board[ix,iy])
                    except:
                        #pass
                        tmp2.append(Cell(None,None,'-1'))
                tmp.neighbor = tmp2
                tmp3 = []
                for i in range(-1,2):
                    for j in range(-1,2):
                        ix,iy = x + i,y + j
                        try:
                            tmp3.append(tmp.board[ix,iy])
                        except:
                            #pass
                            tmp3.append(Cell(None,None,'0'))
                tmp.neighbor_me = tmp3

    def __getitem__(self, i):
        x = i[0]
        y = i[1]
        if x<0 or self.w<=x or y<0 or self.h<=y:
            raise ValueError("Coordinates out of range %i,%i"% (x,y))
        return self.grid[(i[1] * self.w) + i[0]]

    def __setitem__(self, i, v):
        self.grid[(i[1] * self.w) + i[0]] = v

    def __str__(self):
        s1=''
        for x, y in self.allcoords:
            tmp = self[x,y]
            s1+=str(int(tmp)+tmp.second)
        return s1

    @property
    def num_null(self):
        num = 0
        for i in self.grid:
            if i.isnull():
                num+=1
        return num

class AurousWood(BayouWater):
    def __init__(self, config):
        super(AurousWood, self).__init__(config)
        self.log0.log = 'init AurousWood'

    def clear(self,x,y):
        'right key'
        self.state[x,y].group.dead()

    def play_rm(self,x,y):
        self._history.add(str(self))
        t1 = self[x, y].clear()
        if t1 > 0:
            self.add_rand('clear')
            self.tp1.replay_add(trans_lab('r',x,y))

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

class Darkerror(RuntimeError):
    pass

class SeekFire(AurousWood):
    tips = {
            'finish':'Finish. start.',
            'win':'Success. Return to restart.',
            'lose':'Failure. Return to restart.',
            }
    def __init__(self, config):
        super(SeekFire, self).__init__(config)
        self.log0.log = 'init SeekFire'
        self.sav4 = SaveHistory(self)

        if config.map != '':
            maps = ''.join(config.map)
            self.map = config.map
        else:
            maps = str(IceEarth(self))
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
            self.sav4.save_history('cur')
        if self.lose:
            return self.tips['lose'] 
        elif self.win:
            return self.tips['win'] 
        return ''

    def change_day(self):
        self.dn_num += 1
        self.tp1.replay_add('#DN_%d ' % self.dn_num)
        self.isday = not self.isday

    @property
    def status(self):
        return '%s: %dx%d %d/%d' % ('day' if self.isday else 'night', self.w, self.h, 
        self.b_oil_num,self.total_oil)

class DealBoard(SeekFire):
    def __init__(self, config):
        super(DealBoard, self).__init__(config)
        self.log0.log = 'init DealBoard'

        self.mark_cell = None

    def swap(self,a0,a1):
        b0 = a0 + a1
        if b0:
            self.fill_group()
        else:
            return b0
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
            self.tp1.replay_add(trans_lab('m',x,y))

class BoldBoard(DealBoard):
    def __init__(self, config):
        super(BoldBoard, self).__init__(config)
        self.log0.log = 'init BoldBoard'

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

class PegBoard(BoldBoard):

    back= {
            '130': '001',
            '240': '002',
            '350': '003',
            '410': '004',
            '520': '005',
            '110': '002',
            '220': '003',
            '330': '004',
            '440': '005',
            '550': '001',
        }
 
    def __init__(self, config):
        self.isday = True
        super(PegBoard, self).__init__(config)
        self.log0.log = 'init PegBoard'

        self._seed = config.seed
        self._old_lose = False

    def fill_heart(self):
        p = peg_neighbor
        self.marked_num =0
        for x, y in self.allcoords:
            for tmp1 in list(self.back.keys()):
                if self[x,y].map == tmp1[0]:
                    for j4 in range(4):
                        p4 = p[j4]
                        p1 = p4[0]
                        p2 = p4[1]
                        try :
                            neighbor1 = self[x+p1[0],y+p1[1]]
                            neighbor2 = self[x+p2[0],y+p2[1]]
                            rule1 = "%s%s%s"%(self[x,y].map,neighbor1.map,neighbor2.map) 
                            tmp_lst = [self[x,y], neighbor2,  neighbor1]
                            if rule1 == tmp1 and check_cell_lst(tmp_lst,'is_oil') :
                                if not self[x,y].marked :
                                    self[x,y].hopes = []
                                    self[x,y].marked=True
                                    self.marked_num +=1
                                self[x,y].hopes.append(neighbor2)
                        except:
                            pass
        if self.marked_num == 0:
            if self._old_lose:
                self.lose = True
                return
            self.change_day()
            self._clear_group()
            self.start()
        else:
            if self._old_lose:
                self._old_lose = False

    
    def add_rand(self,rand_mines):
        if super(PegBoard, self).add_rand(rand_mines) :
            self.change_day()
            self._old_lose = True
            self._clear_exposed()
            self.fill_heart()

    def play_mark(self,x,y):
        if self.isday:
            super(PegBoard, self).play_mark(x,y) 
        else:
            tmp = self[x, y]
            if tmp.marked:
                if tmp.isnull():
                    m1 = self.mark_cell
                    self._jump(m1,tmp)
                    self.tp1.replay_add(trans_lab('m',m1.x,m1.y))
                    self.tp1.replay_add(trans_lab('m',tmp.x,tmp.y))
                    self.mark_cell = None
                else:
                    self.mark_cell = tmp
                    self._clear_marked()
                    for i in tmp.hopes:
                        i.marked = True
            else :
                self.mark_cell = None
                self._clear_marked()
                self.fill_heart()

    def _clear_marked(self):
        for x, y in self.allcoords:
            self[x,y].marked=False

    def _share_neighbor(self,c0,c1):
        tx = get_mid(c0.x,c1.x)
        ty = get_mid(c0.y,c1.y)
        return self[tx,ty]

    def _jump(self,c0,c1):
        middle = self._share_neighbor(c0,c1)
        rule1 = "%s%s%s"%(c0.map,middle.map,c1.map) 
        t1 = c0.is_2 or middle.is_2 
        c0.map,middle.map,c1.map  = self.back[rule1]
        if t1 :
            if c1.map in '123':
                c1.second = 5
        self._clear_marked()
        self.fill_heart()

    def play_rm(self,x,y):
        if self.isday:
            super(PegBoard, self).play_rm(x,y) 

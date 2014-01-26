from .common import  peg_neighbor

class Replay(object):
    def __init__(self, old_replay = ''):
        self.replay = ''
        self.is_replay = False
        self._old_replay = old_replay

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

class Again(Replay):

    def __init__(self, config):
        super(Again, self).__init__(config.old_replay)
        self.w, self.h = config.width, config.height
        self.total_oil = int(self.w*self.h/9)
        self.b_oil_num = 0
        self._old_oil = None
        self._always_null = []

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
                self.replay_add('#O_%d ' % self.b_oil_num)
                self.old_oil = tmp2

from .cell import Cell

class Board0(Again):
    def __init__(self, config):
        super(Board0, self).__init__(config)
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


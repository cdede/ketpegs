from .again import Again
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


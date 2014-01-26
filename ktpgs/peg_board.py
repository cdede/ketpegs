from .board import Board5
from .common import hope_rule,peg_neighbor,get_mid, check_cell_lst,trans_lab

class PegBoard(Board5):
    def __init__(self, config):
        self.isday = True
        super(PegBoard, self).__init__(config)
        self._seed = config.seed
        self.back=hope_rule
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
                    self.replay_add(trans_lab('m',m1.x,m1.y))
                    self.replay_add(trans_lab('m',tmp.x,tmp.y))
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

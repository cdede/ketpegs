from .board import PegBoard
from .base.client import ThreadedClient
from .common import get_wp_config, save_file, tips
config = get_wp_config()
class KtpClient(ThreadedClient):
    """
    """
    def __init__(self ):
        """
        """
        self.init_g()
        self._gen1 = None
        super(KtpClient, self).__init__(self.g.h,self.g.w)

    def init_g(self):
        self.g = PegBoard(config)
        self.g.start()

    @property
    def msg(self):
        g2 = []
        for x in range(self.g.h*self.g.w):
            x1,y1 = self.g.allcoords[x]
            g2.append(self.g[x1,y1].symbol)
        self._msg.cells = g2
        self._msg.statusline = '%d,%d %s' % (self.gui._cur_x, self.gui._cur_y, self.g.status )
             
        return self._msg

    def input(self,a):
        if self.g.win or self.g.lose:
            if a == 'enter':
                self.init_g()
            return
        x,y = self.gui._cur_x,self.gui._cur_y
        if a == 'm':
            self.g.play_mark(x,y)
            b = self.g.check_win()
            self._msg.tipline=b
        elif a == ' ':
            self.g.play_rm(x,y)
            b = self.g.check_win()
            self._msg.tipline=b
        elif a == 'R' and len(self.g.tp1.replay)==0:
            for a in self.g.tp1.play_replay():
                pass
            self._msg.tipline = tips['finish']
        elif a == 'r' and len(self.g.tp1.replay)==0:
            self.update_timer()
        elif a == 't':
            self.gui.loop.remove_alarm(self.handle2)
        elif a == 's':#save
            self.g.sav4.save_history()


    def update_timer(self,loop=None,user_data=None):
        if self._gen1 is None:
            self._gen1 = self.g.play_replay()
            self.num = 0
        a = next(self._gen1)
        if not a:
            self.num += 1
            self._msg.tipline = str(self.num)
            self.gui.render(self.msg)
            self.handle2 = self.gui.loop.set_alarm_in(0.01, self.update_timer )
        else:
            self._msg.tipline = tips['finish']
            self.gui.render(self.msg)



from .swap import Board1
import os
from .common import save_file, split_str

class Board4(Board1):
    def __init__(self, config):
        super(Board4, self).__init__(config)
        self.work_path = config.work_path
        self._name = config.name

    @property
    def save(self):
        config ={}
        config['seed'] = self._seed
        config['name'] =self._name
        config['old_replay'] = split_str(self.replay, 70)
        return config

    def save_file(self,flag='',prefix = ''):
        if prefix == '':
            prefix = self._name
        os.chdir(self.work_path)
        w_l = 'win' if self.win else 'lose'
        fstr ='_'+w_l if flag == 'cur' else ''
        filename = "%s_%d_%d%s.json" % (prefix,self.b_oil_num,
                len(self.replay.split()),fstr)
        save_file(filename,self.save)
 

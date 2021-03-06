import os
import json
'''
fire 1
earth 2
metals 3
water 4
wood 5
5 + 2
2 + 4 
4 + 1
1 + 3
3 + 5
'''
   
animal_rule = [ 4,2, 5,5,2, 1,1,2, 3,3,2, 4]

# Available colors are:
#   none (transparent/default)
#   black
#   red
#   green
#   yellow
#   blue
#   magenta
#   cyan
#   white
class TargetConfig(object):
    def __init__(self, config):
        self.colors = {
    # Grid colors.
    'unselected':        ('green', 'none'),
    'selected':          ('black', 'green'),
    'unselected_exposed': ('blue', 'none'),
    'selected_exposed':   ('black', 'blue'),

    'statusline': ('white', 'none'),

    # Message colors.
    'info':    ('white', 'none'),
    'failure': ('red', 'none'),
    'success': ('green', 'none'),
}

        self.name = config['name']
        self.old_replay = config['old_replay']
        self.work_path = ''

        self.width,         self.height = 9, 9
        self.kind = 5
        self.add_swap = 3
        self.add_clear = 6
        self.map = ''
        self.seed = config['seed']

def get_wp_config():
    file_conf = 'config.json'
    work_path = '%s/ketpegs' % os.getenv('XDG_CONFIG_HOME',
                                             '%s/.config' % os.getenv('HOME'))
    p1 = work_path if  os.path.exists(work_path+'/'+file_conf) else '/usr/share/ketpegs'
    with open(p1+'/'+file_conf,'r') as file1:
        config=json.load(file1)
    config = TargetConfig(config)
    config.work_path = work_path
    return config
 

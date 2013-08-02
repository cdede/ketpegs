import math
import random
import json
import os
import textwrap
from operator import  attrgetter
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
hope_rule= {
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

m12_rule= {
        'a':'rl2rl5rl4',
        'b':"rlrl3rl2",
        'c':"rlrl3rl2rl9rl7rl8",
        'd':"rl3rl6rlrl9rl7rl8",
        'e':"rl9rl7rl8rl7rlrl5",
        'f':"rlrl3rl2rl7rlrl5rl7rlrl5",
        }
animal_rule = [ 4,2, 5,5,2, 1,1,2, 3,3,2, 4]

entropy_rule = [ 0, -1 , -2 , -3 ,-4 ,4 ,1,2,3]

peg_neighbor = [
        [(1,0),(2,0)],
        [(-1,0),(-2,0)],
        [(0,1),(0,2)],
        [(0,-1),(0,-2)],
        ]

tips = {
        'finish':'Finish. start.',
        'win':'Success. Return to restart.',
        'lose':'Failure. Return to restart.',
        }

def get_mid(a,b):
    return min (a,b)+int(math.fabs(a-b)/2)

def sum_str(s1):
    return sum([int(i) for i in s1])

def save_file(filename,obj1):
    with open(filename, 'w') as file1:
        k=json.dump(obj1,file1,indent=4)

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
        self.DEBUG = True
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
 
def split_str(str1,size):
    ret = []
    wrapped = textwrap.wrap(str1, size)
    for line in wrapped:
        ret.append( line)
    return ret

def check_cell_lst(lst,att1):
    ret = True
    for i in lst:
        f1 = attrgetter(att1)
        ret = ret and not f1(i)
    return ret

def trans_lab(a,b,c):
    return '%s_%d_%d ' % (a,b,c)

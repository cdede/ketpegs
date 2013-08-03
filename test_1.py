#!/usr/bin/python
import os
import json
from ktpgs.cell import Cell
from ktpgs.board import Board
from ktpgs.b_random import BoardRan
from ktpgs.peg_board import PegBoard
from ktpgs.common import TargetConfig, entropy_rule, get_wp_config
from ktpgs.entropy import gen_kind_num
from ktpgs.gen_oil import ent2num, gen_oil
from ktpgs.animal import Animal

import unittest
os.sys.path.append(os.curdir)

config = get_wp_config()
map1='''
111100000
110000000
100000000
100002220
000000220
000003000
153000200
207000040
846050000
'''
config.map=map1.replace("\n",'')

class CellTest(unittest.TestCase):

    def setUp(self):
        self.c1=Cell(0,0,'7')

    def tearDown(self):
        pass

    def test_dead(self):
        self.c1.dead()
        self.assertTrue(self.c1.map=='0')


class  BoardTest(unittest.TestCase):

    def setUp(self):
        self.b1=PegBoard(config)

    def tearDown(self):
        pass

    def test_str(self):
        self.assertTrue(str(self.b1)==config.map)
        self.assertTrue(self.b1==self.b1[0,0].board)

    def test_neighbor(self):
        self.assertTrue(len(self.b1[0,0].neighbor)==4)

    def test_group(self):
        g1=self.b1.group(0,0)
        self.assertTrue(len(g1.cells)==8)
        g1=self.b1.group(7,7)
        self.assertTrue(len(g1.cells)==1)
        self.assertTrue(len(self.b1.big_groups)==2)
        self.assertTrue(self.b1.num_kinds=={1: 10, 2: 8, 3: 3, 4: 2, 5: 2})
        self.assertTrue(self.b1[1,7].neighbor_num==0)

    def test_neighbor_num(self):
        self.assertTrue(int(self.b1[0,0].neighbor_num)==5)

    def test_save_file(self):
        self.b1.save_file(prefix='test')

    def test_save_file1(self):
        self.b1.lose = True
        self.b1.save_file('cur', prefix = 'test')

class PegBoardTest(unittest.TestCase):
    def setUp(self):
        self.p1 = PegBoard(config)

    def test_fill_heart(self):
        self.p1.fill_heart()
        self.assertTrue(self.p1.marked_num==9)
        self.assertTrue(len(self.p1[6,3].hopes)==3)
        self.assertTrue(len(self.p1[7,4].hopes)==2)

class FunTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_gen_kind_num(self):
        a= gen_kind_num({ 1:0, 2:1, 3:1, 4:1, 5:0 },5)
        self.assertTrue(a==1)
    def test_entropy_rule(self):
        for i in range(len(entropy_rule)):
            self.assertTrue(ent2num(entropy_rule[i])==i)

    def test_gen_oil(self):

        self.assertTrue(gen_oil()=='''153
207
846
---------
''')

map_a1 = {
        "3_4": "128374bca596", 
        "3_5": "1275364ca8b9", 
        "3_6": "12ba537c6894", 
        "3_7": "128a79346c5b", 
        "3_8": "125648b3a7c9", 
        "3_9": "129ac86b3754",
        "3_10": "1268a57b93c4", 
        "3_11": "12c9b6478a35", 
        "3_12": "1296cb47a583", 
        "4_5": "123c4867b9a5", 
        "4_6": "123684c5a9b7", 
        "4_7": "1238c64b597a", 
        "4_8": "12387c549ba6", 
        "4_9": "1236958b47ac", 
        "4_10": "1235b6c974a8", 
        "4_11": "1238596ca74b", 
        "4_12": "1237ac6958b4", 
        "5_6": "1234b597a8c6", 
        "5_7": "1234a85b6c97", 
        "5_8": "12349a65cb78", 
        "5_9": "123487bc56a9", 
        "5_10": "123479c6b58a", 
        "5_11": "12346c8a795b", 
        "5_12": "1234cba98765", 
    }

seed1 = '7pVq7ogV'

class AnimalTest(unittest.TestCase):
    def setUp(self):
        self.p1 = Animal('abc')

    def test_solve_1(self):
        for i in map_a1.keys():
            self.p1.set_map(map_a1[i])
            self.p1.solve()

    def test_solve_2(self):
        for i in range(10):
            seed = "%s%d" %(seed1,i)
            self.p1 = Animal(seed)
            self.p1.randomize()
            self.p1.solve()

class BoardRanTest(unittest.TestCase):
    def setUp(self):
        self.tmp1 = config.map
        config.map =''
        self.p1 =BoardRan(config)

    def test_fill_oil(self):
        self.assertTrue(self.p1.num_null == 62)

    def tearDown(self):
        config.map =self.tmp1

if __name__ == "__main__":
    unittest.main()

class Group:
    def __init__(self ):
        self.id = ''
        self.cells = []
        self.map = 0
    def add(self,cell1):
        if cell1.is_oil:
            return
        if self.id =='':
            self.id = "%d_%d" % (cell1.x,cell1.y)
            self.cells.append(cell1)
            cell1.group =self
            self.map = cell1.map
            for i in cell1.neighbor:
                self.add(i)
        elif cell1 not in self.cells and cell1.map == self.map :
            self.cells.append(cell1)
            cell1.group =self
            for i in cell1.neighbor:
                self.add(i)



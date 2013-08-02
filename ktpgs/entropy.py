from operator import  attrgetter

def neighbor_entropy(size=3, map=[]):
    size = size
    grid = {}
    for x in range(size ):
        for y in range(size):
            grid[(x,y)]=map[y*size+x]
    average = sum(map)/size
    entropy = 0
    for x in range(size ):
        tmp = 0
        tmp1 = 0
        for y in range(size):
            tmp += grid[(x,y)]
            tmp1 += grid[(y,x)]
        a1,a2 =tmp-average,tmp1-average
        entropy += a1*a1 +a2*a2
    return entropy

class KindEntropy(object):
    def __init__(self,  kind = 1,entropy = 0.0):
        self.kind = kind
        self.entropy = entropy

def gen_kind_num(dict1,kind):
    sum1 = sum([ dict1[ i+1] for i in range(kind)])
    average = sum1 + 1
    tmp_lst = []
    for i in range(kind):
        j = i + 1
        dict2 = dict1.copy()
        dict2[j] = dict1[j] + 1
        tmp_lst.append(KindEntropy(j,kind_entropy(dict2,average,kind)))
    sort_lst=sorted(tmp_lst,key=attrgetter('entropy', 'kind'))
    return sort_lst[0].kind

def kind_entropy(dict1, average, kind):
    entropy = 0
    for i in range(kind):
        j = i + 1
        a1 = dict1[j]*kind - average
        entropy += a1*a1
    return entropy


from .entropy import neighbor_entropy

def gen_oil():
    ret = ''
    lst1 = []
    t = list(range(1,10))
    t.remove(5)
    for i in t:
        for j in t:
            ij9 = 15 - i -j
            if ij9 in t :
                lst=[i,j,ij9]
                if len(set(lst)) == 3 :
                    lst1.append(lst)
    lst2 = []
    for i in t:
        i9 = 10 - i 
        if i9 in t :
            lst=[i,5,i9]
            lst2.append(lst)
    t = lst1
    k = []
    for i in t:
        k.extend(i)
        for j in lst2:
            k.extend(j)
            for m in t:
                k.extend(m)
                if len(set(k)) == 9 and neighbor_entropy(map=k) == 0:
                    if  i[0] == 4 and j[0] == 3:
                        ret += say ([ent2num(i-5) for i in k])+"\n"
                k = k[:-3]
            k = k[:-3]
        k = k[:-3]
    return ret

def ent2num(num):
    if num <= 0:
        ret = -num
    elif num == 4 :
        ret = 5
    else:
        ret = num + 5
    return ret

def say(lst):
    ret = ''
    for i in range(3):
        ret += ''.join([str(i) for  i in lst[i*3:(i+1)*3]])+"\n"
    ret += '---------'
    return ret

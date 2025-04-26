import numpy as np
from collections import Counter


## Testing s/f/pair type functions, takes cards list and gives t/f
def flush(suits):
    # suits = [c[1] for c in cards]
    n = len(Counter(suits))
    return n == 1

def convert(v):
    '''converts letters to value T-K, A goes to 14'''
    # D = {'A':14, 'K':13, 'Q':12, 'J':11, 'T':10}
    if v == 'A':
        return 14
    if v == 'K':
        return 13
    if v =='Q':
        return 12
    if v == 'J':
        return 11
    if v == 'T':
        return 10
    return int(v)

def straight(values):
    # values = [c[0] for c in cards]
    # values = [convert(v) for v in values]
    # values.sort()
    if len(Counter(values)) < 5:
        return False
    s = (values[4] - values[0] == 4) or (values[3] == 5 and values[4] == 14)
    return s

def pair(values):
    '''fully process pair type (non S/F) hands'''
    C = Counter(values)
    l = C.most_common()
    type = [i[1] for i in l]
    vals = [i[0] for i in l]
    if type == [4,1]:
        return ['Q'] + vals
    if type == [3,2]:
        return ['B'] + vals
    if type == [3,1,1]:
        temp = vals[1:]
        temp.sort(reverse = 'True')
        return ['T', vals[0]] + temp
    if type == [2,2,1]:
        temp = vals[:-1]
        temp.sort(reverse = 'True')
        return ['TP'] + temp + [vals[2]]
    if type == [2,1,1,1]:
        temp = vals[1:]
        temp.sort(reverse = 'True')
        return ['P', vals[0]] + temp
    vals.sort(reverse = 'True')
    return ['HC'] + vals

def value_aux(s):
    '''takes string input of hand and returns hand value as list [hand type, rank(s)]'''
    # HC, P, TP, T, S, F, B, Q, SF
    cards = s.split(" ")
    values = [c[0] for c in cards]
    values = [convert(v) for v in values]
    values.sort()
    suits = [c[1] for c in cards]
    f = flush(suits)
    s = straight(values)
    if f and s:
        hc = 0
        if values[4] - values[3] > 1:
            hc = 5
        else:
            hc = values[4]
        return ['SF', hc]
    if f:
        values.reverse()
        return ['F', values]
    if s:
        hc = 0
        if values[4] - values[3] > 1:
            hc = 5
        else:
            hc = values[4]
        return ['S', hc]
    return pair(values)

def type_conv(type):
    '''takes hand rank string and gives values 1 to 9'''
    D = {'HC':1, 'P':2, 'TP':3, 'T':4, 'S':5, 'F':6, 'B':7, 'Q':8, 'SF':9}
    return D[type]
    
def value(s):
    '''Applies aux and converts hand type chars to values, HC = 1..., SF = 9'''
    temp = value_aux(s)
    temp[0] = type_conv(temp[0])
    return temp
    
def compare(s):
    '''Takes string, splits in 2 hands and compare. Return True if player 1 wins'''
    s1 = s[:14]
    s2 = s[15:]
    v1 = value(s1)
    v2 = value(s2)
    for i in range(10):
        if v1[i]!=v2[i]:
            return v1[i]>v2[i]
    return True
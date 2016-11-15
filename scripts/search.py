import json
import os
from collections import defaultdict

def power(a, b, mod):
    x = 1
    while b:
        if (b&1):
            x *= a
            if x >= mod:
                x %= mod
        a *= a
        if a >= mod:
            a %= mod
        b >>= 1
    return x

ques_list = list()

os.chdir("..")
basedir = os.path.abspath(os.curdir)

with open(basedir + '/data/q1.json', 'r') as f:
    json_data = json.loads(f.read())

for q in json_data:
    ques_list.append(q['short_description'])

mod1 = 10**9 + 7
mod2 = 9999991
power1 = [31]
power2 = [97]
for i in range(1, 1005):
    h1 = power1[i - 1]*31
    h2 = power2[i - 1]*97
    if h1 >= mod1:
        h1 %= mod1
    if h2 >= mod2:
        h2 %= mod2
    power1.append(h1)
    power2.append(h2)

d = defaultdict(list)

def get_hash(q):
    h1, h2 = 0, 0
    ll = list()
    for ind, character in enumerate(q):
        h1 += ord(character.lower())*power1[ind]
        h2 += ord(character.lower())*power2[ind]
        if h1 >= mod1:
            h1 %= mod1
        if h2 >= mod2:
            h2 %= mod2
        ll.append((h1 ,h2))
    return ll

for ques_id, ques in enumerate(ques_list):
    for element in get_hash(ques):
        d[ques_id].append(element)

def search(s):
    l = len(s)
    hsh = get_hash(s)[-1]
    lst = list()
    for ques_id, ques in enumerate(ques_list):
        x = d[ques_id]
        for length in range(l - 1, len(ques)):
            hsh1, hsh2 = x[length][0], x[length][1]
            if length + 1 != l:
                hsh1 -= x[length - l][0]
                hsh2 -= x[length - l][1]
                while hsh1 < 0:
                    hsh1 += mod1
                while hsh2 < 0:
                    hsh2 += mod2
                hsh1 *= power(power1[length - l], mod1 - 2, mod1)
                hsh2 *= power(power2[length - l], mod2 - 2, mod2)
                if hsh1 >= mod1:
                    hsh1 %= mod1
                if hsh2 >= mod2:
                    hsh2 %= mod2
            if (hsh1, hsh2) == hsh:
                lst.append(ques_id)
                break
    return lst

s = input().split(" ")
dd = dict()
for each in s:
    for entry in search(each):
        if entry in dd.keys():
            dd[entry] += 1
        else:
            dd[entry] = 1
if len(dd) > 5:
    for entry in sorted(dd.items(), key=lambda x:x[1])[-5:]:
        print(entry[0], ques_list[entry[0]])
else:
    for entry in dd.items():
        print(entry[0], ques_list[entry[0]])

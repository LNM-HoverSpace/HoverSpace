import os
from searching import Searching
import json

ques_list = list()

os.chdir("..")
basedir = os.path.abspath(os.curdir)

with open(basedir + '/data/q1.json', 'r') as f:
    json_data = json.loads(f.read())

for q in json_data:
    ques_list.append(q['short_description'])

srch = Searching(10**9 + 7, 9999991, 31, 97)
for i, q in enumerate(ques_list):
    srch.add_string(i, q)

s = input()
all_ans = srch.search(s)
for entry in all_ans:
    print(entry, ques_list[entry])

import json
import os
from random import randint, choice
from bson.objectid import ObjectId

key = dict()

def generate_random_key():
    while True:
        data = randint(1, 10**20)
        if data in key.keys():
            continue
        key[data] = True
        return data

def find_json(path):
    with open(path, 'r') as f:
        json_data = json.loads(f.read())
    return json_data

def return_ques(json_data):
    quess = {}
    for q in json_data:
        data = {
            '_id': q['id'],
            'short_description': q['short_description'],
            'long_description': q['long_description'],
            'timestamp': q['timestamp'],
            'postedBy': None,
            'accepted_ans': None,
            'votes': 0,
            'flag': False,
            'ansID': list()
        }
        quess[generate_random_key()] = data
    return quess

def return_ans(json_data):
    anss = {}
    for a in json_data:
        data = {
            '_id': a['_id'],
            'votes': 0,
            'quesID': None,
            'timestamp': a['timestamp'],
            'postedBy': None,
            'ansText': a['anstext']
        }
        anss[generate_random_key()] = data
    return anss

os.chdir("..")
basedir = os.path.abspath(os.curdir) + '/data/'

a1 = return_ans(find_json(basedir + 'a1.json'))
a2 = return_ans(find_json(basedir + 'a2.json'))
ans = {}
for a, b in a1.items():
    ans[a] = b
for a, b in a2.items():
    ans[a] = b

q1 = return_ques(find_json(basedir + 'q1.json'))
q2 = return_ques(find_json(basedir + 'q2.json'))
ques = {}
for a, b in q1.items():
    ques[a] = b
for a, b in q2.items():
    ques[a] = b

user_json = find_json(basedir + 'sample_user.json')
while len(user_json) > 50:
    ind = randint(0, len(user_json) - 1)
    del user_json[ind]

c1, c2 = 0, 0
for user in user_json:
    c1 += user['quesPosted']
    c2 += user['ansPosted']
    user['voted_ans'] += 5
    user['voted_ques'] += 5

while len(ques) > c1:
    ind = choice(list(ques.keys()))
    del ques[ind]

while len(ans) > c2:
    ind = choice(list(ans.keys()))
    del ans[ind]

ans_temp = list(ans.keys())

while len(ans_temp):
    a = ans_temp.pop()
    ind = choice(list(ques.keys()))
    ques[ind]['ansID'].append(ans[a]['_id']['$oid'])
    ans[a]['quesID'] = ques[ind]['_id']['$oid']

ques_back = list(ques.keys())
ans_back = list(ans.keys())
user_list = []

for user in user_json:
    data = {
        '_id': user['_id'],
        'email': user['email'],
        'firstname': user['firstname'],
        'lastname': user['lastname'],
        'password': user['password'],
        'karma': user['karma'],
        'quesPosted': list(),
        'ansPosted': list(),
        'bookmarks': list(),
        'voted_ques': list(),
        'voted_ans': list()
    }
    qp, ap = {}, {}

    while user['quesPosted']:
        q = ques_back.pop()
        ques[q]['postedBy'] = user['_id']
        data['quesPosted'].append(ques[q]['_id']['$oid'])
        user['quesPosted'] -= 1
        qp[q] = True

    while user['ansPosted']:
        a = ans_back.pop()
        data['ansPosted'].append(ans[a]['_id']['$oid'])
        ans[a]['postedBy'] = user['_id']
        user['ansPosted'] -= 1
        ap[q] = True

    while user['bookmarks']:
        ind = choice(list(ques.keys()))
        if ind in qp.keys():
            continue
        data['bookmarks'].append(ques[ind]['_id']['$oid'])
        user['bookmarks'] -= 1

    while user['voted_ques']:
        ind = choice(list(ques.keys()))
        if ind in qp.keys():
            continue
        data['voted_ques'].append(ques[ind]['_id']['$oid'])
        ques[ind]['votes'] += 1
        user['voted_ques'] -= 1

    while user['voted_ans']:
        ind = choice(list(ans.keys()))
        if ind in ap.keys():
            continue
        data['voted_ans'].append(ans[ind]['_id']['$oid'])
        ans[ind]['votes'] += 1
        user['voted_ans'] -= 1

    user_list.append(data)

with open(basedir + "user.json", 'w') as f:
    json.dump(user_list, f, sort_keys=True)

ans_list = []
for key, value in ans.items():
    ans_list.append(value)

with open(basedir + 'answer.json', 'w') as f:
    json.dump(ans_list, f, sort_keys=True)

ques_list = []
for key, value in ques.items():
    ques_list.append(value)

with open(basedir + 'question.json', 'w') as f:
    json.dump(ques_list, f, sort_keys=True)

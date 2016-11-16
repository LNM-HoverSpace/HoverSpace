from collections import defaultdict
from HoverSpace.methods import QUESTIONS_COLLECTION

class Searching:
    def __init__(self, m1, m2, p1, p2):
        self.mod1 = m1
        self.mod2 = m2
        self.power1 = self.get_power(p1, m1)
        self.power2 = self.get_power(p2, m2)
        self.d = defaultdict(list)
        self.jump = list()

    def get_power(self, val, mod):
        power = [val]
        for i in range(1, 1005):
            h = power[i - 1]*val
            if h >= mod:
                h %= mod
            power.append(h)
        return power

    def get_hash(self, s):
        h1, h2 = 0, 0
        hashes = list()
        for ind, character in enumerate(s):
            h1 += ord(character.lower())*self.power1[ind]
            h2 += ord(character.lower())*self.power2[ind]
            if h1 >= self.mod1:
                h1 %= self.mod1
            if h2 >= self.mod2:
                h2 %= self.mod2
            hashes.append((h1, h2))
        return hashes

    def add_string(self, ques_id, ques):
        for element in self.get_hash(ques):
            self.d[ques_id].append(element)

    def power(self, a, b, mod):
        x = 1
        while b:
            if b&1:
                x *= a
                if x >= mod:
                    x %= mod
            a *= a
            if a >= mod:
                a %= mod
            b >>= 1
        return x

    def query(self, s):
        l = len(s)
        hsh = self.get_hash(s)[-1]
        lst = list()
        for key, value in self.d.items():
            for length in range(l - 1, len(value)):
                hsh1, hsh2 = value[length][0], value[length][1]
                if length + 1 != l:
                    hsh1 -= value[length - l][0]
                    hsh2 -= value[length - l][1]
                    while hsh1 < 0:
                        hsh1 += self.mod1
                    while hsh2 < 0:
                        hsh2 += self.mod2
                    hsh1 *= self.power(self.power1[length - l], self.mod1 - 2, self.mod1)
                    hsh2 *= self.power(self.power2[length - l], self.mod2 - 2, self.mod2)
                    if hsh1 >= self.mod1:
                        hsh1 %= self.mod1
                    if hsh2 >= self.mod2:
                        hsh2 %= self.mod2
                if (hsh1, hsh2) == hsh:
                    lst.append(key)
                    break
        return lst

    def search(self, s):
        dd = defaultdict(int)
        for each in s.split(' '):
            if each in self.jump:
                continue
            for entry in self.query(each):
                if entry in dd.keys():
                    dd[entry] += 1
                else:
                    dd[entry] = 1

        l = list()
        if len(dd) > 5:
            for entry in sorted(dd.items(), key=lambda x: x[1])[-5:]:
                l.append(entry[0])
        else:
            for key, value in dd.items():
                l.append(key)
        return l

    def add_all(self):
		for entry in QUESTIONS_COLLECTION.find():
    		srch.add_string(str(entry['_id']), entry['short_description'])

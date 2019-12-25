import re


class Desentisize(object):
    data = None

    def __init__(self, data):
        self.data = data
        self.rules = iter([self.match_telphone, self.match_email, self.match_idcard, self.match_mobel])

    def match_telphone(self):
        p = re.compile(r"^1[3-9]\d{9}$")
        res = p.findall(self.data)
        return res

    def match_email(self):
        p = re.compile(r"\w{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}")
        res = p.findall(self.data)
        return res

    def match_idcard(self):
        p = re.compile(r"^[1-6]\d{5}[12]\d{3}(0[1-9]|1[12])(0[1-9]|1[0-9]|2[0-9]|3[01])\d{3}(\d|X|x)$")
        res = p.findall(self.data)
        return res

    def match_mobel(self):
        p = re.compile(r"\d{3}-\d{8}|\d{4}-\d{7}")
        res = p.findall(self.data)
        return res

    def deal(self):
        try:
            res = next(self.rules)()
            if res:
                self.data = self.data.replace(res[0], "*****")
            self.deal()
        except StopIteration:
            return


string = """
a = 1228291335@qq.com
b = 17621063414
c = 021-65979152
"""
des = Desentisize(string)
print("before:", des.data)
des.deal()
print("after:", des.data)

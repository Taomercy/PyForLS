import re


class Desentisize(object):
    data = None

    def __init__(self, data):
        self.data = data
        self.rules = iter([self.match_telphone, self.match_email, self.match_idcard, self.match_mobel])

    def match_telphone(self, context):
        p = re.compile(r"^1[3-9]\d{9}$")
        res = p.findall(context)
        return res

    def match_email(self, context):
        p = re.compile(r"\w{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}")
        res = p.findall(context)
        return res

    def match_idcard(self, context):
        p = re.compile(r"^[1-6]\d{5}[12]\d{3}(0[1-9]|1[12])(0[1-9]|1[0-9]|2[0-9]|3[01])\d{3}(\d|X|x)$")
        res = p.findall(context)
        return res

    def match_mobel(self, context):
        p = re.compile(r"\d{3}-\d{8}|\d{4}-\d{7}")
        res = p.findall(context)
        return res

    def deal(self):
        try:
            func = next(self.rules)
            for k, v in self.data.items():
                res = func(v)
                if res:
                    self.data[k] = v.replace(res[0], "*****")
            self.deal()
        except StopIteration:
            return


input_data = {'email': "1228291335@qq.com",
              "mobile-phone": "17621063414",
              "tel-phone": "021-65979152"}

des = Desentisize(input_data)
print("before:", des.data)
des.deal()
print("after:", des.data)

import re
import threading
import time
from threading import Thread


class Desentisize(object):
    data = None

    def __init__(self, data):
        self.input = data
        self.rules = [self.match_telphone, self.match_email, self.match_idcard, self.match_mobel]
        self.output = []

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

    def thread_func(self, json, threadLock):
        threadLock.acquire()
        for key, value in json.items():
            for rule in self.rules:
                res = rule(value)
                if res:
                    json[key] = value.replace(res[0], "****")
        self.output.append(json)
        threadLock.release()

    def deal(self):
        start = time.time()
        threads = []
        for info in self.input:
            threadLock = threading.Lock()
            thread = Thread(target=self.thread_func, args=(info, threadLock))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        print("span:", time.time() - start)


input_data = {'email': "1228291335@qq.com",
              "mobile-phone": "17621063414",
              "tel-phone": "021-65979152"}

json_list = []
for i in range(0, 500):
    json_list.append(input_data)

print("data size:", len(json_list))
des = Desentisize(json_list)
print("before:", des.input)
des.deal()
print("after:", des.output)

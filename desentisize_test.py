import re
import threading
import time
from threading import Thread
from desentisize import Desensitization


def span_cal(func):
    def func_wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print("span:", time.time() - start)
        return func
    return func_wrapper


class Desentisize(object):
    data = None

    def __init__(self, data):
        self.input = data
        self.rules = [self.match_email, self.match_idcard, self.match_mobile]
        self.output = []

    def match_email(self, context):
        p = re.compile(r"\w{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}")
        res = p.findall(context)
        if res:
            return Desensitization(email=context).get_email()
        return None

    def match_idcard(self, context):
        p = re.compile(r"^[1-6]\d{5}[12]\d{3}(0[1-9]|1[12])(0[1-9]|1[0-9]|2[0-9]|3[01])\d{3}(\d|X|x)$")
        res = p.findall(context)
        if res:
            return Desensitization(identity_card=context).get_identity_card()
        return None

    def match_mobile(self, context):
        p = re.compile(r"\d{3}-\d{8}|\d{4}-\d{7}")
        res = p.findall(context)
        if res:
            return Desensitization(mobile=context).get_mobile()
        return None

    # def match_address(self, context):
    #     if res:
    #         return Desensitization(address=context).get_address()
    #     return None

    def thread_func(self, json, threadLock):
        threadLock.acquire()
        for key, value in json.items():
            for rule in self.rules:
                res = rule(value)
                if res:
                    json[key] = res
        self.output.append(json)
        threadLock.release()

    @span_cal
    def deal(self):
        threads = []
        for info in self.input:
            threadLock = threading.Lock()
            thread = Thread(target=self.thread_func, args=(info, threadLock))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()


input_data = {'email': "linqunbin@126.com",
              "mobile-phone": "18911112222",
              "identity_card": "123123200001011234",
              "address": "上海市虹口区某某路某某号123室"}

json_list = []
for i in range(0, 500):
    json_list.append(input_data)

print("data size:", len(json_list))
des = Desentisize(json_list)
print("before:", des.input)
des.deal()
print("after:", des.output)

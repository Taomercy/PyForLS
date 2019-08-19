#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time


def funcA():
    class MyThread(threading.Thread):
        def __init__(self, threadID, param):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.param = param

        def run(self):
            threadLock = threading.Lock()
            threadLock.acquire()
            print "Starting thread [%d]" % self.threadID
            threadLock.release()
            print "Exiting thread [%d]" % self.threadID

    start = time.time()
    threads = []
    threadID = 1
    for i in range(10):
        thread = MyThread(threadID, i)
        thread.start()
        threads.append(thread)
        threadID += 1
    for t in threads:
        t.join()

    print "span:", time.time() - start


if __name__ == '__main__':
    funcA()


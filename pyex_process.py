# -*-coding:utf-8-*-
from multiprocessing import Lock, Process
import time


def process(num):
    time.sleep(num)
    print 'Process ' + str(num)


def process1():
    if __name__ == '__main__':
        for i in range(5):
            p = Process(target=process, args=(i,))  # args接受元组，只有一个元素的元组也不要漏了'，'
            p.start()
        print multiprocessing.cpu_count()
        for child in multiprocessing.active_children():
            print child.name + ' ' + str(child.pid)


class MyProcess(Process):
    def __init__(self, loop_count):
        Process.__init__(self)
        self.loop_count = loop_count

    def run(self):  # 这里相当于override process 的 run()
        for i in range(self.loop_count):
            time.sleep(1)
            print str(self.pid) + ' ' + str(i)


def process2():
    for i in range(2, 5):
        p = MyProcess(i)
        p.daemon = True  # daemon
        p.start()
        p.join()  # join

    print 'main process end'


class MyProcess2(Process):
    def __init__(self, loop_count, lock):
        Process.__init__(self)
        self.loop_count = loop_count
        self.lock = lock

    def run(self):
        for i in range(self.loop_count):
            time.sleep(0.1)
            self.lock.acquire()  # lock acquire and release
            print str(self.pid) + ' ' + str(i)
            self.lock.release()


def process3():
    lock = Lock()
    for i in range(10, 15):
        p = MyProcess2(i, lock)
        p.start()

process3()

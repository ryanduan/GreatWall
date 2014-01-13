#/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Ryan

import random
import time
import os

numy = str(time.strftime('%Y', time.localtime(time.time())))

def dlt():
    q = range(1,36)
    rq = []
    for i in range(5):
        x = random.randint(0, len(q)-1)
        rq.append(q.pop(x))
    h = range(1,13)
    rh = []
    for i in range(2):
        x = random.randint(0, len(h)-1)
        rh.append(h.pop(x))
    rq.sort()
    rh.sort()
    res = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    print res,'前区：',rq,'后区：',rh
dlt()

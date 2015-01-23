#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports

import random
import os

#vars
msg_i = '177.126.180.83 - - ['
msg_m = '/Aug/2013:'
msg_e = '­ -0300]   "GET   /meme.jpg   HTTP/1.1"   200 2148 "-­" "userid=5352b590-­05ac-­11e3-­9923-­c3e7d8408f3a'


def gerar_arquivo():
    d=1;
    h=0;
    m=0;
    s=0;
    os.mkdir("servidor1")
    os.mkdir("servidor2")
    os.mkdir("servidor3")
    os.mkdir("servidor4")
    os.mkdir("servidor_out")
    for x in range(0, 1000000):
        if(x%10==0):
            s=s+1
        if(s>5):
            s=0
            m=m+1
        if(m>59):
            m=0
            h=h+1
        if(h>23):
            h=0
            d=d+1
            print x
                    
        f = open("./servidor"+str(1)+"/log"+str(x%100)+".txt",'a')
        f.write(msg_i+str(d)+msg_m+str(h)+":"+str(m)+":"+str(s)+'2"'+msg_e+str(random.randint(0,50))+'"\n')
        f.close()
        f = open("./servidor"+str(2)+"/log"+str(x%100)+".txt",'a')
        f.write(msg_i+str(d)+msg_m+str(h)+":"+str(m)+":"+str(s)+'4"'+msg_e+str(random.randint(0,50))+'"\n')
        f.close()
        f = open("./servidor"+str(3)+"/log"+str(x%100)+".txt",'a')
        f.write(msg_i+str(d)+msg_m+str(h)+":"+str(m)+":"+str(s)+'6"'+msg_e+str(random.randint(0,50))+'"\n')
        f.close()
        f = open("./servidor"+str(4)+"/log"+str(x%100)+".txt",'a')
        f.write(msg_i+str(d)+msg_m+str(h)+":"+str(m)+":"+str(s)+'8"'+msg_e+str(random.randint(0,50))+'"\n')
        f.close()
        
        
gerar_arquivo()
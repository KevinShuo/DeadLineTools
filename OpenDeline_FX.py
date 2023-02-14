import subprocess
import sys
import threading
import os
import time
from pynput import mouse
import configparser
import psutil
import GPUtil
import datetime

Num = 0
GpuList = []
CpuList = []
iniPath = r'Y:\LUXSERVER\DATA_BASE\02_TD\IT\DeadLineTools\SetUp_FX.ini'


def mouseListern():
    global Num
    with mouse.Events() as events:
        for event in events:
            Num = 0


def Timing():
    global Num
    while True:
        time.sleep(1)
        try:
            conf = configparser.ConfigParser()
            conf.read(iniPath, encoding = 'utf-8')
            pathAll = conf.get('ProjectSet', 'Begin')
            TimeSet = conf.get('ProjectSet', 'Time')
            if int(pathAll) == 1:
                Num += 1
                print(('Time:%d' % Num))
                if Num == int(TimeSet):
                    print('---Strat Check CPU and GPU percent---')
                    checkpercent()
                    if 1 in CpuList:
                        if 1 in GpuList:
                            print('---CPU and Gpu  is free---')
                            CheckPath()
            else:
                Num = 0
                print('Program is Stop')
        except:
            print('---Warning!!!!!---Y: is no Exist or Other Error')


def CurrentTime():
    hour = datetime.datetime.today()
    return int(hour.strftime('%H'))


def checkpercent():
    global GpuList
    global CpuList
    global Num

    conf = configparser.ConfigParser()
    conf.read(iniPath, encoding = 'utf-8')
    CPUuse = int(conf.get('ProjectSet', 'CPU'))
    GPUuse = int(conf.get('ProjectSet', 'GPU'))
    Cpu_Gpu_CheckTime = int(conf.get('ProjectSet', 'Cpu_Gpu_CheckTime'))

    for i in range(5):
        print(('%d Minute :(About 1 minute)' % (i + 1)))
        time.sleep(Cpu_Gpu_CheckTime)
        for Count in range(20):
            if Num != 0:
                if GetGpuMemory() < GPUuse:
                    GpuList.append(1)
                    if Cpupercent() < CPUuse:
                        CpuList.append(1)
                    else:
                        print('CPU percent is High')
                        CpuList.append(0)
                        Num = 0
                        Timing()
                else:
                    print('GPU percent is High')
                    GpuList.append(0)
                    Num = 0
                    Timing()
            else:
                Timing()


def Cpupercent():
    cpuPercent = cpuMemory_percent_check()
    return int(cpuPercent)


def GetGpuMemory():
    GPUS = GPUtil.getGPUs()
    load = GPUS[0].load
    return int(load * 100)


def CheckPath():
    conf = configparser.ConfigParser()
    conf.read(iniPath, encoding = 'utf-8')

    pathAll = conf.get('ProjectSet', 'projectPath').split('|')
    if len(pathAll) == 1:
        path = pathAll[0].split(':')
        if os.path.isdir(path[0] + ':\\') == True:
            print((path[0] + ' :Path is Exist'))
            CheckProcess()
        else:
            print(('Build The Path:' + path[0] + ':\\'))
            os.system('subst ' + pathAll[0])
            CheckProcess()
    else:
        TrueList = []
        for path in pathAll:
            pathlist = path.split(':')
            if os.path.isdir(pathlist[0] + ':\\') == True:
                print((pathlist[0] + ' :Path is Exist'))
                TrueList.append(1)
            else:
                print(('Build The Path:' + pathlist[0] + ':\\'))
                os.system('subst ' + path)
                TrueList.append(1)
        if 1 in TrueList:
            CheckProcess()


pidList = []

'''def CheckProcess():
    global pidList
    global Num
    while True:
        p1 = psutil.pids()
        for pid in p1:
            DeadLineName = psutil.Process(pid).name()
            pidList.append(DeadLineName)
        time.sleep(1)
        if 'deadlineslave.exe' in pidList:
            print('Already Open the DeadLine')
            pidList.clear()
            Num = 0
            Timing()
        else:
            print('Opening the DeadLine')
            subprocess.Popen(r'C:\Program Files\Thinkbox\Deadline10\bin\deadlineslave.exe')
            pidList.clear()
            Num = 0
            Timing()'''


def CheckProcess():
    global pidList
    global Num
    conf = configparser.ConfigParser()
    conf.read(iniPath, encoding = 'utf-8')
    processAll = conf.get('ProjectSet', 'Process').split('|')
    p1 = psutil.pids()
    for pid in p1:
        DeadLineName = psutil.Process(pid).name()
        pidList.append(DeadLineName)
    if len(processAll) > 1:
        for process in processAll:
            print('---Strat Check the process---')
            if process in pidList:
                print(('%s:process is Exist' % process))
                pidList.clear()
                Num = 0
                Timing()
            else:
                if 'deadlineslave.exe' in pidList:
                    print('Already Open the DeadLine')
                    pidList.clear()
                    Num = 0
                    Timing()
                else:
                    print('Opening the DeadLine')
                    subprocess.Popen(r'C:\Program Files\Thinkbox\Deadline10\bin\deadlineslave.exe')
                    pidList.clear()
                    Num = 0
                    Timing()
    else:
        print('---Strat Check the process---')
        if processAll[0] in pidList:
            print(('%s:process is Exist' % processAll[0]))
            pidList.clear()
            Num = 0
            Timing()
        else:
            if 'deadlineslave.exe' in pidList:
                print('Already Open the DeadLine')
                pidList.clear()
                Num = 0
                Timing()
            else:
                print('***Opening the DeadLine***')
                subprocess.Popen(r'C:\Program Files\Thinkbox\Deadline10\bin\deadlineslave.exe')
                pidList.clear()
                Num = 0
                Timing()


def cpuMemory_percent_check():
    cpu_percent = psutil.cpu_percent(interval = 1)
    return cpu_percent


t1 = threading.Thread(target = Timing)
t2 = threading.Thread(target = mouseListern)
t1.start()
t2.start()
t1.join()
t2.join()

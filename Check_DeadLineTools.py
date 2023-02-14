# -*- coding: utf-8 -*-
import os
import time

import psutil
import subprocess
import configparser

List = []
try:
    while True:
        time.sleep(10)
        List.clear()
        p1 = psutil.pids()
        Path = r'Y:\LUXSERVER\DATA_BASE\02_TD\Maya_Menu\WS\MyselfScript\DeadLine_Admin\SetUp.ini'
        conf = configparser.ConfigParser()
        conf.read(Path, encoding = 'utf-8')
        ToolPath = conf.get('DeadLineTools', 'path')
        Reload = int(conf.get('DeadLineTools', 'Reload'))

        if Reload == 1:
            try:
                os.system('taskkill /f /t /im OpenDeline.exe')
            except:
                pass
        else:
            try:
                for id in p1:
                    DeadLineTools = psutil.Process(id).name()
                    List.append(DeadLineTools)

                if 'OpenDeline.exe' in List:
                    print('OpenDeline.exe is Exist')
                else:
                    print((subprocess.Popen(ToolPath)))
            except:
                pass
except:
    pass
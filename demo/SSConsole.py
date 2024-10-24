"""
@file simpsave.py
@author WaterRun
@version 0.12
@date 2024-10-22
@description Source code for the SimpSave project
"""

import simpsave as ss
import datetime

def parser() -> bool:
    ...
    
if __name__ == '__main__':
    print('SimpSave Demo Progarm: SSConsole\n')
    if not ss.ready():
        ss.init(['count','last use'],[0,datetime.datetime.now()])
    count, last_use = ss.read('count'), ss.read('last use') 
    print(f'The program has been run for {count} times.\nlast use: {last_use}')
    ss.write('count', count+1)
    ss.write('last use', datetime.datetime.now(), convert_unsupported=True)
       
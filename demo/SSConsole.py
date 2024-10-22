r"""
@author WaterRun
@date 2024-10-21
@version 1.0
一个示例程序,实现一个简单的终端,直观展示的SimpSave的功能
"""

# pip install simplesave
import simpsave as ss
import datetime

def parser():
    ...
    
if __name__ == '__main__':
    print("SimpSave demo program by WaterRun\n\n\n'>>' stand for await input")
    if not ss.ready():
        ss.init(['count'],[0])
    count = ss.read('count')
    print(f"SSConsole ver 1.0\nThe program has been runned {count} times before\n'help' for help, 'exit' for exit")
    ss.write('count',count+1)
    
    print(f'last use: {ss.read('last use')}') if ss.has('last use') else print('no exist last use record') 
    
    ss.write('last use', datetime.datetime.now(), unsupport_str_convert=True)    
    while True:
        input('>>')
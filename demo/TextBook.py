"""
@file TextBook.py
@author WaterRun
@version 1.0
@date 2024-10-22
@description SimpSave示例程序:记事本 
"""
import datetime
import time
import simpsave as ss

class TextBook:
    def __init__(self, name:str):
        self.name = name 
        self.author = ""
        self.content = []
        self.build_time = datetime.datetime.now()
        self.last_upadte = datetime.datetime.now()
        self.edit_time = 0
        self.has_pwd = False
        self.pwd = ""
    def __len__(self) -> int:
        return len(self.content)
    def load(self):
        ...
    def save(self):
        ...
    def delete(self):
        ...
        
def show_use_count():
    if not ss.ready():
        ss.init()
    if not ss.has('__COUNT__'):
        ss.write('__COUNT__', 0)
    else:
        ss.write('__COUNT__', count := ss.read('__COUNT__')+1)
    print("程序已运行{count}次")
    
def main_parser(command: str):
    ...
    
class Operation():
    ...
        
if __name__ == '__main__':
    print("SimpSave示例程序:TextBook")
    show_use_count()
    
    
    
    
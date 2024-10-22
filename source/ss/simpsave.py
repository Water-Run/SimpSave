"""
@file simpsave.py
@author WaterRun
@version 0.9
@description SimpSave项目源码
"""

import os
import configparser

r"""
SIMPSAVE_FILENAME: 用于存储SimpSave的INI文件名,默认为'__ss__.ini'
"""
SIMPSAVE_FILENAME = '__ss__' + '.ini' # 更改时只更改第一个字符串
        
def ready() -> bool:
    r"""
    通过INI文件存在与否判断SimpSave是否可用
    @return 存在与否
    """
    return os.path.exists(SIMPSAVE_FILENAME)

def clear_ss() -> bool:
    r"""
    在目录下删除SimpSave的INI文件 
    @return 删除情况
    """
    if not ready():
        raise FileNotFoundError(f"The SimpSave has not been initilaized: {SIMPSAVE_FILENAME} not found")
    return os.remove(SIMPSAVE_FILENAME)

def init(names:list[str], values:list[str]) -> bool:
    r"""
    初始化SimpSave:创建INI文件并写入的预设数据(names和values一一对应写入).
    @param names: 待写入的预设名称列表
    @param values: 待写入的预设值列表
    @return 初始化成功与否
    """
    if ready():
        raise FileExistsError(f"SimpSave has been initilaized:{SIMPSAVE_FILENAME} already exists")
    else:
        if len(names) != len(values):
            raise IndexError(f"The length of name list and value list must be equal ({len(names)}:{len(values)})")
        with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as file:
            file.write('')
            for name,value in zip(names, values):
                if not write(name, value, overwrite=False,auto_init=True):
                    return False
        return True
    
def has(name: str) -> bool:
    r"""
    @param name: 待查找的名称
    @return 存在与否
    """
    if not ready():
        raise FileNotFoundError(f"The SimpSave has not been initilaized: {SIMPSAVE_FILENAME} not found")
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME,encoding='utf-8')
    
    return config.has_section(name)

def read(name: str) -> any:
    r"""
    读取匹配指定名称的单元并返回其的值
    @param name: 待读取的名称
    @return 查找到的Unit
    """
    if not ready():
        raise FileNotFoundError(f"The SimpSave has not been initilaized: {SIMPSAVE_FILENAME} not found")
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME,encoding='utf-8')
    
    if name not in config:
        raise KeyError(f"Section {name} not found")
    
    section = config[name]
    type = section['type']
    value = section['value']
    
    support_types = ('int','float','bool','str','list','tuple','dict') # SimpSave only support basic types of python
    if type in support_types:
        value = eval(f"{type}({value})")
    else:
        raise TypeError(f"SimpSave only support types in {support_types}")
    
    return value
    
def write(name:str, value:any, overwrite=True, auto_init = True, type_check = True) -> bool:
    r"""
    写入指定值至指定名称中
    @param name: 写入的目标名称
    @param value: 待写入的值
    @param overwrite: 覆写开关(False下,将阻止已存在名称的再写入)
    @param auto_init: 自动初始化SimpSave开关(开启后,则在SimpSave未初始化的前提下自动初始化并写入指定数据)
    @return 写入情况
    """
    if (not ready()) and auto_init:
        init()
    elif not ready():
        raise FileNotFoundError(f"The SimpSave has not been initilaized: {SIMPSAVE_FILENAME} not found")
        
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME,encoding='utf-8')
    
    if not overwrite and has(name):
        raise KeyError(f"Overwrite Check Enabled: Section {name} already exists")
    
    if type_check and has(name) and type(old_value := read(name)) != type(value) :
        raise TypeError(f'Type Check Enabled: The Type of new Unit is {type(value).__name__}, while the old one is {type(old_value).__name__}')
    
    config[name] = {
        'type': type(value).__name__,
        'value': str(value)
    }
    
    with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    
    return True

def remove(name: str) -> bool:
    r"""
    删除存储的指定名称的项
    @param name: 待删除的名称
    @return 删除情况
    """
    if not ready():
        raise FileNotFoundError(f"The SimpSave has not been initilaized: {SIMPSAVE_FILENAME} not found")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME,encoding='utf-8')
    
    return config.remove_section(name)
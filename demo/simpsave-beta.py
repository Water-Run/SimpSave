"""
@file simpsave-beta.py
@author WaterRun
@version 1.0
@date 2024-10-30
@description Source code of simpsave project
"""

import os
import datetime
import configparser
import hashlib
import sys
import re
import importlib.util
from itertools import cycle
from typing import List, Any

_SIMPSAVE_DEFAULTPATH_ = '__ss__.ini' # Default filekey for the SimpSave INI file
_RESERVED_ = ('__path__', '__update__', '__build__', '__log__', '__description__', '__file__', '__lock__', '__delete__') # Reserved keys
_SUPPORTED_TYPES_ = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict') # Basic types that simpsave supported

r"""
Private
"""

class _Checker_:
    
    @staticmethod
    def input_legal(keys: List[str] = None, values: List[Any] = None,  annotations: List[str] = None, boolean_sequence: List[bool] = None,  seeds: list[str] = None, operation_file: str = None):
        r"""
        """
        
        if keys != None:
            for key in keys:
                
                if not isinstance(key, str):
                    _Process_.log(f'Input Checker:Type, key not string. {key} in {keys}', 0, operation_file)
                    raise TypeError(f'Key must be string: {key} in {keys}')
                
                if key in _RESERVED_:
                    _Process_.log(f'Input Checker:Value, key in reserved. {key} in {keys}', 0, operation_file)
                    raise ValueError(f'Key is reserved: {key} in {keys}. Reserved: {_RESERVED_}')

        if annotations != None and not all(isinstance(annotaition, str) for annotaition in annotations):
            _Process_.log(f'Input Checker:Value, annotation not string. {annotations}', 0, operation_file)
            raise ValueError(f'All annotation must be string ({annotations})')
        
        if seeds != None and not all(isinstance(seed, str) for seed in seeds):
            _Process_.log(f'Input Checker:Value, seed not string. {seeds}', 0, operation_file)
            raise ValueError(f'All seeds must be string ({seeds})')
        
        if boolean_sequence != None and not all(isinstance(bool_value) for bool_value in boolean_sequence):
            _Process_.log(f'Input Checker:Value, bool_value not boolean. {boolean_sequence}', 0, operation_file)
            raise ValueError(f'All bool_value must be boolean ({boolean_sequence})')
        
        if keys == values == annotations == boolean_sequence == seeds == None:
            _Process_.log(f'Input Checker:Value, none valid input', 0, operation_file)
            raise ValueError(f'Input checker can not work with all None value')  

        check_list = [keys, values, annotations, boolean_sequence, seeds]
        check_list = list(map(lambda x: check_list.remove(x) if x is None else ..., check_list))
        
        if not all(lambda x: x == True, map(lambda x: True if len(x) == len(check_list[0]) else False, check_list)):
            _Process_.log(f'Input Chekcer: Length inconsistency', 0, operation_file)
            raise ValueError(f'All input must have same length')
    
    @staticmethod        
    def input_lock(keys: List[str], operation_file: str):
        r"""
        """
        
        try:
            
            locks = read('__lock__', operation_file = operation_file)    
            for key in keys: 
                if key in locks:
                    _Process_.log(f'Lock Chekcer activated: {key} in {keys}', 0, operation_file)
                    raise ValueError(f'Lock Checker: operation denied for "{key}" (locked)')  
        
        except Exception as e:
            
            _Process_.log(f'Lock Checker Failed: {e}', 0, operation_file)
            raise RuntimeError('Lock Checker not available, exception are thrown for locked')

    @staticmethod
    def file_exists(path: str):
        r"""
        """
    
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' not found. Initialize SimpSave first.")

    @staticmethod
    def full_ready(path: str):
        
        r"""
        """
        
        if not ready(path):
            raise RuntimeError('Operation require full ready of SimpSave. If you not init first, init the SimpSave using "init()". ')
                
class _Process_:
    r"""
    """
    
    @staticmethod
    def path_parser(path: str | None) -> str:
        r"""
        """
        
        if path is None: # Default
            path = _SIMPSAVE_DEFAULTPATH_
            
        if not path.endswith('.ini'):
            _Process_.log(f'Path Parser interrupted due to not INI file path: {path}', 0, path)
            raise KeyError(f'Simpsave can only operate .ini file: {path} unsupported.')
        
        if path.startswith('::py?'):
            path = sys.exec_prefix + '\\ssdatas\\' + path.replace('::py?', '', 1)
        elif path.startswith('::ss?'):
            sspath = importlib.util.find_spec('simpsave')
            if sspath is not None and sspath.submodule_search_locations:
                path = sspath.submodule_search_locations[0] + '\\ssdatas\\' + path.replace('::ss?', '', 1)
            else:
                _Process_.log(f'Path Parser interrupted due to unable to find package path: {path}', 0, path)
                raise RuntimeError('Can not find the path of simpsave package. Have you installed using pip?')
        
        return path

    @staticmethod
    def force_write(keys:list[str], values:list[any], operation_file:str): # write() can not write preserveds
        r"""
        """
        
        try:
            config = configparser.ConfigParser()
            config.read(operation_file, encoding='utf-8')
            
            for key, value in zip(keys, values):
                
                value_type = type(value).__name__
                if value_type not in _SUPPORTED_TYPES_:
                    value = str(value)
                    value_type = 'str'
                
                config[key] = {'type': value_type, 'value': str(value)}
                with open(operation_file, 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
        except:
            return False
        return True

    @staticmethod
    def update(operation_file:str) -> bool: 
        r"""
        """
        
        if not _Process_.force_write(['__update__'], [datetime.datetime.now()], operation_file):
            raise RuntimeError('SimpSave failed to update')

    @staticmethod
    def log(info: str, level: int, operation_file: str):
        
        r"""
        """
        
        codes = ['ERR', 'IPT', 'STD']
        if level not in range(0,3):
            raise ValueError(f'Log level {level} out of range')
        
        if not (logs := read('__Process_.log_', operation_file=operation_file)):
            raise RuntimeError('Log Error: can not read logs')
        
        logs.append(f'<{datetime.datetime.now()}>[{codes[level]}]: {info}')
        
        if not write('__logs__', logs, operation_file=operation_file):
            raise RuntimeError('Log Error: can not write logs')
    
    @staticmethod
    def encrypte(seed: str, value: str, operation_file: str) -> str:
        
        r"""
        """
        
        def _encrypte(seed: str, value: str) -> str:
            key = (lambda s, l: bytes([hashlib.sha256(s.encode()).digest()[i % 32] for i in range(l)]))(seed, len(value))
            encrypted_bytes = bytes([b ^ k for b, k in zip(value.encode(), cycle(key))])
            return encrypted_bytes.hex()
        
        return _encrypte(seed, value)
    
    @staticmethod  
    def decrypte(seed: str, value: str, operation_file: str) -> str:

        r"""
        """
        
        def _decrypte(seed: str, value: str) -> str:
            key = (lambda s, l: bytes([hashlib.sha256(s.encode()).digest()[i % 32] for i in range(l)]))(seed, len(bytes.fromhex(value)))
            decrypted_bytes = bytes([b ^ k for b, k in zip(bytes.fromhex(value), cycle(key))])
            return decrypted_bytes.decode()

        return _decrypte(seed, value)

r"""
Public(ss)
"""

def inner_ss(operation_file: str = None):
    
    r"""
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open show console', 2, operation_file)
    
    print(f'SimpSave Info:\n'
          '')
    

def description_ss(operation_file: str = None):

    r"""
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open description console', 2, operation_file)
    
    print(f'Description for SimpSave at {operation_file}:\n\n{read('__description__', operation_file = operation_file)}')
    
    new_des = input(f'\nIf you want to rewrite, enter words that start with "rewrite>>>des:" as prefix (will be remove in final input)>>')
    if new_des.startswith('rewrite>>>des:'):
        new_des = new_des.replace('rewrite>>>des:', '', 1)
        if _Process_.force_write('_description_', new_des, operation_file):
            _Process_.update(operation_file)
            _Process_.log(f'Update new description: {new_des}', 1, operation_file)
            print('Descripton updated')
        else:
            _Process_.log(f'Write fail while update new description', 0, operation_file)
            print('Can not write new description')
    
def log_ss(operation_file: str = None, once_show:int = 5, contain_err = True, contain_ipt = True, contain_std = True):

    r"""
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open log console', 2, operation_file)
    
def delete_ss(operation_file: str = None, safe = True):
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    _Checker_.file_exists(operation_file)
    
    if safe:
        _Checker_.full_ready()
    
    _Process_.log('Open remove console', 2, operation_file)
        
    print(f'Prepare removing: {operation_file}')

    if not safe:
        print('::ALERT:: SAFE DELETE DISABLED' *3 +'\n')
        
    if input('Are you sure to remove? All data will be delete (y)') == 'y':
        
        if read('__delete__', operation_file) != True:
            _Process_.force_write('__delete__', True, operation_file)
            input('The delete lock has been closed. Enter the console again to confirm delete>>')
            _Process_.log('Delete lock disabled', 1, operation_file)
            return
        
        if safe:
            if len(read('__lock__', operation_file = operation_file)) != 0:
                _Process_.log(f'Clear Console: Interrupt unsafe operation: There is still a lock in SimpSave', 0, operation_file)
                raise RuntimeError('Cannot remove: The lock in SimpSave has not been cleared. Clear all locks or set safe=False')
            
            if len(match("", operation_file)) != 0:
                _Process_.log(f'Delete Console: Interrupt unsafe operation: There is still a section in SimpSave', 0, operation_file)
                raise RuntimeError('Cannot remove: The lock in SimpSave has not been cleared. Clear all locks or set safe=False')
                        
        os.remove(operation_file)

        if os.path.exists(operation_file):
            print('Failed to Remove')
            _Process_.log('Attempt to Remove SS, but failed', 0, operation_file)
            _Process_.update(operation_file)
        else:
            print('Remove Success')
    else:
        _Process_.force_write('__delete__', False)

r"""
Public
"""
def ready(operation_file: str = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if not os.path.exists(operation_file):
        return False
    
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
    for reserved in _RESERVED_:
        if not config.has_section(reserved):
            return False

    return True


def init(description: str = "" , preset_keys: None | str | list[str] = None, preset_values: None | any | list[any] = None, preset_annotations: None | str | list[str, None] = None, preset_encryptes: None | str | list[str, None] = None, /, overwrite_check: bool = True, operation_file: str = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if _Checker_.file_exists(operation_file) and overwrite_check:
        raise FileExistsError(f'Overwrite Check enabled: {operation_file} already exists')
    
    have_preset = True
    if preset_keys is None or preset_values is None:
        have_preset = False
    
    if isinstance(preset_keys, str):
        preset_keys = [preset_keys]
        preset_values = [preset_values]
        
    if isinstance(preset_annotations, str):
        preset_annotations = [preset_annotations]
        
    if preset_annotations is not None and not have_preset:
        _Process_.log('Attmpt to init with annotation preset when None preset keys and values were input', 0, operation_file)
        raise ValueError('Can not init with annotation preset when None preset keys and values were input')
        
    if isinstance(preset_encryptes, str):
        preset_encryptes = [preset_encryptes]
        
    if preset_encryptes is not None and not have_preset:
        _Process_.log('Attmpt to init with encryote preset when None preset keys and values were input', 0, operation_file)
        raise ValueError('Can not init with encrypte preset when None preset keys and values were input')

    with open(operation_file, 'w', encoding='utf-8') as file:
        
        if not _Process_.force_write(['__build__', '__path__', '__descripiton__', '__log__', '__file__', '__lock__', '__delete__'], [datetime.datetime.now(), os.getcwd(), description, [], operation_file, []], operation_file, False):
            raise RuntimeError('SimpSave: Failed to load init data')
        
        _Process_.update(operation_file)
        if have_preset and not write(preset_keys, preset_values, preset_annotations, preset_encryptes, overwrite=False, auto_init=False, operation_file=operation_file):
            return False
    
    _Process_.log(f'Init SimpSave in {operation_file} with description: {description} {'(Contain presets)' if have_preset else ''}', 1, operation_file)
    _Process_.update(operation_file)
    
    return True

def has(keys: str | list[str] = [], /, operation_file: str = None) -> bool | list[bool]:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    _Checker_.file_exists(operation_file)
    
    if isinstance(keys, str):
        keys = [keys]
        
    _Checker_.input_legal(keys)
    
    result_list = []
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
    
    for key in keys:
        result_list.append(config.has_section(key))
    
    _Process_.log(f'Exist check for section {keys}', 2, operation_file)
        
    return result_list if len(result_list) > 1 else result_list[0]

def read(keys: str | list[str], decryptes: None | str | list[str, None] = None, /, complete_dict = False, operation_file: str = None) -> any | list[any] | dict:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    _Checker_.file_exists(operation_file)
    
    if isinstance(keys, str):
        keys = [keys]
        decryptes = [decryptes]

    _Checker_.input_legal(keys, seeds=decryptes, operation_file=operation_file)
    
    result_list = []
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
    
    if decryptes is None:
        decryptes = [None for i in keys]

    for key,seed in zip(keys, decryptes):
        
        if not config.has_section(key):
            _Process_.log(f'Read interrupted while trying to read a not exist key', 0, operation_file)
            raise KeyError(f"Key Error: Section '{key}' not found in SimpSave.")
        
        section = config[key]
        
        try:
            value_type = section['type']
            value = section['value']
            annotation = section['annotation']
            update = section['update']
            create = section['create']
            edit_count = section['edit_count']
        except KeyError as error:
            _Process_.log(f'{key} incomplete: {error}', 0, operation_file)
            raise RuntimeError(f'Incomplete Section: {key}: {error}')

        if value_type not in _SUPPORTED_TYPES_:
            value_type = 'str'
            _Process_.log(f'Auto convert to string while reading: {value}', 1, operation_file)
        
        if seed is not None:
            value = _Process_.decrypte(seed, value, operation_file)
            
        if value_type != 'str':
            value = eval(f"{value_type}({value})")
            
        if complete_dict:    
            result_list.append({'value':value, 'type': value_type, 'annotation': annotation, 'update': update, 'create': create, 'edit_count': edit_count})
        else:
           result_list.append(value)
           
    _Process_.log(f"Read: {keys} {'<complete>' if complete_dict else ''}' {'<decrypte>' if decryptes is not None else ''}", 2, operation_file)
    return result_list if len(result_list) > 1 else result_list[0]

def write(keys: str | list[str], values: any | list[any],  annotations: None | str | list[str, None] = None, encryptes: None | str | list[str, None] = None, /, overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False, operation_file: str = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if not os.path.exists(operation_file) and auto_init:
        init(operation_file=operation_file)
        _Process_.log('Auto init while writing', 1, operation_file)
    else:
        _Checker_.file_exists()
        
    if isinstance(keys, str):
        keys = [keys]
        values = [values]
        annotations = [annotations]
        encryptes = [encryptes]

    _Checker_.input_legal(keys, values, annotations, seeds=encryptes, operation_file=operation_file)
    
    _Checker_.input_lock(keys, operation_file)
    
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
    
    if annotations is None:
        annotations = [None for i in keys]
    
    if encryptes is None:
        annotations = [None for i in keys]
        
    for key, value, annotation, encrypte in zip(keys, values, annotations, encryptes):
        
        value_type = type(value).__name__
        if value_type not in _SUPPORTED_TYPES_:
            if convert_unsupported:
                value = str(value)
            else:
                _Process_.log(f'Intterputed while writting an unsupported type value when auto_convert is False ({value}, {value_type})', 0, operation_file)
                raise TypeError(f"Unsupported Type: '{value_type}' is not supported. Supported types are: {_SUPPORTED_TYPES_}. Set convert_unsupported=True to convert.")
        
        if config.has_section(key):
            
            if not overwrite:
                _Process_.log(f'Intterupted while writting overwrite attmpt when overwrite is False', 0, operation_file)
                raise KeyError(f"Overwrite Error: Section '{key}' already exists. Set overwrite=True to overwrite.")
            
            section = config[key]
            
            if annotation is None:
                annotation = section['annotation']
                
            update = section['update']
            create = section['create']
            edit_count = int(section['edit_count']) + 1
            
            if type_check:
                
                old_type = f"{config[key]['type']}"
                
                if old_type != (value_type := type(value).__name__):
                    _Process_.log(f'Intterupted while writting mismatch type when type_check is True', 0, operation_file)
                    raise TypeError(f"Type Error: Value type mismatch for '{key}'. Expected {old_type}, but got {value_type}. Set type_check=False to ignore.")
        else:
            
            if annotation is None:
                annotation = ''
                
            update = create = str(datetime.datetime.now())
            edit_count = 0
        
        value = str(value)
        if encrypte is not None:
            value = _Process_.encrypte(encrypte, value, operation_file)
            
        config[key] = {'value': value, 'type': value_type, 'annotation': annotation, 'update': update, 'create': create, 'edit_count': edit_count}

    try:
        with open(operation_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except:
        _Process_.log(f'Fail to write: {keys}', 0, operation_file)
        return False
    
    _Process_.update(operation_file)
    _Process_.log(f'Write: {keys} {'<none annotation>' if annotation is None else ''} {'<encrypted>' if encryptes is None else ''}', 1, operation_file)
    
    return True

def remove(keys: str | list[str], /, operation_file: str = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)
        
    _Checker_.full_ready(operation_file)
    
    if isinstance(keys, str):
        keys = [keys]

    _Checker_.input_legal(keys, operation_file=operation_file)
    
    _Checker_.input_lock(keys, operation_file)
    
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
        
    for key in keys:
        
        if not config.has_section(key):
            _Process_.log(f'Remove intterupted while trying to remove a key that is not exist', 0, operation_file)
            raise KeyError(f"Key Error: Section '{key}' not found in SimpSave.")
        config.remove_section(key)

    with open(operation_file, 'w', encoding='utf-8') as configfile:
        try:
            config.write(configfile)
        except:
            return False
        
    _Process_.update(operation_file)
    _Process_.log(f'Remove {keys}', 1, operation_file)
    
    return True

def lock(keys: str | list[str], boolean_sequence: bool | list[bool], /, opeartion_file: str = None) -> bool:
    r"""
    """
    
    operation_file = _Process_.path_parser(operation_file)

    _Checker_.full_ready(operation_file)
    
    locks:list = read('__lock__', operation_file = operation_file)
    
    for key, bool_value in zip(keys, boolean_sequence):
        
        if key in locks and not bool_value:
            locks.remove(key)
            _Process_.log(f'Removed lock for "{key}"', 2, opeartion_file)
            
        elif key not in locks and bool_value:
            locks.append(key)
            _Process_.log(f'Add lock for "{key}"', 2, opeartion_file)
    
    if _Process_.force_write('__lock__', locks, operation_file):
        _Process_.update(opeartion_file)
        _Process_.log('Locks change applied', 1, opeartion_file)
        return True
    
    _Process_.log('Locks changes failed to apply', 0, opeartion_file)
    return False
    
def match(re_key: str, /, operation_file:str = None) -> list[dict]:
    r"""
    """
    
    operation_file = _Process_.path_parser(operation_file)

    _Checker_.full_ready(operation_file)
    
    config = configparser.ConfigParser()
    config.read(operation_file)
    
    pattern = re.compile(re_key)
    matching_sections = [section for section in config.sections() if pattern.match(section)]
    
    result = read(matching_sections, complete_dict=True, operation_file=operation_file)
    for unit,match in zip(result, matching_sections):
        unit['key'] = match
    
    _Process_.log(f'Match {len(result)} sections with regex pattern {re_key}', 2, operation_file)
    
    return result 
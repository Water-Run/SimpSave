"""
@file simpsave-beta.py
@author WaterRun
@version 1.0
@date 2024-11-04
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
from typing import List, Any, Optional, Union

_SIMPSAVE_DEFAULTPATH_ = '__ss__.ini' # Default filekey for the SimpSave INI file
_RESERVED_ = ('__path__', '__update__', '__build__', '__log__', '__description__', '__file__', '__lock__', '__delete__') # Reserved keys
_SUPPORTED_TYPES_ = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict') # Basic types that simpsave supported

r"""
Private
"""

class _Checker_:
    
    r"""
    Internal inspection static class
    """
    
    @staticmethod
    def input_legal(keys: Optional[List[str]] = None, values: Optional[List[Any]] = None,  annotations: Optional[List[Optional[str]]] = None, boolean_sequence: Optional[List[bool]] = None,  seeds: Optional[list[str]] = None, operation_file: Optional[str] = None):
        r"""
        Universal input validity check
        
        :param keys: Keys to be check. if None, not check
        :param values: Values to be check. if None, not check
        :param annotations: Annotations to be check. if None, not check
        :param boolean_sequence: Boolean_sequence to be check. if None, not check
        :param seeds: Seeds to be check. if None, not check
        :param operation_file: SimpSave instance for executing operations
        :raise TypeError: If any type check fails
        :raise ValueError: If any value check fails
        """
        
        check_list = [] # Items that need to be check
        
        for name, target, type_limit in zip(['keys', 'annotations', 'boolean_sequence', 'seeds'], [keys, annotations, boolean_sequence, seeds], [str, Optional[str], Optional[str], Optional[bool]]):
            
            if target is not None:
                for unit in target:
                    if not isinstance(unit, type_limit):
                        _Process_.log(f'Input Checker:{name}, "{unit}" not {str(type_limit)}. In {target}', 0, operation_file)
                check_list.append(target)

        if values is not None:
            check_list.append(values)
            
        if len(check_list) == 0: 
            _Process_.log('Input checker have nothing to check', 0, operation_file)
            raise ValueError('Input checker fail due to have nothing to check')
        
        for check_unit in check_list: 
            if len(len_check:= check_unit) != len(len_compare := check_list[0]):
                _Process_.log(f'Input Chekcer: Length inconsistency ({len_check}:{len_compare})', 0, operation_file)
                raise ValueError(f'All input must have same length ({len_check}:{len_compare})')
        
    @staticmethod        
    def key_read_only(keys: List[str], operation_file: str):
        r"""
        Check if the specified key is read-only
        
        :param keys: keys to be check
        :param operation_file: SimpSave instance for executing operations
        :raise ValueError: If key is read-only (locked or reserved)
        """
            
        locks = read('__lock__', operation_file = operation_file)    
        for key in keys: 
            if key in locks:
                _Process_.log(f'Read Only Chekcer activated: "{key}" in {keys}', 0, operation_file)
                raise ValueError(f'Read Only Checker: operation denied for "{key}" (locked)')  

            if key in _RESERVED_:
                _Process_.log(f'Read Only Checker:Value, key in reserved. {key} in {keys}', 0, operation_file)
                raise ValueError(f'Read Only is reserved: {key} in {keys}. Reserved: {_RESERVED_}')

    @staticmethod
    def file_exists(path: str):
        r"""
        Check if the specified file exists
        
        :param path: Path to be check
        :raise FileNotFoundError: If path not found
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"'{path}' not found. Initialize SimpSave first.")

    @staticmethod
    def full_ready(path: str):
        
        r"""
        Check if SimpSave instance has been fully initialized and can be used normally
        
        :param path: Path to check
        :raise RuntimeError: If SimpSave not available 
        """
        
        if not ready(path):
            raise RuntimeError('Operation require full ready of SimpSave. Note: Init SimpSave using init(). ')
                
class _Process_:
    
    r"""
    Internal operation static class
    """
    
    @staticmethod
    def path_parser(path: Optional[str]) -> str:
        r"""
        Parse input to SimpSave path
        
        :param path: Path to be parse. If None, use default SimpSave path
        :raise KeyError: If path is not a .ini file
        :raise RunTimeError: If SimpSave is not correct installed using pip
        """
        
        if path is None: # Default
            path = _SIMPSAVE_DEFAULTPATH_
            
        if not path.endswith('.ini'):
            raise KeyError(f'Simpsave can only operate .ini file: {path} unsupported.')
        
        if path.startswith('::py?'):
            path = sys.exec_prefix + '\\ssdatas\\' + path.replace('::py?', '', 1)
        elif path.startswith('::ss?'):
            sspath = importlib.util.find_spec('simpsave')
            
            if sspath is not None and sspath.submodule_search_locations:
                path = sspath.submodule_search_locations[0] + '\\ssdatas\\' + path.replace('::ss?', '', 1)
            else:
                raise RuntimeError('Can not find the path of simpsave package. Have you installed using pip?')
        
        return path

    @staticmethod
    def write(keys: list[str], values: list[any], operation_file: str, annotations: Optional[List[Optional[str]]] = None):
        r"""
        Write to SimpSave file (Ignore any read-only protection)
        
        :param keys: Keys to be write
        :param values: Values to be write
        :param operation_file: SimpSave instance for executing operations
        :param annotations: Annotation to be write. If None, write empty string
        :raise Exception: If exception occured
        """
        if annotations is None:
            annotations = [None for i in keys]
            
        try:
            config = configparser.ConfigParser()
            config.read(operation_file, encoding='utf-8')
            for key, value, annotation in zip(keys, values, annotations):
                
                value_type = type(value).__name__
                if value_type not in _SUPPORTED_TYPES_:
                    value = str(value)
                    value_type = 'str'
                
                if config.has_section(key):
                    section = config[key]
                    annotation = section['annotation']
                    create = section['create']
                    edit_count = section['edit_count']
                    update = str(datetime.datetime.now())
                else:
                    if annotation is None:
                        annotation = ''
                    create = update = str(datetime.datetime.now())
                    edit_count = -1

                config[key] = {'type': value_type, 'value': value, 'annotation': annotation, 'update': update, 'create': create, 'edit_count': edit_count}
                with open(operation_file, 'w', encoding='utf-8') as configfile:
                    config.write(configfile)
                    
        except Exception as e:
            _Process_.log(f'Force write error: {e}', 0, operation_file)
            return False
        
        return True

    @staticmethod
    def update(operation_file: str) -> bool: 
        r"""
        Refresh SimpSave for the latest updates on internal fields
        
        :param operation_file:  SimpSave instance for executing operations
        :raise RuntimeError: If update failed
        """
        
        if not _Process_.write(['__update__'], [datetime.datetime.now()], operation_file):
            raise RuntimeError('SimpSave failed to update')

    @staticmethod
    def log(info: str, level: int, operation_file: str):
        r"""
        Update SimpSave log
        
        :param info: Info to be logged
        :param level: Log level(0: Error, 1: Important, 2: Standard)
        :raise ValueError: If log level out of range
        :raise RuntimeError: If fail to log
        """
        
        codes = ['ERR', 'IPT', 'STD']
        if level not in range(0,3):
            raise ValueError(f'Log level {level} out of range')
        
        config = configparser.ConfigParser()
        config.read(operation_file, encoding='utf-8')
        
        if not (config.has_section('__log__')):
            raise RuntimeError('Log Error: can not read logs')
        
        logs = eval(config['__log__']['value'])
        logs.append(f'<{datetime.datetime.now()}>[{codes[level]}]: {info}')  
        if not _Process_.write(['__log__'], [logs], operation_file=operation_file):
            raise RuntimeError('Log Error: can not write logs')
    
    @staticmethod
    def encrypte(seed: str, value: str, operation_file: str) -> str:
        r"""
        Encrypt specified SimpSave data
        
        :param seed: The encrypted key
        :param value: Encrypted content
        :param operation_file:  SimpSave instance for executing operations
        """
        
        def _encrypte(seed: str, value: str) -> str:
            key = (lambda s, l: bytes([hashlib.sha256(s.encode('utf-8')).digest()[i % 32] for i in range(l)]))(seed, len(value))
            encrypted_bytes = bytes([b ^ k for b, k in zip(value.encode('utf-8'), cycle(key))])
            return encrypted_bytes.hex()
        
        _Process_.log('Data encryptes', 2, operation_file)
        
        return _encrypte(seed, value)
    
    @staticmethod  
    def decrypte(seed: str, value: str, operation_file: str) -> str:
        r"""
        Decrypt specified SimpSave data
        
        :param seed: The decrypted key
        :param value: Decrypted content
        :param operation_file:  SimpSave instance for executing operations
        """
        
        def _decrypte(seed: str, value: str) -> str:
            encrypted_bytes = bytes.fromhex(value)
            key = (lambda s, l: bytes([hashlib.sha256(s.encode('utf-8')).digest()[i % 32] for i in range(l)]))(seed, len(encrypted_bytes))
            decrypted_bytes = bytes([b ^ k for b, k in zip(encrypted_bytes, cycle(key))])
            return decrypted_bytes.decode('utf-8', errors='ignore')

        _Process_.log('Data decryptes', 2, operation_file)
        
        return _decrypte(seed, value)

r"""
Public(ss)
"""

def info_ss(operation_file: Optional[str] = None):
    r"""
    SimpSave console for displaying internal informations
    
    :param operation_file: SimpSave instance for executing operations
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open show console', 2, operation_file)

    print(f'SimpSave Info:\n'
          f'File Name: {read('__file__', operation_file=operation_file)}\n'
          f'Work Path: {read('__path__', operation_file=operation_file)}\n'
          f'Description: {read('__description__', operation_file=operation_file)}\n'
          f'Build Time: {read('__build__', operation_file=operation_file)}\n'
          f'Latest Update : {read('__update__', operation_file=operation_file)}\n'
          f'Locks: {len(read('__lock__', operation_file=operation_file))} Logs: {len(read('__log__', operation_file=operation_file))}\n'
          f'Delete Protection : {'Disable' if read('__delete__', operation_file=operation_file) else 'Enable'}\n'
          f'--------------------------------------\n'
          f'Note:\n'
          f'[Reserved] {_RESERVED_}\n'
          f'[DEFAULT FILENAME] {_SIMPSAVE_DEFAULTPATH_}\n'
          f'[SUPPORT TYPES] {_SUPPORTED_TYPES_}')
    input('>>')
    

def description_ss(operation_file: Optional[str] = None):
    r"""
    SimpSave console for displaying and modifying description
    
    :param operation_file: SimpSave instance for executing operations
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open description console', 2, operation_file)
    
    print(f'Description for SimpSave at {operation_file}:\n\n{read('__description__', operation_file = operation_file)}')
    
    new_des = input(f'\nIf you want to rewrite, enter words that start with "rewrite>>>des:" as prefix (will be remove in final input)>>')
    if new_des.startswith('rewrite>>>des:'):
        new_des = new_des.replace('rewrite>>>des:', '', 1)
        if _Process_.write(['_description_'], [new_des], operation_file):
            _Process_.update(operation_file)
            _Process_.log(f'Update new description: {new_des}', 1, operation_file)
            print('Descripton updated')
        else:
            _Process_.log(f'Write fail while update new description', 0, operation_file)
            print('Can not write new description')
    input('>>')
    
def log_ss(operation_file: Optional[str] = None, /, once_show: int = 5, reverse: bool = True, contain_err: bool = True, contain_ipt: bool = True, contain_std: bool = True):
    r"""
    SimpSave console for displaying logs
    
    :param operation_file: SimpSave instance for executing operations
    """
    
    operation_file = _Process_.path_parser(operation_file)
    
    _Checker_.full_ready(operation_file)
    
    _Process_.log('Open log console', 2, operation_file)
    
    print(f'SimpSave Log(s)\n {operation_file}\n'
          f'Show: {'ERR' if contain_err else ''} {'IPT' if contain_ipt else ''} {'STD' if contain_std else ''} | Once:{once_show} {'(Reverse)' if reverse else ''}\n')
    
    logs = read('__log__', operation_file)
    
    full_length = len(logs)
    for log in logs:
        
        if not contain_err and log.count('ERR') != 0:
            logs.remove(log)
        if not contain_ipt and log.count('IPT') != 0:
            logs.remove(log)
        if not contain_std and log.count('STD') != 0:
            logs.remove(log)
    
    if reverse:
        logs.reverse()
        
    print(f'Result: {(now_length := len(logs))}/{full_length}')
    
    count = 0
    for log in logs:
        count +=1
        print(log)
        if count % once_show == 0:
            input(f'{count}/{now_length}>>')
    input('>>')
    
def clear_ss(operation_file: Optional[str] = None, /, safe: bool = True):
    r"""
    SimpSave console for deleting
    
    :param operation_file: SimpSave instance for executing operations
    """

    operation_file = _Process_.path_parser(operation_file)
    _Checker_.file_exists(operation_file)
    
    if safe:
        _Checker_.full_ready(operation_file)
    
    _Process_.log('Open remove console', 2, operation_file)
        
    print(f'Prepare removing: {operation_file}')

    if not safe:
        print('::ALERT:: SAFE DELETE DISABLED\t' * 3 +'\n')
        
    if input('Are you sure to remove? All data will be delete (y)>>') == 'y':
        
        if read('__delete__', operation_file) != True:
            _Process_.write('__delete__', True, operation_file)
            input('The delete lock has been closed. Enter the console again to confirm delete>>')
            _Process_.log('Delete lock disabled', 1, operation_file)
            return
        
        if safe:
            if len(read('__lock__', operation_file = operation_file)) != 0:
                _Process_.log(f'Clear Console: Interrupt unsafe operation: There is still a lock in SimpSave', 0, operation_file)
                raise RuntimeError('Cannot remove: The lock in SimpSave has not been cleared. Clear all locks or set safe=False')
            
            # todo
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
        _Process_.write(['__delete__'], [False], operation_file=operation_file)
    input('>>')
    
r"""
Public
"""
def ready(operation_file: Optional[str] = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if not os.path.exists(operation_file):
        return False
    
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')
    for reserved in _RESERVED_:
        if not config.has_section(reserved):
            print(reserved)
            return False

    return True


def init(description: str = "Default SimpSave instance description. " , preset_keys: Optional[Union[str,list[str]]] = None, preset_values: Optional[Union[any,list[any]]] = None, preset_annotations: Optional[Union[str,Optional[List[Optional[str]]]]] = None, preset_encryptes: Optional[Union[str,List[Optional[str]]]] = None, /, overwrite_check: bool = True, operation_file: Optional[str] = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if os.path.exists(operation_file) and overwrite_check:
        raise FileExistsError(f'Overwrite Check enabled: {operation_file} already exists')
    
    have_preset = not preset_keys is None
        
    with open(operation_file, 'w', encoding='utf-8') as file:
        
        file.write('')
        
        if not _Process_.write(['__build__', '__path__', '__description__', '__log__', '__file__', '__lock__', '__delete__', '__update__'], [datetime.datetime.now(), os.getcwd(), description, [], operation_file, [], False, datetime.datetime.now()], operation_file, ['SimpSave initialization time', 'SimpSave instance path', 'SimpSave instance description', 'SimpSave instance log', 'SimpSave instance filename', 'SimpSave key locks', 'SimpSave delete protection', 'SimpSave update time']):
            raise RuntimeError('SimpSave: Failed to load init data')
        
        _Process_.update(operation_file)
        if have_preset and not write(preset_keys, preset_values, preset_annotations, preset_encryptes, overwrite=False, auto_init=False, operation_file=operation_file):
            return False
    
    _Process_.log(f'Init SimpSave in {operation_file} with description: {description} {'(Contain presets)' if have_preset else ''}', 1, operation_file)
    _Process_.update(operation_file)
    
    return True

def has(keys: Union[str,list[str]] = [], /, operation_file: Optional[str] = None) -> Union[bool,list[bool]]:
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
    
    return result_list if len(result_list) > 1 else result_list[0]

def read(keys: Union[str,list[str]], decryptes: Optional[Union[str,List[Optional[str]]]] = None, /, complete_dict: bool = False, operation_file: Optional[str] = None) -> Union[any,list[any],dict]:
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
           
    return result_list if len(result_list) > 1 else result_list[0]

def write(keys: Union[str,list[str]], values: Union[any,list[any]],  annotations: Optional[Union[str,List[Optional[str]]]] = None, encryptes: Optional[Union[str,List[Optional[str]]]] = None, /, overwrite: bool = True, auto_init: bool = False, type_check: bool = False, convert_unsupported: bool = False, operation_file: Optional[str] = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)

    if not os.path.exists(operation_file) and auto_init:
        init(operation_file=operation_file)
        _Process_.log('Auto init while writing', 1, operation_file)
    else:
        _Checker_.file_exists(operation_file)
        
    if isinstance(keys, str):
        keys = [keys]
        values = [values]
        annotations = [annotations]
        encryptes = [encryptes]

    _Checker_.input_legal(keys, values, annotations, seeds=encryptes, operation_file=operation_file)
    
    _Checker_.key_read_only(keys, operation_file)
    
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
            value = _Process_.encrypte(encrypte, str(value), operation_file)
            
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

def remove(keys: Union[str,list[str]], /, operation_file: Optional[str] = None) -> bool:
    r"""
    """

    operation_file = _Process_.path_parser(operation_file)
        
    _Checker_.full_ready(operation_file)
    
    if isinstance(keys, str):
        keys = [keys]

    _Checker_.input_legal(keys, operation_file=operation_file)
    
    _Checker_.key_read_only(keys, operation_file)
    
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

def lock(keys: Union[str,list[str]], boolean_sequence: Union[bool,list[bool]], /, opeartion_file: Optional[str] = None) -> bool:
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
    
    if _Process_.write('__lock__', locks, operation_file):
        _Process_.update(opeartion_file)
        _Process_.log('Locks change applied', 1, opeartion_file)
        return True
    
    _Process_.log('Locks changes failed to apply', 0, opeartion_file)
    return False
    
def match(re_key: str, /, operation_file: Optional[str] = None) -> list[dict]:
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
       
    return result 
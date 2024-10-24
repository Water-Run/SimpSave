"""
@file simpsave.py
@author WaterRun
@version 0.13
@date 2024-10-23
@description Source code of simpsave project
"""

import os
import configparser
from typing import List, Any, Union

SIMPSAVE_FILENAME = '__ss__.ini'  # Default filename for the SimpSave INI file

def ready() -> bool:
    """
    Check if the SimpSave INI file exists.
    
    :return: True if the file exists, False otherwise.
    """
    return os.path.exists(SIMPSAVE_FILENAME)

def clear_ss() -> bool:
    """
    Delete the SimpSave INI file in the current directory.
    
    :return: True if the file was successfully deleted, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    """
    if not ready():
        raise FileNotFoundError(f"Initialization Error: '{SIMPSAVE_FILENAME}' not found. Please initialize SimpSave first.")
    
    os.remove(SIMPSAVE_FILENAME)
    return not ready()

def init(names: Union[str, List[str]] = [], values: Union[str, List[str]] = [], init_check: bool = False) -> bool:
    """
    Initialize SimpSave by creating the INI file and writing preset data.
    
    :param names: List of keys (or a single key) to be written.
    :param values: List of corresponding values (or a single value) to be written.
    :param init_check: If True, raises FileExistsError if the .ini file exists.
    :return: True if initialization was successful, False otherwise.
    :raises FileExistsError: If the INI file already exists and init_check is True.
    :raises ValueError: If `names` or `values` are not lists or their lengths don't match.
    """
    if ready() and init_check:
        raise FileExistsError(f"Initialization Error: '{SIMPSAVE_FILENAME}' already exists. Set `init_check=False` to overwrite.")

    if isinstance(names, str):
        names = [names]
        values = [values]
    
    if not isinstance(names, list) or not isinstance(values, list):
        raise ValueError("Both 'names' and 'values' must be lists or single strings.")
    
    if len(names) != len(values):
        raise ValueError(f"Mismatch Error: 'names' and 'values' must have the same length. Got {len(names)} names and {len(values)} values.")
    
    with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as file:
        file.write('')
        for name, value in zip(names, values):
            if not write(name, value, overwrite=False, auto_init=True):
                return False
    return True

def has(name: str) -> bool:
    """
    Check if a section with the given name exists in the INI file.
    
    :param name: The section name to check.
    :return: True if the section exists, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises TypeError: If 'name' is not a string.
    """
    if not ready():
        raise FileNotFoundError(f"File Error: '{SIMPSAVE_FILENAME}' not found. Initialize SimpSave first.")
    
    if not isinstance(name, str):
        raise TypeError(f"Type Error: 'name' must be a string, not {type(name).__name__}.")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')
    return config.has_section(name)

def read(names: Union[str, List[str]]) -> Union[Any, List[Any]]:
    """
    Read and return the values associated with the given section name(s).
    
    :param names: The section name or list of section names to read.
    :return: The value(s) of the specified section(s).
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If a section does not exist.
    :raises TypeError: If the value's type is unsupported or 'names' is not a string/list.
    """
    if not ready():
        raise FileNotFoundError(f"File Error: '{SIMPSAVE_FILENAME}' not found. Initialize SimpSave first.")

    if isinstance(names, str):
        names = [names]
    
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise TypeError(f"Type Error: 'names' must be a list of strings or a single string.")
    
    result_list = []
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')

    for name in names:
        if not config.has_section(name):
            raise KeyError(f"Key Error: Section '{name}' not found in SimpSave.")
        
        section = config[name]
        value_type = section['type']
        value_str = section['value']

        supported_types = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict')
        if value_type not in supported_types:
            raise TypeError(f"Unsupported Type: '{value_type}' is not supported. Supported types are: {supported_types}")
        
        result_list.append(eval(f"{value_type}({value_str})"))

    return result_list if len(result_list) > 1 else result_list[0]

def write(names: Union[str, List[str]], values: Union[Any, List[Any]], overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False) -> bool:
    """
    Write values to sections with the specified names.
    
    :param names: The section name(s) to write to.
    :param values: The value(s) to write.
    :param overwrite: If False, prevents overwriting existing sections.
    :param auto_init: Automatically initializes SimpSave if not already initialized.
    :param type_check: Ensures type consistency with existing sections.
    :param convert_unsupported: If True, unsupported types are converted to strings.
    :return: True if the write was successful, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If overwrite is disabled and a section already exists.
    :raises TypeError: If a value's type is unsupported or does not match existing data type.
    """
    if not ready() and auto_init:
        init()
    elif not ready():
        raise FileNotFoundError(f"File Error: '{SIMPSAVE_FILENAME}' not found. Initialize SimpSave or set auto_init=True.")
    
    if isinstance(names, str):
        names = [names]
        values = [values]
    
    if len(names) != len(values):
        raise ValueError(f"Mismatch Error: 'names' and 'values' must have the same length. Got {len(names)} names and {len(values)} values.")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')

    supported_types = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict')

    for name, value in zip(names, values):
        if not isinstance(name, str):
            raise TypeError(f"Type Error: 'name' must be a string, not {type(name).__name__}.")
        
        value_type = type(value).__name__
        if value_type not in supported_types:
            if convert_unsupported:
                value = str(value)
            else:
                raise TypeError(f"Unsupported Type: '{value_type}' is not supported. Supported types are: {supported_types}. Set convert_unsupported=True to convert.")
        
        if overwrite is False and config.has_section(name):
            raise KeyError(f"Overwrite Error: Section '{name}' already exists. Set overwrite=True to overwrite.")
        
        if type_check and config.has_section(name):
            old_value = eval(f"{config[name]['type']}({config[name]['value']})")
            if type(old_value) is not type(value):
                raise TypeError(f"Type Error: Value type mismatch for '{name}'. Expected {type(old_value).__name__}, but got {value_type}. Set type_check=False to ignore.")
        
        config[name] = {'type': value_type, 'value': str(value)}

    with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    
    return True

def remove(names: Union[str, List[str]]) -> bool:
    """
    Remove section(s) from the SimpSave INI file.
    
    :param names: The section name or list of section names to remove.
    :return: True if all specified sections were successfully removed, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If a section does not exist.
    :raises TypeError: If 'names' is not a string or list of strings.
    """
    if not ready():
        raise FileNotFoundError(f"File Error: '{SIMPSAVE_FILENAME}' not found. Initialize SimpSave first.")
    
    if isinstance(names, str):
        names = [names]
    
    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise TypeError(f"Type Error: 'names' must be a list of strings or a single string.")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')

    for name in names:
        if not config.has_section(name):
            raise KeyError(f"Key Error: Section '{name}' not found in SimpSave.")
        config.remove_section(name)

    with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    
    return True

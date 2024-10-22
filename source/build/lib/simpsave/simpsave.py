"""
@file simpsave.py
@author WaterRun
@version 0.11
@date 2024-10-22
@description Source code for the SimpSave project
"""

import os
import configparser

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
        raise FileNotFoundError(f"SimpSave has not been initialized: {SIMPSAVE_FILENAME} not found")
    return os.remove(SIMPSAVE_FILENAME)

def init(names: list[str] = [], values: list[str] = [], init_check = False) -> bool:
    """
    Initialize SimpSave by creating the INI file and writing preset data.
    
    :param names: List of keys to be written.
    :param values: List of corresponding values to be written.
    :param init_check: If True, raise FileExistsError while .ini exists.
    :return: True if initialization was successful, False otherwise.
    :raises FileExistsError: If the INI file already exists.
    :raises ValueError: If `names` or `values` are not lists.
    :raises IndexError: If the lengths of `names` and `values` do not match.
    """
    if ready() and init_check:
        raise FileExistsError(f"Init Check: SimpSave has already been initialized: {SIMPSAVE_FILENAME} exists")
    
    if isinstance(names, str): # auto convert
        names = [names]
        values = [values]
        
    if not isinstance(names, list) or not isinstance(values, list):
        raise ValueError('Expected two lists for names and values')

    if len(names) != len(values):
        raise IndexError(f"Length of names and values must be equal (names: {len(names)}, values: {len(values)})")

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
    """
    if not ready():
        raise FileNotFoundError(f"SimpSave has not been initialized: {SIMPSAVE_FILENAME} not found")

    if not isinstance(name, str):
        raise TypeError(f"The name must be string: {name}")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')
    return config.has_section(name)

def read(name: str) -> any:
    """
    Read and return the value associated with the given section name.
    
    :param name: The section name to read.
    :return: The value of the specified section.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If the section does not exist.
    :raises TypeError: If the value's type is not supported.
    """
    if not ready():
        raise FileNotFoundError(f"SimpSave has not been initialized: {SIMPSAVE_FILENAME} not found")

    if not isinstance(name, str):
        raise TypeError(f"The name must be string: {name}")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')

    if name not in config:
        raise KeyError(f"Section {name} not found")

    section = config[name]
    type_str = section['type']
    value_str = section['value']

    supported_types = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict')
    if type_str not in supported_types:
        raise TypeError(f"SimpSave only supports types in {supported_types}")

    if type_str == 'str':
        return value_str
    return eval(f"{type_str}({value_str})")

def write(name: str, value: any, overwrite=True, auto_init=True, type_check=True, convert_unsupported=False) -> bool:
    """
    Write a value to a section with the specified name.
    
    :param name: The section name to write to.
    :param value: The value to write.
    :param overwrite: If False, prevents overwriting existing sections.
    :param auto_init: Automatically initializes SimpSave if not already initialized.
    :param type_check: Ensures type consistency with existing sections.
    :param convert_unsupported: If True, unsupported types are converted to strings.
    :return: True if the write was successful, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If overwrite is disabled and the section already exists.
    :raises TypeError: If the value's type is not supported or does not match existing data type.
    """
    if not ready() and auto_init:
        init()
    elif not ready():
        raise FileNotFoundError(f"SimpSave has not been initialized: {SIMPSAVE_FILENAME} not found")

    if not isinstance(name, str):
        raise TypeError(f"The name must be string: {name}")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')

    if not overwrite and has(name):
        raise KeyError(f"Overwrite disabled: Section {name} already exists")
    
    supported_types = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict')
    value_type = type(value).__name__

    if value_type not in supported_types:
        if convert_unsupported:
            value = str(value)
        else:
            raise TypeError(f"SimpSave only supports types in {supported_types}")

    if type_check and has(name):
        old_value = read(name)
        if type(old_value) != type(value):
            raise TypeError(f"Type mismatch: {value_type} given, but {type(old_value).__name__} expected")

    config[name] = {
        'type': value_type,
        'value': str(value)
    }

    with open(SIMPSAVE_FILENAME, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    return True

def remove(name: str) -> bool:
    """
    Remove a section with the specified name from the INI file.
    
    :param name: The section name to remove.
    :return: True if the section was successfully removed, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    """
    if not ready():
        raise FileNotFoundError(f"SimpSave has not been initialized: {SIMPSAVE_FILENAME} not found")

    if not isinstance(name, str):
        raise TypeError(f"The name must be string: {name}")
    
    config = configparser.ConfigParser()
    config.read(SIMPSAVE_FILENAME, encoding='utf-8')
    return config.remove_section(name)

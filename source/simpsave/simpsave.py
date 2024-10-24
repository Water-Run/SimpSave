"""
@file simpsave.py
@author WaterRun
@version 0.20
@date 2024-10-23
@description Source code of simpsave project
"""

import os
import configparser
from typing import List, Any, Union

SIMPSAVE_FILENAME = 'ss.ini' # Default filename for the SimpSave INI file

def ready(operation_file: str = None) -> bool:
    """
    Check if the SimpSave INI file exists.
    asciidoc

    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :raise NameError: If operation_file isn't an INI file. 
    :return: True if the file exists, False otherwise.
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   
        
    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')
        
    return os.path.exists(operation_file)

def clear_ss(operation_file: str = None) -> bool:
    """
    Delete the SimpSave INI file in the current directory.
    basic

    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: True if the file was successfully deleted, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   
        
    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')
        
    if not ready(operation_file=operation_file):
        raise FileNotFoundError(f"Initialization Error: '{operation_file}' not found. Please initialize SimpSave first.")

    os.remove(operation_file)
    return not ready(operation_file=operation_file)

def init(names: Union[str, List[str]] = [], values: Union[any, List[any]] = [], init_check: bool = True, operation_file: str = None) -> bool:
    """
    Initialize SimpSave by creating the INI file and writing preset data.
    asciidoc

    :param names: List of keys (or a single key) to be written.
    :param values: List of corresponding values (or a single value) to be written.
    :param init_check: If True, raises FileExistsError if the .ini file exists.
    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: True if initialization was successful, False otherwise.
    :raises FileExistsError: If the INI file already exists and init_check is True.
    :raises ValueError: If `names` or `values` are not lists or their lengths don't match.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   

    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')

    if ready(operation_file=operation_file) and init_check:
        raise FileExistsError(f"Initialization Error: '{operation_file}' already exists. Set `init_check=False` to overwrite.")

    if isinstance(names, str):
        names = [names]
        values = [values]
        
    if not all(isinstance(name, str) for name in names):
        raise ValueError(f'All input name must be string: {names}')

    if not isinstance(names, list) or not isinstance(values, list):
        raise ValueError("Both 'names' and 'values' must be lists or single strings.")

    if len(names) != len(values):
        raise ValueError(f"Mismatch Error: 'names' and 'values' must have the same length. Got {len(names)} names and {len(values)} values.")

    with open(operation_file, 'w', encoding='utf-8') as file:
        file.write('')
        for name, value in zip(names, values):
            if not write(name, value, overwrite=False, auto_init=True, operation_file=operation_file):
                return False
    return True

def has(names: Union[str, List[str]] = [], operation_file: str = None) -> Union[bool, list[bool]]:
    """
    Check if a section with the given name exists in the INI file.
    asciidoc

    :param name: The section name or list of section names to check.
    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: A list of (or single) True if the section exists, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises TypeError: If 'name' is not a string.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   

    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')

    if not ready(operation_file=operation_file):
        raise FileNotFoundError(f"File Error: '{operation_file}' not found. Initialize SimpSave first.")

    if isinstance(names, str):
        names = [names]
        values = [values]
        
    if not all(isinstance(name, str) for name in names):
        raise ValueError(f'All input name must be string: {names}')

    if not isinstance(names, list) or not isinstance(values, list):
        raise ValueError("Both 'names' and 'values' must be lists or single strings.")

    if len(names) != len(values):
        raise ValueError(f"Mismatch Error: 'names' and 'values' must have the same length. Got {len(names)} names and {len(values)} values.")

    result_list = []
    for name in names:
        config = configparser.ConfigParser()
        config.read(operation_file, encoding='utf-8')
        result_list.append(config.has_section(name))
        
    return result_list if len(result_list) > 1 else result_list[0]

def read(names: Union[str, List[str]], operation_file: str = None) -> Union[Any, List[Any]]:
    """
    Read and return the values associated with the given section name(s).
    asciidoc

    :param names: The section name or list of section names to read.
    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: The value(s) of the specified section(s).
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If a section does not exist.
    :raises TypeError: If the value's type is unsupported or 'names' is not a string/list.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME    

    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')

    if not ready(operation_file=operation_file):
        raise FileNotFoundError(f"File Error: '{operation_file}' not found. Initialize SimpSave first.")

    if isinstance(names, str):
        names = [names]

    if not all(isinstance(name, str) for name in names):
        raise ValueError(f'All input name must be string: {names}')

    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise TypeError(f"Type Error: 'names' must be a list of strings or a single string.")

    result_list = []
    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')

    for name in names:
        if not config.has_section(name):
            raise KeyError(f"Key Error: Section '{name}' not found in SimpSave.")
        
        section = config[name]
        value_type = section['type']
        value_str = section['value']

        supported_types = ('int', 'float', 'bool', 'str', 'list', 'tuple', 'dict')
        if value_type not in supported_types:
            raise TypeError(f"Unsupported Type: '{value_type}' is not supported. Supported types are: {supported_types}")
        
        result_list.append(f'{value_str}') if value_type == 'str' else result_list.append(eval(f"{value_type}({value_str})"))

    return result_list if len(result_list) > 1 else result_list[0]

def write(names: Union[str, List[str]], values: Union[Any, List[Any]], overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False, operation_file: str = None) -> bool:
    """
    Write values to sections with the specified names.
    asciidoc

    :param names: The section name(s) to write to.
    :param values: The value(s) to write.
    :param overwrite: If False, prevents overwriting existing sections.
    :param auto_init: Automatically initializes SimpSave if not already initialized.
    :param type_check: Ensures type consistency with existing sections.
    :param convert_unsupported: If True, unsupported types are converted to strings.
    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: True if the write was successful, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If overwrite is disabled and a section already exists.
    :raises TypeError: If a value's type is unsupported or does not match existing data type.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   

    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')

    if not ready(operation_file=operation_file) and auto_init:
        init(operation_file=operation_file)
    elif not ready(operation_file=operation_file):
        raise FileNotFoundError(f"File Error: '{operation_file}' not found. Initialize SimpSave or set auto_init=True.")

    if isinstance(names, str):
        names = [names]
        values = [values]

    if not all(isinstance(name, str) for name in names):
        raise ValueError(f'All input name must be string: {names}')

    if len(names) != len(values):
        raise ValueError(f"Mismatch Error: 'names' and 'values' must have the same length. Got {len(names)} names and {len(values)} values.")

    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')

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
        
        if overwrite == False and config.has_section(name):
            raise KeyError(f"Overwrite Error: Section '{name}' already exists. Set overwrite=True to overwrite.")
        
        if type_check and config.has_section(name):
            old_type = f"{config[name]['type']}"
            if old_type != (value_type := type(value).__name__):
                raise TypeError(f"Type Error: Value type mismatch for '{name}'. Expected {old_type}, but got {value_type}. Set type_check=False to ignore.")
        
        config[name] = {'type': value_type, 'value': str(value)}

    try:
        with open(operation_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
    except:
        return False
        
    return True

def remove(names: Union[str, List[str]], operation_file: str = None) -> bool:
    """
    Remove section(s) from the SimpSave INI file.
    basic

    :param names: The section name or list of section names to remove.
    :param operation_file: Simsave INI file for storage and manipulation. If None, using default SIMPSAVE_FILENAME.
    :return: True if all specified sections were successfully removed, False otherwise.
    :raises FileNotFoundError: If the INI file does not exist.
    :raises KeyError: If a section does not exist.
    :raises TypeError: If 'names' is not a string or list of strings.
    :raise NameError: If operation_file isn't an INI file. 
    """

    if operation_file is None:
        operation_file = SIMPSAVE_FILENAME   
        
    if not operation_file.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {operation_file} unsupported.')
        
    if not ready(operation_file=operation_file):
        raise FileNotFoundError(f"File Error: '{operation_file}' not found. Initialize SimpSave first.")

    if isinstance(names, str):
        names = [names]

    if not all(isinstance(name, str) for name in names):
        raise ValueError(f'All input name must be string: {names}')

    if not isinstance(names, list) or not all(isinstance(name, str) for name in names):
        raise TypeError(f"Type Error: 'names' must be a list of strings or a single string.")

    config = configparser.ConfigParser()
    config.read(operation_file, encoding='utf-8')

    for name in names:
        if not config.has_section(name):
            raise KeyError(f"Key Error: Section '{name}' not found in SimpSave.")
        config.remove_section(name)

    with open(operation_file, 'w', encoding='utf-8') as configfile:
        try:
            config.write(configfile)
        except:
            return False

    return True
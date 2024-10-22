# SimpSave

## Introduction  
As the name suggests, SimpSave is an extremely lightweight Python library that provides a simple solution for variable persistence. It is particularly suitable for use in small scripts or student projects.

SimpSave offers the following features:  
- **Extremely Simple**: The project has less than 200 lines of code, making it easy to understand and use quickly.
- **Easy to Learn**: It requires only basic Python knowledge, with no need for complex tutorials. In most cases, users can learn to use the library within a minute.

> The project has been published on PyPi.

## Usage Guide  

### Installation  
- Install SimpSave via `pip`:  
  ```bash
  pip install simpsave
  ```

- Import SimpSave into your code (usually as `ss`):  
  ```python
  import simpsave as ss
  ```

### Basic Concepts  
SimpSave supports the persistent storage of basic Python data types, including `int`, `float`, `bool`, `str`, as well as `list`, `tuple`, and `dict`. It provides basic operations like create, read, update, and delete.  
> For non-basic types, if the object implements a `__str__()` method, you can set the `convert_unsupported` parameter to `True` to store it as a string.

SimpSave’s methods make it easy to achieve data persistence. First, you need to check if SimpSave is ready (i.e., if the `.ini` file exists). If not, you need to initialize it:  
- Use `ss.ready()` to check if SimpSave is ready (i.e., if the `.ini` file exists).
- If not initialized, use the `ss.init()` method to initialize it. You can pass in `names` and `values` lists to set initial key-value pairs. The two lists must correspond one-to-one and have the same length.

SimpSave provides the following core functionalities:  
- `write()` to write data into the `.ini` file.
- `read()` to read stored data.
- `remove()` to delete specific data.
- `has()` to check if a specific key exists.
- `clear_ss()` to clear SimpSave by deleting the `.ini` file.

By default, SimpSave uses `__ss__.ini` as the storage file name, but you can change the file name by modifying the global variable `SIMPSAVE_FILENAME`.

Here’s a simple code example:  
```python
import simpsave as ss  # Import SimpSave with the alias ss

# Prepare data
name = 'Hello World'
value = 'Hello World!'

# Initialize SimpSave and write data (auto convert to two list)
ss.init(name, value)

"""
The above code is equivalent to (if auto_init = True)
ss.write(name, value)
"""

# Read and print the stored value
print(ss.read(name))  # Output: Hello World!
```

The name of a SimpSave storage unit can be any string, but ensure uniqueness to avoid conflicts.

For more detailed function usage and explanations, check the library overview below. You can also visit the GitHub project page to download sample code and explore this simple, easy-to-use library further.

## Library Overview  

### 1. Variables  
- `SIMPSAVE_FILENAME`: A `str` type variable, defaulting to `__ss__.ini`, controls the name of the `.ini` file used for storage. Make sure to include the `.ini` suffix when modifying this variable.

### 2. Functions  

#### `ready()`  
- **Description**: Checks whether SimpSave is initialized, i.e., whether the `.ini` file exists.  
- **Returns**: `True` if the file exists, `False` if it does not.  
- **Exceptions**: None.  
- **Example**:  
  ```python
  if ss.ready():
      print("SimpSave is ready!")
  ```

#### `init(names: list[str] = [] or str, values: list[str] = [] or any, init_check: bool = False)`  
- **Description**: Initializes SimpSave and can preset key-value pairs (if single key-value, auto convert) during creation.  
- **Parameters**:  
  - `names`: A list of strings (or single string) representing key names.  
  - `values`: A list (or single value, if name is single string) of strings representing key values.  
  - `init_check`: If set to `True`, throws a `FileExistsError` if SimpSave already exists.  
- **Returns**: `True` if initialization is successful.  
- **Exceptions**:  
  - `FileExistsError`: If the `.ini` file already exists and `init_check` is `True`.  
  - `ValueError`: If `names` and `values` are not lists.  
  - `IndexError`: If the `names` and `values` lists have different lengths.  
- **Example**:  
  ```python
  ss.init(['key1'], ['value1'])
  ```

#### `write(name: str, value: any, overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False)`  
- **Description**: Writes the specified key-value pair into SimpSave.  
- **Parameters**:  
  - `name`: The key name (string).  
  - `value`: The value (any supported type).  
  - `overwrite`: If set to `False`, throws a `KeyError` if the key already exists.  
  - `auto_init`: Automatically initializes if the `.ini` file does not exist.  
  - `type_check`: Checks type consistency and throws a `TypeError` if inconsistent.  
  - `convert_unsupported`: Whether to automatically convert unsupported types to strings.  
- **Returns**: `True` if the write is successful.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist and `auto_init` is `False`.  
  - `KeyError`: If `overwrite` is `False` and the key already exists.  
  - `TypeError`: If the type is unsupported or inconsistent with the existing key’s value, or input name isn't string.
- **Example**:  
  ```python
  ss.write('my_key', 123)
  ```

#### `read(name: str)`  
- **Description**: Reads the value associated with the specified key.  
- **Parameters**:  
  - `name`: The key name to read.  
- **Returns**: The value associated with the key.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist.  
  - `KeyError`: If the key does not exist.  
  - `TypeError`: If the value type is unsupported, or input name isn't string.  
- **Example**:  
  ```python
  value = ss.read('my_key')
  ```

#### `has(name: str)`  
- **Description**: Checks whether a specific key exists.  
- **Parameters**:  
  - `name`: The key name to check.  
- **Returns**: `True` if the key exists, `False` if it does not.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist.  
  - `TypeError`: If the input name isn't string.s
- **Example**:  
  ```python
  if ss.has('my_key'):
      print("Key exists!")
  ```

#### `remove(name: str)`  
- **Description**: Removes the specified key and its value.  
- **Parameters**:  
  - `name`: The key name to remove.  
- **Returns**: `True` if the removal is successful.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist.  
  - `KeyError`: If the key does not exist.  
  - `TypeError`: If the input name isn't string.
- **Example**:  
  ```python
  ss.remove('my_key')
  ```

#### `clear_ss()`  
- **Description**: Clears SimpSave by deleting the `.ini` file.  
- **Returns**: `True` if the deletion is successful.  
- **Exceptions**:  
  - `FileNotFoundError`: If the `.ini` file does not exist.  
- **Example**:  
  ```python
  ss.clear_ss()
  ```  
### Implementation

The core of SimpSave is built upon Python's `configparser` module, using an `.ini` file for persistent data storage. It manages Python's basic data types in a key-value pair format and supports simple data read/write operations.  
SimpSave is designed to be simple, lightweight, and easy to use, making it well-suited for small-scale projects, especially for student assignments.
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

### Library Overview  

#### 1. Variables  
- **`SIMPSAVE_FILENAME`**: A string variable that defaults to `__ss__.ini`, controlling the name of the file used for storage. Make sure to include the `.ini` suffix if you modify this variable.

#### 2. Functions  

##### `ready()`  
- **Description**: Checks if SimpSave is initialized by verifying the existence of the `.ini` file.  
- **Returns**: `True` if the file exists, `False` otherwise.  
- **Exceptions**: None.  
- **Example**:  

```python
if ss.ready():
    print("SimpSave is ready!")
```

##### `init(names: Union[list[str], str] = [], values: Union[list[Any], Any] = [], init_check: bool = False)`  
- **Description**: Initializes SimpSave and writes key-value pairs if provided. Handles both single key-value pairs and lists.  
- **Parameters**:  
  - `names`: A list of strings or a single string representing the key(s).  
  - `values`: A list of values or a single value corresponding to the key(s).  
  - `init_check`: If set to `True`, raises a `FileExistsError` if SimpSave already exists.  
- **Returns**: `True` if initialization succeeds.  
- **Exceptions**:  
  - `FileExistsError`: If the `.ini` file exists and `init_check` is `True`.  
  - `ValueError`: If `names` and `values` are not lists or their lengths don't match.  
- **Example**:  

```python
ss.init(['key1'], ['value1'])
```

##### `write(names: Union[str, list[str]], values: Union[Any, list[Any]], overwrite: bool = True, auto_init: bool = True, type_check: bool = True, convert_unsupported: bool = False)`  
- **Description**: Writes key-value pairs to SimpSave, with options for overwriting, automatic initialization, and type checking.  
- **Parameters**:  
  - `names`: Key name(s) (string or list of strings).  
  - `values`: Corresponding value(s) (any supported type).  
  - `overwrite`: If set to `False`, raises a `KeyError` if the key already exists.  
  - `auto_init`: Initializes SimpSave if it does not already exist.  
  - `type_check`: Checks for type consistency with existing data.  
  - `convert_unsupported`: If `True`, converts unsupported types to strings.  
- **Returns**: `True` if the write succeeds.  
- **Exceptions**:  
  - `FileNotFoundError`: If SimpSave doesn't exist and `auto_init` is `False`.  
  - `KeyError`: If overwriting is disabled and the key exists.  
  - `TypeError`: If value types are unsupported or inconsistent.  
- **Example**:  

```python
ss.write('my_key', 123)
```

##### `read(names: Union[str, list[str]])`  
- **Description**: Reads the value(s) associated with the specified key(s).  
- **Parameters**:  
  - `names`: The key(s) to read (string or list of strings).  
- **Returns**: The value(s) associated with the key(s).  
- **Exceptions**:  
  - `FileNotFoundError`: If SimpSave doesn't exist.  
  - `KeyError`: If a key doesn't exist.  
- **Example**:  

```python
value = ss.read('my_key')
```  
#### remove(name: str)  
- **Description**: Removes the specified key and its associated value from SimpSave.  
- **Parameters**:  
  - name: The key name to remove (string).  
- **Returns**: True if the key is successfully removed.  
- **Exceptions**:  
  - FileNotFoundError: If the SimpSave `.ini` file does not exist.  
  - KeyError: If the specified key does not exist.  
  - TypeError: If the key name is not a string.  
- **Example**:  
  

```python
ss.remove('my_key')
```


#### clear_ss()  
- **Description**: Deletes the SimpSave `.ini` file from the current directory.  
- **Returns**: True if the file was successfully deleted, False otherwise.  
- **Exceptions**:  
  - FileNotFoundError: If the `.ini` file does not exist.  
- **Example**:  
  

```python
ss.clear_ss()
```  
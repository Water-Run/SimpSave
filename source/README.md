# SimpSave  

## Introduction  

SimpSave utilizes `.ini` files to store Python basic types in key-value pairs.  
***Features:***  
- **Extremely Simple**: The project consists of fewer than 200 lines of code  
- **Extremely Easy to Use**: It’s almost effortless to get started  
- **Flexible and Free**: SimpSave has very few restrictions, allowing you to fully leverage Python's basic data structures  
> This document applies to SimpSave version 2.2  

## Installation  

SimpSave is available on PyPi and can be installed easily via `pip`:  
```bash
pip install simpsave
```
Then, you can use SimpSave in your project:  
```python
import simpsave as ss  # Typically alias as 'ss'
```  

## Principle  

SimpSave stores Python basic type variables in a specified `.ini` file using key-value pairs. The default `.ini` file is `__ss__.ini` located in the current relative path. However, you can change it to another path.  
> SimpSave’s unique `:ss:` path mode: When you describe your path starting with `:ss:` (e.g., `:ss:test.ini`), SimpSave will place `test.ini` in the SimpSave installation path. This ensures compatibility across different devices.  
>> This feature requires installing SimpSave via `pip`  

A typical SimpSave file contains one or more key-value pairs like the following:  
```plaintext
[Sample_Key]
value = '123'
type = str
```
When data is read, it will be automatically converted based on the value’s type.  
This allows SimpSave to efficiently leverage Python's powerful built-in types like `list`, `dict`, etc., making it a great data persistence tool for many simple applications.  

## Usage Guide  

> Version 2.1 update: The `file` parameter must now be explicitly declared in function calls   
> > eg. `read('key1', file='1.ini')`  
 
### Writing  

SimpSave uses the `write` function for writing operations:  
```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

***Parameters:***  
- `key`: The target key for the value to be written. Must be a valid key name for an INI file  
- `value`: The value to be written. Must be a Python basic type  
- `file`: The target file to write to. Defaults to `__ss__.ini`. If you want to change it, you must specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode to refer to the SimpSave installation path.  

***Return Value:***  
`bool` Whether the writing operation was successful  

***Exceptions:***  
`TypeError` If the input value is not a Python basic type  

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')  # Writes the string 'value' to key1
ss.write('key2', 3.14)  # Writes the float 3.14 to key2
ss.write('key2', [0, True, [123]])  # Writes a mixed list to key2, overwriting the previous float value
```
> If the specified `.ini` file path does not exist, SimpSave will attempt to create one.

### Reading  

SimpSave uses the `read` function for reading operations:  
```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

***Parameters:***  
- `key`: The target key to read. Must be a valid key name for an INI file  
- `file`: The file to read from. Defaults to `__ss__.ini`. If you want to change it, specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode.  

***Return Value:***  
`any` The value stored under the specified key, automatically converted to its original type when stored  

***Exceptions:***  
- `FileNotFoundError` If the specified `.ini` file does not exist  
- `KeyError` If the specified key does not exist in the `.ini` file  
- `ValueError` If the value conversion fails  

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')
ss.write('key2', 3.14)

print(ss.read('key1'))  # Outputs 'value'
print(ss.read('key2'))  # Outputs 3.14
```

### Checking Key Existence  

SimpSave uses the `has` function to check if a specified key exists in the `.ini` file:  
```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

***Parameters:***  
- `key`: The target key to check. Must be a valid key name for an INI file  
- `file`: The target file to check in. Defaults to `__ss__.ini`. If you want to change it, specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode.  

***Return Value:***  
`bool` Whether the specified key exists in the file  

***Exceptions:***  
- `FileNotFoundError` If the specified `.ini` file does not exist

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')
ss.write('key2', 3.14)

print(ss.has('key1'))  # Outputs True, because the key 'key1' exists
print(ss.has('key_nonexistent'))  # Outputs False, because the key does not exist
```

### Removing  

SimpSave uses the `remove` function for removing keys:  
```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

***Parameters:***  
- `key`: The target key to be removed. Must be a valid key name for an INI file  
- `file`: The target file to remove from. Defaults to `__ss__.ini`. If you want to change it, specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode.  

***Return Value:***  
`bool` Whether the removal was successful  

***Exceptions:***  
- `FileNotFoundError` If the specified `.ini` file does not exist  

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')
ss.write('key2', 3.14)

print(ss.remove('key1'))  # Outputs True, indicating successful removal
print(ss.remove('key_nonexistent'))  # Outputs False, because the key does not exist
```

### Matching  

SimpSave uses the `match` function for regular expression matching:  
```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

***Parameters:***  
- `re`: The regular expression for matching keys  
- `file`: The file to match from. Defaults to `__ss__.ini`. If you want to change it, specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode.  

***Return Value:***  
`dict[str, any]` A dictionary of matched keys and their corresponding values  

***Exceptions:***  
- `FileNotFoundError` If the specified `.ini` file does not exist  

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')
ss.write('key2', 3.14)

result = ss.match(r'^key.*')
print(result)  # Outputs {'key1': 'value', 'key2': 3.14}
```

> Regular expression matching is useful to understand the contents stored in a specified `.ini` file  
> If re is null, then all results are automatically matched  
### Deleting  

SimpSave uses the `delete` function to delete files:  
```python
def delete(*, file: str | None = None) -> bool:
    ...
```

***Parameters:***  
- `file`: The file to delete. Defaults to `__ss__.ini`. If you want to change it, specify a valid `.ini` file path, either absolute or relative, or use the `:ss:` mode.  

***Return Value:***  
`bool` Whether the deletion was successful  

***Exceptions:***  
- `IOError` If the delete failed  

***Code Example:***  
```python
import simpsave as ss
ss.write('key1', 'value')
ss.write('key2', 3.14)

print(ss.delete())  # Deletes the default `__ss__.ini` file, returns True if successful
```  
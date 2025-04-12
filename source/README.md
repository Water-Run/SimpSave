# SimpSave  

## Introduction  

SimpSave is a lightweight Python library designed for simple and efficient data persistence. It uses `.ini` files to store Python basic types in key-value pairs, making it an ideal solution for small-scale data storage needs.

### Features:
- **Extremely Simple**: The entire project contains fewer than 200 lines of code.
- **Easy to Use**: Minimal setup and straightforward API for quick integration.
- **Flexible and Lightweight**: Supports Python's basic data types and requires no external dependencies.

> Compatible with SimpSave version 3.2.

---

## Installation  

SimpSave is available on PyPI and can be installed with `pip`:  

```bash
pip install simpsave
```

To use SimpSave in your project:  

```python
import simpsave as ss  # Typically aliased as 'ss'
```

---

## Principle  

SimpSave stores Python basic type variables in `.ini` files using key-value pairs. By default, it saves data in a file named `__ss__.ini` located in the current working directory. However, you can specify a custom file path if needed.

### Unique Path Mode  
SimpSave offers a unique `:ss:` path mode. If your file path starts with `:ss:`, for example, `:ss:config.ini`, the file will be stored in the SimpSave installation directory. This ensures compatibility across different environments.  

> Note: The `:ss:` mode requires SimpSave to be installed via `pip`.  

### Example of a SimpSave `.ini` File:
```ini
[Sample_Key]
value = '123'
type = str
```

When you read the data, SimpSave automatically converts it back to its original type. This makes SimpSave a powerful yet simple tool for persisting Python's built-in types, including `list`, `dict`, and more.

---

## Usage Guide  

### Writing Data  

The `write` function stores key-value pairs in a specified `.ini` file:  

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

#### Parameters:
- `key`: The key under which the value will be stored. Must be a valid INI key name.
- `value`: The value to store. Must be a Python basic type (e.g., `int`, `float`, `str`, `list`, `dict`).
- `file`: The path of the `.ini` file to write to. Defaults to `__ss__.ini`. Can also use `:ss:` mode.  

#### Return Value:
- Returns `True` if the write operation is successful, otherwise `False`.

#### Example:
```python
import simpsave as ss
ss.write('key1', 'Hello World')  # Writes a string
ss.write('key2', 3.14)  # Writes a float
ss.write('key3', [1, 2, 3])  # Writes a list
```

> If the file does not exist, SimpSave will create it automatically.

---

### Reading Data  

The `read` function retrieves a value from a specified `.ini` file:  

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### Parameters:
- `key`: The key to read from the file.
- `file`: The path of the `.ini` file to read from. Defaults to `__ss__.ini`.

#### Return Value:
- Returns the value stored under the specified key, automatically converted to its original type.

#### Example:
```python
import simpsave as ss
print(ss.read('key1'))  # Outputs: 'Hello World'
print(ss.read('key2'))  # Outputs: 3.14
```

---

### Additional Features  

#### Checking Key Existence  

The `has` function checks if a key exists in the `.ini` file:  

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Example:
```python
import simpsave as ss
print(ss.has('key1'))  # Outputs: True
print(ss.has('nonexistent_key'))  # Outputs: False
```

---

#### Removing Keys  

The `remove` function deletes a key (and its value) from the `.ini` file:  

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Example:
```python
import simpsave as ss
ss.remove('key1')  # Removes the key 'key1'
```

---

#### Regular Expression Matching  

The `match` function retrieves all key-value pairs that match a given regular expression:  

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### Example:
```python
import simpsave as ss
result = ss.match(r'^key.*')  # Matches all keys starting with 'key'
print(result)  # Outputs: {'key2': 3.14, 'key3': [1, 2, 3]}
```

---

#### Deleting Files  

The `delete` function deletes the entire `.ini` file:  

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### Example:
```python
import simpsave as ss
ss.delete(file='__ss__.ini')  # Deletes the default file
```

---

## Summary  

SimpSave is a simple, flexible, and lightweight library for persisting Python's basic data types using `.ini` files. With its easy-to-use API and support for common data types like `list` and `dict`, SimpSave is perfect for small-scale, low-complexity projects.

> Explore more on [GitHub](https://github.com/Water-Run/SimpSave).  

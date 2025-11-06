# SimpSave Version 10  

## Introduction

SimpSave 4.0 is a lightweight Python library for simple and efficient data persistence, **now upgraded to use `.yml` files** for storage. This shift from `.ini` to `.yml` brings enhanced support for Unicode and complex data structures, removing the need for UTF-8 or escape-based conversions.

### Features

- **Extremely Simple**: The whole project remains under 200 lines of code.
- **Easy to Use**: Minimal setup and a clean, intuitive API for fast integration.
- **Flexible and Lightweight**: Supports all Python basic types, including Unicode, with no external dependencies (except `PyYAML`).
- **YAML Native**: Full native Unicode and structure support—no more escapes or encoding tricks.

> Compatible with SimpSave version 4.0.

---

## Installation

SimpSave 4.0 is available on PyPI and can be installed with:

```bash
pip install simpsave
```

> **Note:** SimpSave 4.0 requires the [`PyYAML`](https://pypi.org/project/PyYAML/) library, which will be installed automatically via pip.

To use SimpSave in your project:

```python
import simpsave as ss  # Typically aliased as 'ss'
```

---

## Principle

SimpSave 4.0 stores Python basic type variables in `.yml` files using key-value pairs. By default, it saves data in a file named `__ss__.yml` located in the current working directory. You can also specify a custom file path if needed.

### Unique Path Mode

Just as before, SimpSave supports a unique `:ss:` path mode. If your file path starts with `:ss:` (e.g., `:ss:config.yml`), the file will be stored in the SimpSave installation directory, ensuring compatibility across environments.

> Note: The `:ss:` mode requires SimpSave to be installed via `pip`.

### Example of a SimpSave `.yml` File

```yaml
key1:
  value: Hello 世界
  type: str
key2:
  value: 3.14
  type: float
key3:
  value: [1, 2, 3, "中文", {"a": 1}]
  type: list
```

When you read the data, SimpSave automatically converts it back to its original type. SimpSave 4.0 fully supports Python's built-in types including `list`, `dict`, and Unicode strings.

---

## Usage Guide

### Writing Data

The `write` function stores key-value pairs in a specified `.yml` file:

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

#### Parameters:

- `key`: The key under which the value will be stored. Must be a valid YAML key.
- `value`: The value to store. Must be a Python basic type (e.g., `int`, `float`, `str`, `list`, `dict`).
- `file`: The path of the `.yml` file to write to. Defaults to `__ss__.yml`. Can also use `:ss:` mode.

#### Return Value:

- Returns `True` if the write operation is successful, otherwise `False`.

#### Example:

```python
import simpsave as ss
ss.write('key1', 'Hello 世界')      # Writes a Unicode string
ss.write('key2', 3.14)             # Writes a float
ss.write('key3', [1, 2, 3, '中文']) # Writes a list with Unicode
```

> If the file does not exist, SimpSave creates it automatically.

---

### Reading Data

The `read` function retrieves a value from a specified `.yml` file:

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### Parameters:

- `key`: The key to read from the file.
- `file`: The path of the `.yml` file to read from. Defaults to `__ss__.yml`.

#### Return Value:

- Returns the value stored under the specified key, automatically converted to its original type.

#### Example:

```python
import simpsave as ss
print(ss.read('key1'))  # Outputs: 'Hello 世界'
print(ss.read('key2'))  # Outputs: 3.14
```

---

### Additional Features

#### Checking Key Existence

The `has` function checks if a key exists in the `.yml` file:

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Example:

```python
import simpsave as ss
print(ss.has('key1'))          # Outputs: True
print(ss.has('nonexistent'))   # Outputs: False
```

---

#### Removing Keys

The `remove` function deletes a key (and its value) from the `.yml` file:

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
print(result)  # Outputs: {'key2': 3.14, 'key3': [1, 2, 3, '中文']}
```

---

#### Deleting Files

The `delete` function deletes the entire `.yml` file:

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### Example:

```python
import simpsave as ss
ss.delete(file='__ss__.yml')  # Deletes the default file
```

---

## Summary

SimpSave 4.0 is a simple, flexible, and lightweight library for persisting Python's basic data types using `.yml` files. With its easy-to-use API, native Unicode support, and compatibility with all common data types, SimpSave is perfect for small-scale, low-complexity projects.

> Explore more on [GitHub](https://github.com/Water-Run/SimpSave).

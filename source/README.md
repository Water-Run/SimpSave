# SimpSave Version 10

## Introduction

**SimpSave** is a lightweight Python key-value storage database for basic variable persistence, utilizing Python’s powerful built-in data structures. It follows a “read-and-use” style, making it extremely easy to use and perfect for small scripts such as student projects or configuration files.  
**SimpSave 10** is a major upgrade that introduces optional storage engines. With an encapsulated `sqlite` engine, it even reaches production usability levels for lightweight scenarios (despite having no connection pool mechanism for its functional API). For minimal environments, optional dependencies preserve the original zero-dependency ultra-lightweight nature.

### Core Features

- **Extremely Lightweight**: Minimal and efficient core code; dependency-free minimal installation  
- **Extremely Easy to Use**: Functional APIs (`read()`, `write()`, etc.) are straightforward with almost no learning curve  
  ```python
  import simpsave as ss
  ss.write('key1', 'value1')
  ss.read('key1')  # 'value1'
  ```
- **Read-and-Use**: Stored and retrieved types remain consistent, with no need for manual type conversion  
  ```python
  import simpsave as ss
  ss.write('key1', 1)
  type(ss.read('key1')).__name__  # 'int'
  ss.read('key1') + 1  # 2
  ```
- **Multi-Engine Support**: From dependency-free lightweight `XML` engines to production-ready `SQLITE` engines. **SimpSave** automatically selects an engine based on file extension—no configuration required.  

## Installation

**SimpSave** is available on [PyPI](https://pypi.org/project/simpsave/). Install it using `pip`:  

```bash
pip install simpsave
```

Then, import it into your project:  

```python
import simpsave as ss  # commonly aliased as 'ss'
```

And you’re ready to use it.  

### Optional Dependencies

**SimpSave** supports optional dependencies so you can install only what you need:  

```bash
pip install simpsave                # Install with all engines
pip install simpsave[XML]           # Minimal: XML engine only (requires xml.etree)
pip install simpsave[INI]           # XML + INI engines (no external dependencies)
pip install simpsave[YML]           # XML + YML engines (requires PyYAML)
pip install simpsave[TOML]          # XML + TOML engines (requires tomli)
pip install simpsave[JSON]          # XML + JSON engines (no external dependencies)
pip install simpsave[SQLITE]        # XML + SQLITE engines (requires sqlite3)
```

> The `SQLITE` engine requires an existing SQLite environment installed locally.  

## Quick Start Example

Below is a simple example to get started with **SimpSave**:  

```python
import simpsave as ss

# Write data
ss.write('name', 'Alice')
ss.write('age', 25)
ss.write('scores', [90, 85, 92])

# Read data
print(ss.read('name'))     # Alice
print(ss.read('age'))      # 25
print(ss.read('scores'))   # [90, 85, 92]

# Check key existence
print(ss.has('name'))      # True
print(ss.has('email'))     # False

# Delete a key
ss.remove('age')
print(ss.has('age'))       # False

# Regex match
ss.write('user_admin', True)
ss.write('user_guest', False)
print(ss.match(r'^user_'))  # {'user_admin': True, 'user_guest': False}

# Use a different file (engine auto-selected)
ss.write('theme', 'dark', file='config.yml')
print(ss.read('theme', file='config.yml'))  # dark

# Use :ss: mode (stored in installation directory)
ss.write('key1', 'value1', file=':ss:config.toml')
print(ss.read('key1', file=':ss:config.toml'))  # value1

# Delete storage files
ss.delete()
ss.delete(file='config.yml')
```

If you have basic programming knowledge, you’ll master **SimpSave** almost instantly.  

## Engines

**SimpSave 10** supports multiple storage engines, selectable per use case. Each engine is defined in the `ss.ENGINE` enumeration:  

| Engine | File Format | Dependency | Description |
|---------|--------------|-------------|-------------|
| `XML` | `.xml` | `xml.etree` (built-in) | Stores data in XML format; lightweight, dependency-free |
| `INI` | `.ini` | `configparser` (built-in) | Stores data in INI format; limited Unicode support |
| `YML` | `.yml` | `PyYAML` | YAML format storage |
| `TOML` | `.toml` | `tomli` | TOML format storage |
| `JSON` | `.json` | `json` (built-in) | JSON format storage |
| `SQLITE` | `.db` | `sqlite3` (built-in) | SQLite database; production-level performance |

### Automatic Engine Selection

**SimpSave** automatically chooses an engine based on the file extension provided to `file`:  

```python
import simpsave as ss

ss.write('key1', 'value1', file='data.yml')     # Uses YML engine
ss.write('key2', 'value2', file='config.toml')  # Uses TOML engine
ss.write('key3', 'value3', file='data.db')      # Uses SQLITE engine
```

## Mechanism

**SimpSave** stores Python’s built-in basic data types as key-value pairs. The actual data format varies based on the selected engine.  

> By default, data is saved to `__ss__.xml` in the current working directory.  

### `:ss:` Mode  

As in earlier versions, **SimpSave** supports the unique `:ss:` path prefix—files with `:ss:` (e.g., `:ss:config.json`) are stored in the **SimpSave** installation directory, ensuring cross-environment compatibility.  

```python
import simpsave as ss

ss.write('key1', 'value1', file=':ss:config.yml')
print(ss.read('key1', file=':ss:config.yml'))
```

> `:ss:` mode is available only when SimpSave is installed via `pip`.  

### Supported Data Types

**SimpSave** fully supports Python’s basic built-in types, including:  

- `int`
- `float`
- `str`
- `bool`
- `list` (including nested lists of basic types)
- `dict`
- `tuple`
- `None`

When read back, data automatically restores to its original Python type—providing genuine “read-and-use” capability.  

## API Reference

### Write Data

`write` writes a key-value pair into the specified file:  

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

If the file doesn’t exist, it will be created automatically.  

#### Parameters

- `key`: The key to save (string only)
- `value`: The value to store (any supported Python base type)
- `file`: Target file path; defaults to `__ss__.xml`. Supports `:ss:` mode. Engine is auto-selected by extension.  

#### Return Value

- Returns `True` on success, `False` on failure.  

#### Exceptions

- `ValueError`: Value is not a supported Python base type  
- `IOError`: Write operation failed  
- `RuntimeError`: Other runtime errors (e.g., engine not installed)  

#### Example

```python
import simpsave as ss

ss.write('key1', 'Hello World')
ss.write('key2', 3.14)
ss.write('key3', [1, 2, 3, 'Text'])
ss.write('key4', {'a': 1, 'b': 2})

# Different engines
ss.write('config', 'value', file='settings.yml')  # YML engine
ss.write('data', 100, file='cache.db')            # SQLITE engine
```

> Files are created automatically if missing.  

### Read Data

`read` reads data from a specified file:  

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### Parameters

- `key`: Key name to read  
- `file`: File path to read from (defaults to `__ss__.xml`)  

#### Return Value

- Returns the value associated with the key (restored to its original type).  
- Returns `None` if the key does not exist.  

#### Exceptions

- `IOError`: Read error  
- `RuntimeError`: Engine error or missing dependency  

#### Example

```python
import simpsave as ss

print(ss.read('key1'))
print(ss.read('key2'))
print(ss.read('key3'))

value = ss.read('config', file='settings.yml')
```

### Check for Key Existence

`has` checks if a given key exists in the file:  

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `key`: Key name to check  
- `file`: File path (defaults to `__ss__.xml`)  

#### Return Value

- Returns `True` if the key exists, otherwise `False`.  

#### Exceptions

- `IOError`: Read error  
- `RuntimeError`: Engine error  

#### Example

```python
import simpsave as ss

print(ss.has('key1'))
print(ss.has('nonexistent'))
```

### Remove a Key

`remove` deletes a key and its associated value:  

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `key`: Key to delete  
- `file`: Target file (defaults to `__ss__.xml`)  

#### Return Value

- Returns `True` on success, `False` on failure.  

#### Exceptions

- `IOError`: Write error  
- `RuntimeError`: Engine error  

#### Example

```python
import simpsave as ss

ss.remove('key1')
print(ss.has('key1'))  # False
```

### Regex Match Keys

`match` returns key-value pairs that match a regular expression:  

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### Parameters

- `re`: Regular expression string (empty = all keys)  
- `file`: File path (defaults to `__ss__.xml`)  

#### Return Value

- Returns a dictionary of all matched key-value pairs.  

#### Exceptions

- `IOError`: Read error  
- `RuntimeError`: Engine error  

#### Example

```python
import simpsave as ss

ss.write('user_name', 'Alice')
ss.write('user_age', 25)
ss.write('admin_name', 'Bob')

result = ss.match(r'^user_.*')
print(result)
```

### Delete File

`delete` removes the entire storage file:  

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `file`: File path to delete (defaults to `__ss__.xml`)  

#### Return Value

- Returns `True` on success, `False` on failure.  

#### Exceptions

- `IOError`: Delete error  
- `RuntimeError`: Engine error  

#### Example

```python
import simpsave as ss

ss.delete()
ss.delete(file='config.yml')
```

## Exception Handling

**SimpSave** may raise the following exceptions. Understanding them helps you write more robust code.  

### Common Exception Types

#### `ValueError`

Raised when attempting to store non-basic Python types.  

**Examples:**  

```python
import simpsave as ss

class CustomClass:
    pass

try:
    ss.write('key1', CustomClass())
except ValueError as e:
    print(f"Error: {e}")
```

#### `IOError`

Raised when file read/write operations fail.  

**Examples:**  

```python
import simpsave as ss

try:
    ss.read('key1', file='/root/protected.db')
except IOError as e:
    print(f"File I/O error: {e}")
```

#### `RuntimeError`

Raised for engine or runtime-related issues.  

**Examples:**  

```python
import simpsave as ss

try:
    ss.write('key1', 'value1', file='data.unknown')
except RuntimeError as e:
    print(f"Runtime error: {e}")
```

### Best Practices for Exception Handling

Use `try-except` to safely handle operations:  

```python
import simpsave as ss

# Safe write
try:
    ss.write('key1', 'value1')
except ValueError as e:
    print(f"Invalid value type: {e}")
except IOError as e:
    print(f"Write failed: {e}")
except RuntimeError as e:
    print(f"Runtime error: {e}")

# Safe read
try:
    value = ss.read('key1')
    if value is None:
        print("Key does not exist")
except IOError as e:
    print(f"Read failed: {e}")
except RuntimeError as e:
    print(f"Runtime error: {e}")
```

## Practical Tips  

1. For non-`SQLITE` engines, keep data size and complexity under control.  
2. Always use `has()` or `try-except` checks before reading:  
    ```python
    import simpsave as ss
    value = 'default'
    if ss.has('key_1'):
        value = ss.read('key_1')
    else:
        ss.write('key_1', 'default')
    ```
    - When file existence is uncertain, use initialization inside `try-except`.  

> For more information, visit [GitHub](https://github.com/Water-Run/SimpSave)
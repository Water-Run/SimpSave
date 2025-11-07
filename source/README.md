# SimpSave Version 10

## Introduction

**SimpSave** is a lightweight Python key-value database for persisting basic Python variables. It leverages Python's powerful native data structure support, making it extremely easy to use and ideal for small scripts such as student assignments.

**SimpSave 10** is a major upgrade that introduces optional storage engines: engine wrappers for `sqlite` and `Redis` provide production-level capabilities for lightweight environments, while maintaining the original zero-dependency minimalist design for simple use cases.

### Core Features

- **Extremely Lightweight**: Core code is concise and efficient, with minimal installation requiring no dependencies
- **Extremely Easy to Learn**: Functional API (`read()`, `write()`, etc.) is very intuitive with virtually no learning curve, ready to use immediately
  ```python
  import simpsave as ss
  ss.write('key1', 'value1')
  ss.read('key1')  # 'value1'
  ```
- **Read-and-Use**: Stored types match retrieved types, no need for type checking or conversion, further simplifying usage
  ```python
  import simpsave as ss
  ss.write('key1', 1)
  type(ss.read('key1')).__name__  # 'int'
  ss.read('key1') + 1  # 2
  ```
- **Multi-Engine Support**: From the ultra-minimal dependency-free `SIMP` engine to production-grade `SQLITE` and `REDIS` engines. Automatically selects engine based on file extension, no manual configuration needed

## Installation

**SimpSave** is published on [PyPI](https://pypi.org/project/simpsave/) and can be installed with `pip`:

```bash
pip install simpsave
```

Then import it in your project:

```python
import simpsave as ss  # Commonly aliased as 'ss'
```

You're ready to start using it.

### Optional Dependencies

**SimpSave** supports optional dependencies based on your needs:

```bash
pip install simpsave                # Install all dependencies
pip install simpsave[SIMP]          # Minimal: SIMP engine only (no dependencies)
pip install simpsave[INI]           # SIMP and INI engines (no dependencies)
pip install simpsave[XML]           # SIMP and XML engines (requires xml.etree)
pip install simpsave[YML]           # SIMP and YML engines (requires PyYAML)
pip install simpsave[TOML]          # SIMP and TOML engines (requires tomli)
pip install simpsave[JSON]          # SIMP and JSON engines (no dependencies)
pip install simpsave[SQLITE]        # SIMP and SQLITE engines (requires sqlite3)
pip install simpsave[REDIS]         # SIMP and REDIS engines (requires redis-py)
```

> The `SQLITE` engine requires SQLite to be deployed locally; the `REDIS` engine requires a Redis service to be running

## Quick Start Example

The following code provides a quick start example for **SimpSave**:

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

# Check keys
print(ss.has('name'))      # True
print(ss.has('email'))     # False

# Remove keys
ss.remove('age')
print(ss.has('age'))       # False

# Regular expression matching
ss.write('user_admin', True)
ss.write('user_guest', False)
print(ss.match(r'^user_'))  # {'user_admin': True, 'user_guest': False}

# Use different files (automatically selects corresponding engine)
ss.write('theme', 'dark', file='config.yml')
print(ss.read('theme', file='config.yml'))  # dark

# Use :ss: mode (saves to installation directory)
ss.write('key1', 'value1', file=':ss:config.yml')
print(ss.read('key1', file=':ss:config.yml'))  # value1

# Delete files
ss.delete()
ss.delete(file='config.yml')
```

If you have some programming background, **SimpSave's** intuitive design should have you up and running in no time.

## Engines

**SimpSave 10** supports multiple storage engines that can be selected based on your needs. Engines are stored in the `ss.ENGINE` enum:

| Engine Name | File Format | Write Performance Benchmark | Read Performance Benchmark | Dependencies | Description |
|-------------|-------------|----------------------------|---------------------------|--------------|-------------|
| `SIMP` | `.simpsave` | Fast | Fast | None | Simplest engine, uses custom plain text files with no external dependencies |
| `INI` | `.ini` | Fast | Fast | `configparser` (built-in) | Uses INI format storage, not fully `Unicode` compatible |
| `XML` | `.xml` | Medium | Medium | `xml.etree` (built-in) | Uses XML format storage |
| `YML` | `.yml` | Medium | Medium | `PyYAML` | Uses YAML format storage |
| `TOML` | `.toml` | Fast | Fast | `tomli` | Uses TOML format storage |
| `JSON` | `.json` | Fast | Fast | `json` (built-in) | Uses JSON format storage |
| `SQLITE` | `.db` | Very Fast | Very Fast | `sqlite3` (built-in) | Uses SQLite database with production-grade performance |
| `REDIS` | Memory | Extremely Fast | Extremely Fast | `redis-py` | Uses Redis in-memory database with production-grade performance |

> Test benchmark: `Fedora 43`, `i7-13620H`, `16GB DDR5`, `SN740 1TB`

### Automatic Engine Selection

**SimpSave** automatically selects the appropriate engine based on the file extension in the `file` parameter:

```python
import simpsave as ss

ss.write('key1', 'value1', file='data.yml')     # Automatically uses YML engine
ss.write('key2', 'value2', file='config.toml')  # Automatically uses TOML engine
ss.write('key3', 'value3', file='data.db')      # Automatically uses SQLITE engine
```

If no file is specified or the extension is unrecognized, the default `SIMP` engine is used with filename `__ss__.simpsave`

## How It Works

**SimpSave** stores Python basic type data in key-value format. Depending on the selected engine, data is stored in different formats.

> By default, data is saved to the `__ss__.simpsave` file in the current working directory

### `:ss:` Mode

Like previous versions, **SimpSave** retains support for the unique `:ss:` path mode: if the file path starts with `:ss:` (e.g., `:ss:config.yml`), the file will be saved in the **SimpSave** installation directory, ensuring cross-environment compatibility.

```python
import simpsave as ss

ss.write('key1', 'value1', file=':ss:config.yml')  # Save to SimpSave installation directory
print(ss.read('key1', file=':ss:config.yml'))      # Read from installation directory
```

> `:ss:` mode requires SimpSave to be installed via `pip`

### Data Types

**SimpSave** fully supports Python's built-in basic types, including:

- `int`
- `float`
- `str`
- `bool`
- `list`
- `dict`
- `tuple`
- `None`

When reading data, **SimpSave** automatically restores it to its original `Python` type, achieving "read-and-use" functionality.

## API Reference

### Writing Data

The `write` function writes key-value pairs to a specified file:

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `key`: The key to store, must be a valid string
- `value`: The value to store, supports Python basic types
- `file`: The file path to write to, defaults to `__ss__.simpsave`, can use `:ss:` mode. Engine is automatically selected based on file extension

#### Return Value

- Returns `True` on success, `False` on failure

#### Example

```python
import simpsave as ss

ss.write('key1', 'Hello 世界')           # Write Unicode string
ss.write('key2', 3.14)                  # Write float
ss.write('key3', [1, 2, 3, '中文'])      # Write list with Chinese characters
ss.write('key4', {'a': 1, 'b': 2})      # Write dictionary

# Use different engines
ss.write('config', 'value', file='settings.yml')   # Use YML engine
ss.write('data', 100, file='cache.db')             # Use SQLITE engine
```

> If the file doesn't exist, SimpSave creates it automatically

---

### Reading Data

The `read` function reads data from a specified file:

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### Parameters

- `key`: The key name to read
- `file`: The file path to read from, defaults to `__ss__.simpsave`

#### Return Value

* Returns the value corresponding to the specified key, automatically restored to its original type
* Returns `None` if the key doesn't exist

#### Example

```python
import simpsave as ss

print(ss.read('key1'))  # Output: 'Hello 世界'
print(ss.read('key2'))  # Output: 3.14
print(ss.read('key3'))  # Output: [1, 2, 3, '中文']

# Read from different files
value = ss.read('config', file='settings.yml')
```

---

### Checking Key Existence

The `has` function checks if a key exists in a file:

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `key`: The key name to check
- `file`: The file path to check, defaults to `__ss__.simpsave`

#### Return Value

* Returns `True` if key exists, `False` otherwise

#### Example

```python
import simpsave as ss

print(ss.has('key1'))        # Output: True
print(ss.has('nonexistent')) # Output: False
```

---

### Removing Keys

The `remove` function deletes a key and its corresponding value from a file:

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `key`: The key name to remove
- `file`: The file path to operate on, defaults to `__ss__.simpsave`

#### Return Value

* Returns `True` on successful deletion, `False` on failure

#### Example

```python
import simpsave as ss

ss.remove('key1')  # Remove key 'key1'
print(ss.has('key1'))  # Output: False
```

---

### Regular Expression Key Matching

The `match` function matches all keys using a regular expression and returns corresponding key-value pairs:

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### Parameters

- `re`: Regular expression string for matching key names. Empty string matches all keys
- `file`: The file path to operate on, defaults to `__ss__.simpsave`

#### Return Value

- Returns a dictionary containing all matched key-value pairs

#### Example

```python
import simpsave as ss

ss.write('user_name', 'Alice')
ss.write('user_age', 25)
ss.write('admin_name', 'Bob')

result = ss.match(r'^user_.*')  # Match all keys starting with 'user_'
print(result)  # Output: {'user_name': 'Alice', 'user_age': 25}

all_data = ss.match()  # Get all key-value pairs
print(all_data)
```

---

### Deleting Files

The `delete` function deletes an entire storage file:

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### Parameters

- `file`: The file path to delete, defaults to `__ss__.simpsave`

#### Return Value

- Returns `True` on successful deletion, `False` on failure

#### Example

```python
import simpsave as ss

ss.delete()  # Delete the default save file
ss.delete(file='config.yml')  # Delete specified file
```

---

## Note: Using the REDIS Engine

The `REDIS` engine stores data in memory, which is lost on power loss. Ensure Redis service is running before use

```python
import simpsave as ss

# Use REDIS engine (file parameter is used as Redis key prefix)
ss.write('key1', 'value1', file='redis://localhost:6379/0')
print(ss.read('key1', file='redis://localhost:6379/0'))
```

The `REDIS` engine requires the `redis-py` dependency: `pip install simpsave[REDIS]`

> Learn more at [GitHub](https://github.com/Water-Run/SimpSave)  

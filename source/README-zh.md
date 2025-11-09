# SimpSave 版本 10

## 简介

**SimpSave**是一个Python羽量级键值对Python基本变量存储数据库, 利用了`Python`原生强大的数据结构支持, "即读即用", 极其简易上手, 很适合用于各种小型脚本如学生作业中, 或作为配置文件等使用.  
**SimpSave 10**是一次重大升级, 带来了可选引擎的能力: 对`sqlite`的引擎封装提供,使其在某些轻量级生产环境也具备了可用水平(尽管函数式的API无连接池机制); 而对于简易环境中的使用, 可选依赖也可保持原先的0依赖极简特性.

### 核心特点

- **极其轻量**: 核心代码简洁高效, 最小化安装无任何依赖  
- **极其容易上手**: 函数式 API(`read()`、`write()` 等)非常直观, 几乎没有任何学习成本,可以直接上手  
  ```python
  import simpsave as ss
  ss.write('key1', 'value1')
  ss.read('key1')  # 'value1'
  ```
- **即读即用**: 存储的类型和读出类型保持一致, 无需进行类型判断和转换, 进一步简化使用  
  ```python
  import simpsave as ss
  ss.write('key1', 1)
  type(ss.read('key1')).__name__  # 'int'
  ss.read('key1') + 1  # 2
  ```
- **多引擎支持**: 从无任何依赖的轻量级 `XML` 引擎, 到具备生产性能的 `SQLITE` 引擎. **SimpSave**根据文件后缀自动选择引擎, 无需手动配置  

## 安装

**SimpSave** 已发布在 [PyPI](https://pypi.org/project/simpsave/) 上, 使用 `pip` 进行安装:  

```bash
pip install simpsave
```

然后, 在你的项目中导入它:  

```python
import simpsave as ss  # 通常别名为 'ss'
```

即可开始使用.  

### 可选依赖

**SimpSave** 支持可选依赖, 可根据实际需求选择安装:  

```bash
pip install simpsave                # 安装全部依赖
pip install simpsave[XML]           # 最小化: 仅包含 XML 引擎（需要 xml.etree）
pip install simpsave[INI]           # 包含 XML 和 INI 引擎（无额外依赖）
pip install simpsave[YML]           # 包含 XML 和 YML 引擎（需要 PyYAML）
pip install simpsave[TOML]          # 包含 XML 和 TOML 引擎（需要 tomli）
pip install simpsave[JSON]          # 包含 XML 和 JSON 引擎（无额外依赖）
pip install simpsave[SQLITE]        # 包含 XML 和 SQLITE 引擎（需要 sqlite3）
```

> `SQLITE` 引擎需要在本机上提前部署 `SQLite` 环境  

## 快速上手示例

以下代码提供了 **SimpSave** 快速上手示例:  

```python
import simpsave as ss

# 写入数据
ss.write('name', 'Alice')
ss.write('age', 25)
ss.write('scores', [90, 85, 92])

# 读取数据
print(ss.read('name'))     # Alice
print(ss.read('age'))      # 25
print(ss.read('scores'))   # [90, 85, 92]

# 检查键
print(ss.has('name'))      # True
print(ss.has('email'))     # False

# 删除键
ss.remove('age')
print(ss.has('age'))       # False

# 正则匹配
ss.write('user_admin', True)
ss.write('user_guest', False)
print(ss.match(r'^user_'))  # {'user_admin': True, 'user_guest': False}

# 使用不同文件（自动选择对应引擎）
ss.write('theme', 'dark', file='config.yml')
print(ss.read('theme', file='config.yml'))  # dark

# 使用 :ss: 模式（保存到安装目录）
ss.write('键1', '值1', file=':ss:config.toml') # 使用中文键名和TOML引擎
print(ss.read('键1', file=':ss:config.toml'))  # 值1

# 删除文件
ss.delete()
ss.delete(file='config.yml')
```

如果你有一定编程基础, 相信 **SimpSave** 的极其直观已经让你学会它的基本使用了.  

## 引擎

**SimpSave 10** 支持多种存储引擎, 可根据实际需求选择.引擎存储在 `ss.ENGINE` 枚举中:  

| 引擎名称 | 文件格式 | 依赖 | 说明 |
|---------|---------|------|------|
| `XML` | `.xml` | `xml.etree`（内置） | 使用 XML 格式存储, 轻量级且无需额外依赖 |
| `INI` | `.ini` | `configparser`（内置） | 使用 INI 格式存储, 不完全兼容 `Unicode` |
| `YML` | `.yml` | `PyYAML` | 使用 YAML 格式存储 |
| `TOML` | `.toml` | `tomli` | 使用 TOML 格式存储 |
| `JSON` | `.json` | `json`（内置） | 使用 JSON 格式存储 |
| `SQLITE` | `.db` | `sqlite3`（内置） | 使用 SQLite 数据库, 具备生产级性能 |

### 自动引擎选择

**SimpSave** 会根据 `file` 参数的文件后缀自动选择合适的引擎:  

```python
import simpsave as ss

ss.write('key1', 'value1', file='data.yml')     # 自动使用 YML 引擎
ss.write('key2', 'value2', file='config.toml')  # 自动使用 TOML 引擎
ss.write('key3', 'value3', file='data.db')      # 自动使用 SQLITE 引擎
```

## 原理

**SimpSave** 使用键值对（key-value）的形式保存 Python 的基础类型数据. 根据选择的引擎不同, 数据会以不同的格式存储.  

> 默认情况下, 数据保存到当前工作目录下的 `__ss__.xml` 文件中  

### `:ss:` 模式  

与旧版相同, **SimpSave** 保留支持独特的 `:ss:` 路径模式: 如果文件路径以 `:ss:` 开头(如 `:ss:config.json`), 文件会被保存在 **SimpSave** 的安装目录中, 从而保证跨环境兼容性.  

```python
import simpsave as ss

ss.write('key1', 'value1', file=':ss:config.yml')  # 保存到 SimpSave 安装目录
print(ss.read('key1', file=':ss:config.yml'))      # 从安装目录读取
```

> `:ss:` 模式要求通过 `pip` 安装 SimpSave  

### 数据类型

**SimpSave** 完整支持 Python 内置的基础类型, 包括:  

- `int`
- `float`
- `str`
- `bool`
- `list`(包括嵌套, 嵌套内的项也需要是`Python`的基础类型数据, 下同)
- `dict`
- `tuple`
- `None`

读取数据时, **SimpSave** 会自动将其恢复为原始的 `Python` 类型, 实现"即读即用".  

## API 参考

### 写入数据

`write` 函数用于向指定文件中写入键值对:  

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

如果指定的存储文件不存在, 会自动进行创建.  

#### 参数说明

- `key`: 要存储的键, 必须是合法的字符串
- `value`: 要存储的值, 支持 Python 基础类型
- `file`: 要写入的文件路径, 默认为 `__ss__.xml`, 可使用 `:ss:` 模式. 引擎会根据文件后缀自动选择  

#### 返回值

- 成功写入返回 `True`, 失败返回 `False`.

#### 异常  

- `ValueError`: 值非Python基本类型的值  
- `IOError`: 写入错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

ss.write('key1', 'Hello 世界')           # 写入 Unicode 字符串
ss.write('key2', 3.14)                  # 写入浮点数
ss.write('key3', [1, 2, 3, '中文'])      # 写入包含中文的列表
ss.write('key4', {'a': 1, 'b': 2})      # 写入字典

# 使用不同引擎
ss.write('config', 'value', file='settings.yml')   # 使用 YML 引擎
ss.write('data', 100, file='cache.db')             # 使用 SQLITE 引擎
```

> 如果文件不存在, SimpSave 会自动创建.

### 读取数据

`read` 函数用于从指定文件中读取数据:  

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### 参数说明

- `key`: 要读取的键名.
- `file`: 要读取的文件路径, 默认为 `__ss__.xml`.

#### 返回值

- 返回指定键对应的值, 并自动恢复为原始类型.
- 如果键不存在, 返回 `None`.

#### 异常  

- `IOError`: 读取错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

print(ss.read('key1'))  # 输出: 'Hello 世界'
print(ss.read('key2'))  # 输出: 3.14
print(ss.read('key3'))  # 输出: [1, 2, 3, '中文']

# 从不同文件读取
value = ss.read('config', file='settings.yml')
```

### 检查键是否存在

`has` 函数用于检测某个键是否存在于文件中:  

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `key`: 要检查的键名.
- `file`: 要检查的文件路径, 默认为 `__ss__.xml`.

#### 返回值

- 键存在返回 `True`, 不存在返回 `False`.

#### 异常  

- `IOError`: 读取错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

print(ss.has('key1'))        # 输出: True
print(ss.has('nonexistent')) # 输出: False
```

### 删除键

`remove` 函数用于删除文件中的某个键及其对应值:  

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `key`: 要删除的键名.
- `file`: 要操作的文件路径, 默认为 `__ss__.xml`.

#### 返回值

- 成功删除返回 `True`, 失败返回 `False`.

#### 异常  

- `IOError`: 写入错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

ss.remove('key1')  # 删除键 'key1'
print(ss.has('key1'))  # 输出: False
```

### 正则匹配键

`match` 函数可通过正则表达式匹配所有符合条件的键, 并返回对应的键值对:  

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### 参数说明

- `re`: 正则表达式字符串, 用于匹配键名.空字符串表示匹配所有键.
- `file`: 要操作的文件路径, 默认为 `__ss__.xml`.

#### 返回值

- 返回一个字典, 包含所有匹配的键值对.

#### 异常  

- `IOError`: 读取错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

ss.write('user_name', 'Alice')
ss.write('user_age', 25)
ss.write('admin_name', 'Bob')

result = ss.match(r'^user_.*')  # 匹配所有以 'user_' 开头的键
print(result)  # 输出: {'user_name': 'Alice', 'user_age': 25}

all_data = ss.match()  # 获取所有键值对
print(all_data)
```

### 删除文件

`delete` 函数可删除整个存储文件:  

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `file`: 要删除的文件路径, 默认为 `__ss__.xml`.

#### 返回值

- 成功删除返回 `True`, 失败返回 `False`.

#### 异常  

- `IOError`: 删除错误  
- `RuntimeError`: 其它运行时错误, 如所选引擎未安装等  

#### 示例

```python
import simpsave as ss

ss.delete()  # 删除默认的保存文件
ss.delete(file='config.yml')  # 删除指定文件
```

## 异常处理

**SimpSave** 在运行过程中可能会抛出以下异常, 了解这些异常有助于编写更健壮的代码.  

### 常见异常类型

#### `ValueError`

当传入的值不是 Python 基本类型时抛出.  

**触发场景:**  

- 尝试存储不支持的复杂对象(如自定义类实例、函数等)
- 传入的值超出引擎支持的类型范围

**示例:**  

```python
import simpsave as ss

class CustomClass:
    pass

try:
    ss.write('key1', CustomClass())  # 抛出 ValueError
except ValueError as e:
    print(f"错误: {e}")
```

#### `IOError`

文件读写操作失败时抛出.  

**触发场景:**  

- 文件权限不足
- 磁盘空间不足
- 文件被其他进程占用
- 文件路径不存在或无效

**示例:**  

```python
import simpsave as ss

try:
    ss.read('key1', file='/root/protected.db')  # 可能抛出 IOError
except IOError as e:
    print(f"文件操作错误: {e}")
```

#### `RuntimeError`

其他运行时错误, 通常是引擎内部错误或配置问题.  

**触发场景:**  

- 引擎初始化失败
- 数据格式损坏
- 依赖库缺失或版本不兼容

**示例:**  

```python
import simpsave as ss

try:
    ss.write('key1', 'value1', file='data.unknown')  # 可能抛出 RuntimeError
except RuntimeError as e:
    print(f"运行时错误: {e}")
```

### 异常处理最佳实践

推荐使用 `try-except` 语句处理可能的异常:  

```python
import simpsave as ss

# 安全写入
try:
    ss.write('key1', 'value1')
except ValueError as e:
    print(f"值类型错误: {e}")
except IOError as e:
    print(f"文件写入失败: {e}")
except RuntimeError as e:
    print(f"运行时错误: {e}")

# 安全读取
try:
    value = ss.read('key1')
    if value is None:
        print("键不存在")
except IOError as e:
    print(f"文件读取失败: {e}")
except RuntimeError as e:
    print(f"运行时错误: {e}")
```

## 实践建议  

1. 使用非`SQLITE`引擎时, 控制数据量和复杂度;  
2. 在读取数据之前, 使用`has`或`try-except`语句安全读取:
    ```python
    import simpsave as ss
    value = 'default value'
    if ss.has('key_1'):
        value = ss.read('key_1')
    else:
        ss.write('key_1', 'default value')
    ```
    - 无法确认对应文件是否存在时,使用`try-except`结合初始化语句.  

> 了解更多, 访问 [GitHub](https://github.com/Water-Run/SimpSave)

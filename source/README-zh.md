# SimpSave 版本 10

## 简介

**SimpSave**是一个Python羽量级键值对Python基本变量存储数据库, 利用了`Python`原生强大的数据结构支持, 极其简易上手, 很适合用于各种小型脚本如学生作业中.  
**SimpSave 10**是一次重大升级, 带来了可选引擎的能力: 对`sqlite`和`Redis`的引擎封装提供,使其在某些轻量级生产环境也具备了可用水平; 而对于简易环境中的使用, 可选依赖也可保持原先的0依赖极简特性.

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
- **多引擎支持**: 从无任何依赖的极简 `SIMP` 引擎, 到具备生产性能的 `SQLITE` 和 `REDIS` 引擎. 根据文件后缀自动选择引擎, 无需手动配置  

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
pip install simpsave[SIMP]          # 最小化: 仅包含 SIMP 引擎（无依赖）
pip install simpsave[INI]           # 包含 SIMP 和 INI 引擎（无依赖）
pip install simpsave[XML]           # 包含 SIMP 和 XML 引擎（需要 xml.etree）
pip install simpsave[YML]           # 包含 SIMP 和 YML 引擎（需要 PyYAML）
pip install simpsave[TOML]          # 包含 SIMP 和 TOML 引擎（需要 tomli）
pip install simpsave[JSON]          # 包含 SIMP 和 JSON 引擎（无依赖）
pip install simpsave[SQLITE]        # 包含 SIMP 和 SQLITE 引擎（需要 sqlite3）
pip install simpsave[REDIS]         # 包含 SIMP 和 REDIS 引擎（需要 redis-py）
```

> `SQLITE` 引擎需要在本机上提前部署 `SQLite` 环境；`REDIS` 引擎需要在本机上提前部署 `Redis` 服务  

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
ss.write('key1', 'value1', file=':ss:config.yml')
print(ss.read('key1', file=':ss:config.yml'))  # value1

# 删除文件
ss.delete()
ss.delete(file='config.yml')
```

如果你有一定编程基础, 相信 **SimpSave** 的极其直观已经让你学会它的基本使用了.  

## 引擎

**SimpSave 10** 支持多种存储引擎, 可根据实际需求选择.引擎存储在 `ss.ENGINE` 枚举中: 

| 引擎名称 | 文件格式 | 写入性能基准 | 读取性能基准 | 依赖 | 说明 |
|---------|---------|---------|---------|------|------|
| `SIMP` | `.simpsave` | 快 | 快 | 无 | 最简易的引擎, 使用自定义的纯文本文件, 无任何外部依赖 |
| `INI` | `.ini` | 快 | 快 | `configparser`（内置） | 使用 INI 格式存储, 不完全兼容 `Unicode` |
| `XML` | `.xml` | 中 | 中 | `xml.etree`（内置） | 使用 XML 格式存储 |
| `YML` | `.yml` | 中 | 中 | `PyYAML` | 使用 YAML 格式存储 |
| `TOML` | `.toml` | 快 | 快 | `tomli` | 使用 TOML 格式存储 |
| `JSON` | `.json` | 快 | 快 | `json`（内置） | 使用 JSON 格式存储 |
| `SQLITE` | `.db` | 非常快 | 非常快 | `sqlite3`（内置） | 使用 SQLite 数据库, 具备生产级性能 |
| `REDIS` | 内存 | 极快 | 极快 | `redis-py` | 使用 Redis 内存数据库, 具备生产级性能 |

> 测试基准: `Fedora 43`, `i7-13620H`, `16GB DDR5`, `SN740 1TB`  

### 自动引擎选择

**SimpSave** 会根据 `file` 参数的文件后缀自动选择合适的引擎:  

```python
import simpsave as ss

ss.write('key1', 'value1', file='data.yml')     # 自动使用 YML 引擎
ss.write('key2', 'value2', file='config.toml')  # 自动使用 TOML 引擎
ss.write('key3', 'value3', file='data.db')      # 自动使用 SQLITE 引擎
```

如果未指定文件或后缀无法识别, 默认使用 `SIMP` 引擎, 文件名为 `__ss__.simpsave`  

## 原理

**SimpSave** 使用键值对（key-value）的形式保存 Python 的基础类型数据. 根据选择的引擎不同, 数据会以不同的格式存储.  

> 默认情况下, 数据保存到当前工作目录下的 `__ss__.simpsave` 文件中  

### `:ss:` 模式  

与旧版相同, **SimpSave** 保留支持独特的 `:ss:` 路径模式: 如果文件路径以 `:ss:` 开头(如 `:ss:config.yml`), 文件会被保存在 **SimpSave** 的安装目录中, 从而保证跨环境兼容性.  

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
- `list`
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

#### 参数说明

- `key`: 要存储的键, 必须是合法的字符串
- `value`: 要存储的值, 支持 Python 基础类型
- `file`: 要写入的文件路径, 默认为 `__ss__.simpsave`, 可使用 `:ss:` 模式. 引擎会根据文件后缀自动选择  

#### 返回值

- 成功写入返回 `True`, 失败返回 `False`.

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

---

### 读取数据

`read` 函数用于从指定文件中读取数据:  

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### 参数说明

- `key`: 要读取的键名.
- `file`: 要读取的文件路径, 默认为 `__ss__.simpsave`.

#### 返回值

* 返回指定键对应的值, 并自动恢复为原始类型.
* 如果键不存在, 返回 `None`.

#### 示例

```python
import simpsave as ss

print(ss.read('key1'))  # 输出: 'Hello 世界'
print(ss.read('key2'))  # 输出: 3.14
print(ss.read('key3'))  # 输出: [1, 2, 3, '中文']

# 从不同文件读取
value = ss.read('config', file='settings.yml')
```

---

### 检查键是否存在

`has` 函数用于检测某个键是否存在于文件中:  

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `key`: 要检查的键名.
- `file`: 要检查的文件路径, 默认为 `__ss__.simpsave`.

#### 返回值

* 键存在返回 `True`, 不存在返回 `False`.

#### 示例

```python
import simpsave as ss

print(ss.has('key1'))        # 输出: True
print(ss.has('nonexistent')) # 输出: False
```

---

### 删除键

`remove` 函数用于删除文件中的某个键及其对应值:  

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `key`: 要删除的键名.
- `file`: 要操作的文件路径, 默认为 `__ss__.simpsave`.

#### 返回值

* 成功删除返回 `True`, 失败返回 `False`.

#### 示例

```python
import simpsave as ss

ss.remove('key1')  # 删除键 'key1'
print(ss.has('key1'))  # 输出: False
```

---

### 正则匹配键

`match` 函数可通过正则表达式匹配所有符合条件的键, 并返回对应的键值对:  

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### 参数说明

- `re`: 正则表达式字符串, 用于匹配键名.空字符串表示匹配所有键.
- `file`: 要操作的文件路径, 默认为 `__ss__.simpsave`.

#### 返回值

- 返回一个字典, 包含所有匹配的键值对.

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

---

### 删除文件

`delete` 函数可删除整个存储文件:  

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### 参数说明

- `file`: 要删除的文件路径, 默认为 `__ss__.simpsave`.

#### 返回值

- 成功删除返回 `True`, 失败返回 `False`.

#### 示例

```python
import simpsave as ss

ss.delete()  # 删除默认的保存文件
ss.delete(file='config.yml')  # 删除指定文件
```

---

## 注: 使用 REDIS 引擎

`REDIS` 引擎将数据存储在内存中, 断电即失. 使用前需要确保 Redis 服务已启动  

```python
import simpsave as ss

# 使用 REDIS 引擎（文件参数会被用作 Redis 键前缀）
ss.write('key1', 'value1', file='redis://localhost:6379/0')
print(ss.read('key1', file='redis://localhost:6379/0'))
```

`REDIS` 引擎需要安装 `redis-py` 依赖: `pip install simpsave[REDIS]`  

> 了解更多, 访问 [GitHub](https://github.com/Water-Run/SimpSave)  

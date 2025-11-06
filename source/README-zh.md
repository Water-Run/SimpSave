# SimpSave 版本 10

## 简介

**SimpSave 4.0** 是一个轻量级的 Python 数据持久化库，用于实现简单高效的数据保存。
该版本**已升级为使用 `.yml` 文件**进行存储，相比旧版 `.ini` 格式，它对 Unicode 与复杂数据结构的支持更完善，不再需要 UTF-8 编码或转义操作。

### 特性

* **极度简洁**：整个项目代码量不到 200 行。
* **易于使用**：无需复杂配置，API 简洁直观，快速集成。
* **灵活轻量**：支持所有 Python 基础类型（含 Unicode），除 `PyYAML` 外无其他依赖。
* **原生 YAML 支持**：原生支持 Unicode 与结构化数据——再也不用担心转义或编码问题。

> 向下兼容 SimpSave 4.0 版本。

---

## 安装

SimpSave 4.0 已发布在 PyPI，可通过以下命令安装：

```bash
pip install simpsave
```

> **注意：** SimpSave 4.0 依赖 [`PyYAML`](https://pypi.org/project/PyYAML/)，使用 pip 安装时会自动下载。

在项目中导入：

```python
import simpsave as ss  # 通常简写为 'ss'
```

---

## 原理

SimpSave 4.0 使用 `.yml` 文件以键值对（key-value）的形式保存 Python 的基础类型数据。
默认会将数据保存到当前工作目录下的 `__ss__.yml` 文件中，也可手动指定路径。

### 唯一路径模式

与旧版相同，SimpSave 支持独特的 `:ss:` 路径模式。
如果文件路径以 `:ss:` 开头（例如 `:ss:config.yml`），文件会被保存在 SimpSave 的安装目录中，从而保证跨环境兼容性。

> 注意：`:ss:` 模式要求通过 `pip` 安装 SimpSave。

### `.yml` 文件示例

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

当读取数据时，SimpSave 会自动将其恢复为原始的 Python 类型。
SimpSave 4.0 完整支持 Python 内置类型，包括 `list`、`dict` 以及 Unicode 字符串。

---

## 使用指南

### 写入数据

`write` 函数用于向指定的 `.yml` 文件中写入键值对：

```python
def write(key: str, value: any, *, file: str | None = None) -> bool:
    ...
```

#### 参数说明：

* `key`：要存储的键，必须是合法的 YAML 键名。
* `value`：要存储的值，支持 Python 基础类型（如 `int`、`float`、`str`、`list`、`dict`）。
* `file`：要写入的 `.yml` 文件路径，默认为 `__ss__.yml`，可使用 `:ss:` 模式。

#### 返回值：

* 成功写入返回 `True`，失败返回 `False`。

#### 示例：

```python
import simpsave as ss
ss.write('key1', 'Hello 世界')      # 写入 Unicode 字符串
ss.write('key2', 3.14)             # 写入浮点数
ss.write('key3', [1, 2, 3, '中文']) # 写入包含中文的列表
```

> 如果文件不存在，SimpSave 会自动创建。

---

### 读取数据

`read` 函数用于从指定的 `.yml` 文件中读取数据：

```python
def read(key: str, *, file: str | None = None) -> any:
    ...
```

#### 参数说明：

* `key`：要读取的键名。
* `file`：要读取的 `.yml` 文件路径，默认为 `__ss__.yml`。

#### 返回值：

* 返回指定键对应的值，并自动恢复为原始类型。

#### 示例：

```python
import simpsave as ss
print(ss.read('key1'))  # 输出: 'Hello 世界'
print(ss.read('key2'))  # 输出: 3.14
```

---

### 附加功能

#### 检查键是否存在

`has` 函数用于检测某个键是否存在于 `.yml` 文件中：

```python
def has(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 示例：

```python
import simpsave as ss
print(ss.has('key1'))        # 输出: True
print(ss.has('nonexistent')) # 输出: False
```

---

#### 删除键

`remove` 函数用于删除 `.yml` 文件中的某个键及其对应值：

```python
def remove(key: str, *, file: str | None = None) -> bool:
    ...
```

#### 示例：

```python
import simpsave as ss
ss.remove('key1')  # 删除键 'key1'
```

---

#### 正则匹配键

`match` 函数可通过正则表达式匹配所有符合条件的键，并返回对应的键值对：

```python
def match(re: str = "", *, file: str | None = None) -> dict[str, any]:
    ...
```

#### 示例：

```python
import simpsave as ss
result = ss.match(r'^key.*')  # 匹配所有以 key 开头的键
print(result)  # 输出: {'key2': 3.14, 'key3': [1, 2, 3, '中文']}
```

---

#### 删除文件

`delete` 函数可删除整个 `.yml` 文件：

```python
def delete(*, file: str | None = None) -> bool:
    ...
```

#### 示例：

```python
import simpsave as ss
ss.delete(file='__ss__.yml')  # 删除默认的保存文件
```

## 总结

SimpSave 4.0 是一个简洁、灵活、轻量的 Python 数据持久化库，使用 `.yml` 文件保存基础数据类型。
凭借其简单的 API、原生 Unicode 支持以及对常用数据类型的兼容性，SimpSave 是中小型项目中理想的轻量数据存储方案。

> 了解更多请访问 [GitHub](https://github.com/Water-Run/SimpSave)。

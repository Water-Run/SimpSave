# SimpSave: 简单的持久化Python变量     

`适配版本: 0.80`    

## 简介  
正如名字所示，SimpSave 是一个轻量级的 Python 库, 通过在.ini文件中格式化存储键值对来持久化存储变量，非常适合小型及临时项目的使用。

SimpSave 具备以下特点：  
- **简单**：项目代码由不到 1000 行的结构清晰代码组成，便于快速理解和使用。
- **易学**：只需基本的 Python 知识，不需要复杂的教程。大多数情况下，用户可以在十分钟内上手该库。同时,本文档提供了循序渐进的详细教程, 在阅读后精通此库也十分容易.  
- **扩展功能**: SimpSave实现了包括基本的对称加密, 匹配, 类型检查等扩展功能, 有效的简化了日常使用.  
- **轻量,但足够用的结构**: SimpSave有效的利用了Python原生强大的基本数据结构,包括`list`和`dict`,满足相当多情况的使用.      

> 该项目已发布在 PyPi 上。

## 使用指南  
以下提供一份通俗易懂的使用指南.很建议在使用SimpSave之前完整的阅读.  

#### 安装SimpSave  
- 通过 `pip` 安装 SimpSave：  
  ```bash
  pip install simpsave
  ```
> 注意不是 `simplesave`  

- 将 SimpSave 导入代码中（通常为 `ss`）：  
  ```python
  import simpsave as ss
  ```
  在之后的教程中, 我们均假设已编写该`import`语句.  

> 运行SimpSave需要3.10以上的Python版本  

#### 从初始化开始     
要使得数据能够持久化储存,显然我们需要在ROM下创建一个文件.在SimpSave中,这个创建的过程称为初始化.(当然,也包含一些其它的SimpSave信息).  
初始化使用`init()`实现:  
```python
# 最简单的初始化
ss.init()
```
> 别忘记`import simpsave as ss`!  
> 你可能会发现, 如果再次运行程序, 会出现`FileExistsError`.这是因为`init()`默认设定`overwrite_check = True`避免覆写内容. 尝试`init(overwrite_check = False)`.     
>> 在使用中务必小心设置`overwrite = False`. 否则, 你的数据很容易因为重复初始化而毁于一旦.   

在运行代码后,你大概会发现在你的代码路径下多了一个`__ss__.ini`文件.恭喜!你成功创建了SimpSave的第一个实例.  

> `__ss__.ini`是SimpSave的默认文件名.你可以通过修改`init()`中的`operation_file`进行修改.有关文件名的更多内容,见后文更换文件的部分.  

建议为你的SimpSave实例添加描述.操作很简单,`init()`第一个参数即是描述:  
```python
ss.init("First SimpSave!")
```  
> 也可以通过设置`description=`显式的进行修改  
从初始化开始,让我们正式的掌握SimpSave.  

##### 是否ready()  
如何判断我们的SimpSave实例是否可用?很简单,只需要使用`ready()`即可.它会返回一个布尔值,指示SimpSave的可用信息:  
```python
if ss.ready():
  print('Very Good')
else:
  print('Oh no')
```
当然也可以修改SimpSave的实例对象:
```python
ss.ready('No Such File.ini') # 当然,False
```
> 和`init()`一样,修改文件路径即修改`operation_file`.事实上,各个可用的方法都如此!  

#### 简单的写入和读取 
##### 写入数据   
##### 写进去了吗?has()  
##### 使用预设初始化  
##### 关于类型  
##### 读取数据    
##### 批量输入  

#### 示例程序: HelloWorld   
接下来, 让我们编写一个最简单的示例程序:  
```python
import simpsave as ss # 导入SimpSave
ss.init() # 初始化, 创建SimpSave实例.ini文件  
ss.write('Hello World', 'Hello World!') # 向键 "Hello World" 写入值 "Hello World!"
# 读取键 "Hello World" 的值并打印
print(ss.read('Hello World')) # Hello World!
```   

#### 注释  
##### 键注释  
##### 文档描述  

#### 示例程序: 计时计数器  

#### 内部字段   
##### 概念  
##### 具体各字段及使用  

#### 数据保护    
##### 键锁  
想要保护你的数据不被异常修改,可以使用SimpSave通过`lock()`提供的键锁功能.`lock()`函数需要被设置的键和设置键锁状态(布尔),被设置锁的键将进入只读状态:  
```python
ss.write('key1', 1)
ss.lock('key1', True) # 将key1的键锁开启
ss.read('key1') # 正常执行  
# 以下操作将导致异常抛出
ss.write('key1', 2)
ss.remove('key1')
ss.lock('key1', False) # 关闭key1的键锁
ss.remove('key1')
ss.has('key1') # False
```  
当然,也可以通过输入键列表和键锁列表进行批量设置:  
```python
ss.lock(['key1', 'key2', 'key3'], [True, False, True]) # 开启key1, key3的锁, 关闭key2的锁  
```
> 键锁的原理本质上是修改内部字段`__lock__`,独立于数据.因此,可以设置不存在的键的锁.   
>> 一种通常的用法是设置不存在的键的锁避免使用特定键     
##### 加密  
键锁可以保护意外情况下修改需要只读的数据.不过,由于SimpSave是明文存储的,它并不能真正保护我们的数据.  
SimpSave提供了基本的加密功能.在写入和读出(及初始化的预设)时,可以进行加解密操作.  
加解密具有相同的密钥.密钥可以是任意的字符串.  
> SimpSave提供的加密是对称加密.因此,务必保存好密钥   
写入时,将修改密钥至`encrypts`字段;读出时,修改密钥至`decrypts`字段.其中值是字符串或字符串数组(批量时):  
```python
ss.write('key1', [1, 2, 3], encrypts = 'seed1')
ss.read('key1') # 无法解析的密文
ss.read('key1', decrypts = 'wrong seed') # 错误,无法正确解密
ss.read('key1', decrypts = 'seed1') # [1, 2, 3]
ss.write(['key2', 'key3'], [[4, 5], 6], decrypts = ['seed2', 'seed3']) # 批量
```  
在`init()`中使用加密方法类似,修改`preset_encrypts`即可.    
> 务必保管好密钥  
> 在使用`match()`时,无法解密. 必须使用`read()`函数解密  
> 尽管SimpSave提供了加密功能,但是这种对称加密的安全性依旧有限.同时,Python代码中明文的密钥也并不安全. 如果你需要更好的安全性,建议使用安全的算法先对数据预处理加密后再保存到SimpSave中  

#### 完整数据    

#### match(): 使用正则表达式匹配   

#### 'ss'方法: 操控SimpSave    
##### 'ss'?  
##### 功能  

#### 可变,可靠: 更换文件   
##### 换一个文件  
在之前的教程中,我们均使用默认的SimpSave INI文件,即在相对路径下创建`_SIMPSAVE_DEFAULTPATH_`中存储的文件名(默认情况下,即`__ss__.ini`).   
在SimpSave提供的每个方法中,均有`operation_file`参数.你可以修改参数至任何你想要名称:  
```python
ss.init(operation_file = 'NewFileName.ini') # 在相对路径下以"NewFileName.ini"为实例初始化  
```
> "任何你想要的名称"不太准确.文件名当然需要当前系统下的合法名称.另外,必须是.ini文件.  
当然,也可以通过这样操作不同的文件:   
```python
... # 假设之前的代码中已经初始化  
ss.write('key1', 'value in file a', operation_file = 'a.ini')
ss.write('key1', 'value in file b', operation_file = 'b.ini')
print(ss.read('key1', opeartion_file = 'a.ini')) # value in file a
print(ss.read('key1', operation_file = 'b.ini')) # value in file b
```
很容易的将各个数据独立化.  
不过,这些使用相对路径的方法还是很不稳定可靠.一个简单的例子是,如果以不同的目录启动,那SimpSave实例的路径也将不同.  
一个简单的方法便是使用绝对路径:  
```python
ss.init(operation_file = 'C:\\absoulte.ini')
```
不过,简单的绝对路径可能并不具有很好的兼容性.另外,这也不太Pythonic. 
那有没有更优雅的方式呢?  
##### 路径解析器   
SimpSave提供了一个路径解析器,在每次输入路径时都将自动处理:  
1. 以`::py?`作为文件名开头,将SimpSave实例存储于当前Python环境目录下的ssdatas文件夹中   
2. 以`::ss?`作为文件名开头,将SimpSave实例存储于当前SimpSave包(需要首先使用pip安装SimpSave)目录下的ssdatas文件夹中   
示例:  
```python
ss.init(operation_file = '::py?ss_in_py.ini')
ss.init(operation_file = '::ss?ss_in_ss.ini')
```  
通过这种方式,将文件统一存放,便于管理与使用.我们建议使用这种方式进行存储.   
> (很容易遗忘)如果使用自定义名称, 所有调用的方法都需要你手动设定`operation_file`. 否则,随时出现`FileNotFoundError`等异常.如果你觉得这太麻烦了,你可以修改`_SIMPSAVE_DEFAULTPATH_`来修改默认文件名.  

#### 更高级的使用SimpSave  
##### write()的更高级用法   
##### 通用结构   
##### 其它函数的高级用法        
##### 日志  

## 库概述  

#### 基本方法  

#### 'ss'方法  

#### 其它  

## 开源与联系  
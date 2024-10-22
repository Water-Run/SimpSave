# SimpSave     
## 简介  
SimpSave就如其名,是一个提供简单的将变量持久化的功能的极轻量Python库.很适合在如学生作业等小型脚本使用.  
SimpSave具备以下特点:  
- 极其简单:项目只有不到200行代码构成  
- 极易上手:使用极其容易,(在很大程度上)不需要看任何教程即可在1分钟内学会使用  

> 项目已发布于PyPi      
## 使用  
#### 安装  
- 使用pip安装  
```bash
pip install simpsave
```
- 在你的代码中导入库(一般简称为ss)
```python
import simpsave as ss
... # your code
```  
#### 基本概念  
SimpSave支持持久化存储Python的基本类型值.  
SimpSave将待存储及读出的数据封装到类`Unit`中.其构造需要两个参数:***name*** `str` 和***value*** `any`.  
在一切开始之前,我们需要使用`ready`方法来进行判断SimpSave是否已就绪.如果没有(初次使用),使用`init`方法进行初始化已就绪.  
使用提供的`write`,`read`及`remove`方法,实现对数据的增删查改.  
以下提供简单的代码示例:  
```python
import simpsave as ss # 以ss为别名导入simpsave

# 创建一个SimpSave Unit first ss unit, 其值为Hello World!
a = ss.Unit("first ss unit","Hello World!")

# 将a写入文件,进行持久化储存.(auto_init会自动的创建.ini文件)
ss.write(a)

# 读取名称为a的值,并打印
print(ss.read(a.get_name()))
```   
SimpSave单元的名称可以是任何字符串.不过,需要确保名称的唯一性.  
关于SimpSave方法的具体使用及其他方法,见下一小节.  
另在GitHub上,提供了一些示例程序.可以下载已进一步了解这个简单的库.  

#### 库概览     
1. 变量  
- `SIMPSAVE_FILENAME`:`str`类型,控制用于存储的INI文件的名称.修改时注意包含`.ini`后缀.   
2. 类  
- `Unit`: SimpSave的存储单元.构造时,需要属性`name`(单元的名称,`str`),`value`(单元的值,`any`(Python的基本类型)).自动创建属性`type`用于存储当前类型.  
提供以下方法:
`get_name()`: 返回单元名称 `str` 
`get_value()`: 返回单元的值 `any`    
`get_type()`: 返回单元的类型 `type`  
`rename(name: str)`:  重命名为新名称 
`reset(value: any)`:  重设单元的值为新值  
> 建议使用提供的`rename`和`reset`方法而不是直接修改属性避免类型错误  

另外,实现了`__str__`方法,可以直接转换为字符串(使用`print`打印时很有用).      
3. 函数  

## 实现  
SimpSave的实现基于在项目目录下创建指定名称的`.ini`文件.  
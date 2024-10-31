"""
@file StudentManagementSystem.py
@author WaterRun
@version 1.0
@date 2024-10-28
@description simpsave示例程序:学生管理系统
"""
import simpsave as ss

SS_FILE = 'ssDemo-SMS.ini'

class Student:
    def __init__(self, id:str, name:str, score:float, is_important:bool):
        self.id = id
        self.name = name
        self.score = score
        self.is_important = is_important
        
    def get_dict(self):
        return {'id': self.id, 'name': self.name, 'score': self.score, 'is_important': self.is_important}
    
    def __str__(self):
        return f"{self.id}\t{"(重点)" if self.is_important else ""}\n姓名: {self.name}\n成绩: {self.score}"

_data_source_: list[Student] = []

def _legal_(id: str, name: str, score: float, contain_id: bool) -> bool:
    
    if not len(id) == 4 and id.isdigit():
        print(f"不合法的id: {id}\n确认id由四位纯数字构成")
        return False
    
    try:
        score = float(score)
    except TypeError:
        print(f"不合法的score: {score}\n确认score为数字")
                
    if not (0 <= score <= 100):
        print(f"不合法的score: {score}\n确认score的范围在0-100")
        return False
    
    ids = [i.id for i in _data_source_]
    
    if id in ids and not contain_id:
        print(f'不合法的id: {id}\nid已存在,使用"mdfy"指令进行修改')
        return False
    elif id not in ids and contain_id:
        print(f'不合法的id: {id}\nid不存在,使用"add"指令进行添加')
        return False
    
    return True

def help():
    ...
    
def add(command:list[str]):
    
    if not (len(command) == 5 or len(command) == 4):
        print('add:解析错误.输入"help"获取帮助')
        return
    
    id, name, score = command[1], command[2], command[3]
    
    if len(command) == 5 and command[4] == '-i':
        is_important = True
    else:
        is_important = False
    
    if not _legal_(id, name, score, False):
        print('add:解析错误.输入"help"获取帮助')
        return
    
    _data_source_.append(Student(id, name, float(score), is_important))
    print("数据已更新") if ss.write('students',[i.get_dict() for i in _data_source_], overwrite=True, operation_file=SS_FILE) else print("写入失败警告:内存与SimpSave不同步")
    
def delete(command:list[str]):
    
    if len(command) != 2:
        print('delete:解析错误.输入"help"获取帮助')
        return
        
    id = command[1]
    
    for student in _data_source_:
        if student.id == id:
            _data_source_.remove(student)
            print("数据已更新") if ss.write('students',[i.get_dict() for i in _data_source_], overwrite=True, operation_file=SS_FILE) else print("写入失败警告:内存与SimpSave不同步")
            return
    
    print(f'delete:无法执行, 找不到id: {id}')
    
def search(command:list[str]):
    
    result = []
    
    if len(command) == 2:
        
        id = command[1]
        for student in _data_source_:
            if student.id == id:
                result.append(student)
                break
            
    elif len(command) == 3 or len(command) == 4:
        
        if command[1] != '-n':
            print('search:解析错误.输入"help"获取帮助')
            
        if len(command) == 4 and command[3] != '-s':
            print('search:解析错误.输入"help"获取帮助')
            
        name = command[2]
        result = []
    
        for student in _data_source_:
            if len(command) == 4 and student.name == name:
                result.append(student)
                break
            elif len(command) == 3 and name in student.name:
                result.append(student)
                break
    else:
        print('search:解析错误.输入"help"获取帮助')
    
    for i in result:
        print(i)    
        
    print(f'\n-- {len(result)}个结果 --')
    
def modify(command:list[str]):
    ...
    
def admin(command:str):
    
    if command == 'admin-cls':
        if input('这将清除所有数据.确认(y)>>') == 'y':
            print('SimpSave已清除,立即重启程序') if ss.clear_ss(SS_FILE) else print('异常:SimpSave清除失败')
        else:
            print('命令已取消')
    elif command == 'admin-show':
        ...
    elif command == 'admin-ssinf':
        ...
    else:
        print('admin:无法执行, 不在可选命令中')
        
def parser(command:str):
    
    if command.startswith('help'):
        help()
    elif command.startswith('add'):
        add(command.split())
    elif command.startswith('del'):
        delete(command.split())
    elif command.startswith('srh'):
        search(command.split())
    elif command.startswith('mdfy'):
        modify(command.split())
    elif command.startswith('admin'):
        admin(command)
    else:
        print('非法指令.输入"help"获取帮助')
    
if __name__ == '__main__':
    print('欢迎使用SimpSave示例程序:学生管理系统')
    
    if not ss.ready(SS_FILE):
        ss.init(['count', 'students'], [count:=0,[]], operation_file=SS_FILE)
        print("-- 初始化SimpSave --")
    else:
        ss.write('count', count:=(ss.read('count', operation_file=SS_FILE)+1), operation_file=SS_FILE)
        
    if not ss.has('students', operation_file=SS_FILE):
        raise RuntimeError('无法运行SimpSave Demo: Student Management System')
    
    print(f'SimpSave实例于{SS_FILE}, 该程序已经运行{count}次\n">>"表示等待输入;"help"获取帮助,"exit"退出')
    
    for i in ss.read('students', operation_file=SS_FILE):
        _data_source_.append(Student(i['id'], i['name'], i['score'], i['is_important']))
    
    print(f'-- 从SimpSave中读取了条{len(_data_source_)}数据 --\n提示:id为4位纯数字字符串,name不可使用空格等spilt开,score范围在0-100之间')
    while True:
        command = input(">>")
        if command == 'exit':
            break
        parser(command)
    print('bye')
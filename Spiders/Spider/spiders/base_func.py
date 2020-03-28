"""
- Python3.6

"""
import os

def rm_file(file_name, isprint=True):
    if file_name and os.path.exists(file_name):
        os.remove(file_name)
        if isprint:
            print("删除文件[%s]成功" % file_name)

def read_file(file_name, isprint=False):
    u" 读取文件 "
    if not file_name or not os.path.exists(file_name):
        return []

    with open(file_name, 'rb') as f:
        data = f.readlines()
    data = [str(a, encoding='utf-8').replace(r'\n','') for a in data]

    if isprint:
        print("读取文件[%s]成功" % file_name)
    return data

def write_file(file_name, data, mode='append', isprint=False):
    u" 写入文件 "
    if not file_name:
        # 创建空文件
        return os.mknod(file_name)  

    for row in data:
        cmd = """ echo "%s" >> "%s" """ %(row, file_name)
        os.system(cmd)

    return
    with open(file_name, 'wb') as f:
        if mode == 'append':
            data = read_file(file_name) + data
        else:
            data = data

        for row in data:
            _row = row + '\n'
            _row = bytes(_row, encoding='utf-8')
            f.write(_row)
    if isprint:
        print("写入文件[%s]成功" % file_name)
        



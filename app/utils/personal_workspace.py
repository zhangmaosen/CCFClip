from tinydb import TinyDB, Query
from datetime import datetime

def create_workspace(data : dict, path='db/tinydb/db.json'):
    
    db = TinyDB(path)
    workspace = Query()
    
    # 获取当前日期和时间
    now = datetime.now()

    # 提取到秒的部分
    current_time_seconds = now.strftime("%H:%M:%S")
    print("当前时间到秒:", current_time_seconds)
    data = {**data, **{'time': current_time_seconds}}
    db.insert(data)
    return data
def create_workspace_by_name(name, path='db/tinydb/db.json'):
    
    db = TinyDB(path)
    workspace = Query()
    
    # 获取当前日期和时间
    now = datetime.now()

    # 提取到秒的部分
    current_time_seconds = now.strftime("%H:%M:%S")
    print("当前时间到秒:", current_time_seconds)
    data = {**{'name': name}, **{'time': current_time_seconds}}
    db.insert(data)
    return data
def get_workspaces(path='db/tinydb/db.json'):
    db = TinyDB(path)
    workspace = Query()
    wks_list = db.search(workspace.name != '')
    #print(f'wks_list:{wks_list}')
    return wks_list

def get_workspace_names():
    lists = get_workspaces()
    names = [i['name'] + ' at ' + i['time'] for i in lists]
    print(f'names is {names}')
    return names

def get_workspace_name_by_data(data):
    return data['name'] + ' at ' + data['time']

def save_workspace_data(data:dict, path='db/tinydb/db.json'):
    db = TinyDB(path)
    #workspace = Query()
    print(f' data is {data}')
    # 获取当前日期和时间
    now = datetime.now()

    # 提取到秒的部分
    current_time_seconds = now.strftime("%H:%M:%S")
    #print("当前时间到秒:", current_time_seconds)
    data = {**data, **{'time': current_time_seconds}}
    print(data)
    # db.insert(data)
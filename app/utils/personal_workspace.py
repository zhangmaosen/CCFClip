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

def get_workspaces(path='db/tinydb/db.json'):
    db = TinyDB(path)
    workspace = Query()
    return db.search(workspace.name != '')
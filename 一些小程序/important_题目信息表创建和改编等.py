import os, re
def create_new_dict(id_num):
    dict = {}
    try:
        dict["id"] = str(id_num).zfill(6)
        if re.match(r"^[\d]{6}$",dict["id"]) == None:
            print("id有误.")
            return(-1)
    except:
        print("id有误.")
        return(-1)
    dict["content"] = ""
    dict["objs"] = [] 
    dict["tags"] = [] 
    dict["genre"] = "" 
    dict["ans"] = ""
    dict["solution"] = ""
    dict["duration"] = -1
    dict["usages"] = []
    dict["origin"] = ""
    dict["edit"] = []
    dict["same"] = []
    dict["related"] = []
    dict["remark"] = ""
    dict["space"] = ""
    return(dict)

def add_content(string,dict):
    if dict["content"] != "":
        print(dict["id"], "题目已有内容.")
    else:
        dict["content"] = trim(string)
    return(dict)

def add_obj(string,dict):
    if re.match(r"^(K[\d]{7}[BX])|(KNONE)$",string.upper()) == None:
        print("目标代码", string, "有误.")
    elif not string.upper() in [o.upper() for o in dict["objs"]]:
        dict["objs"].append(string)
    return dict

def add_tag(string,dict):
    if not string.upper() in [o.upper() for o in dict["tags"]]:
        dict["tags"].append(string)
    return dict

def add_genre(string,dict):
    if dict["genre"] == "":
        dict["genre"] = string
    elif dict["genre"] != string:
        print(dict["content"])
        choice = input("原题型:"+dict["genre"]+"; 新题型:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["genre"] = string
    return dict

def add_answer(string,dict):
    if dict["ans"] == "":
        dict["ans"] = string
    elif dict["ans"] != string:
        print(dict["content"])
        choice = input("原答案:"+dict["ans"]+"; 新答案:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["ans"] = string
    return dict

def add_solution(string,dict):
    if dict["solution"] == "":
        dict["solution"] = string
    elif dict["solution"] != string:
        print(dict["content"])
        choice = input("原答案:"+dict["ans"]+";\n 新答案:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["solution"] = string
    return dict

def add_duration(duration,dict):
    if dict["duration"] < 0:
        dict["duration"] = duration
    elif dict["duration"] - duration > 0.01 or dict["duration"] - duration < -0.01:
        print(dict["content"])
        choice = input("原预计耗时:%.2f" %dict["duration"]+";\n 新预计耗时:%.2f" %duration+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["duration"] = duration
    return dict

def add_usage(string,dict):
    for usage in dict["usages"]:
        if re.sub(r"[\s]","",usage) == re.sub(r"[\s]","",string):
            return dict
    dict["usages"].append(string)
    return dict
    
def add_origin(string,dict):
    if dict["origin"] == "":
        dict["origin"] = string
    elif not string in dict["origin"]:
        print("原出处:"+dict["origin"])
        choice = input("新增出处:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["origin"] = trim(dict["origin"]+"\n"+string)
    return dict

def add_editor_history(string,dict):
    for edit in dict["edit"]:
        if re.sub(r"[\s]","",edit) == re.sub(r"[\s]","",string):
            return dict
    dict["edit"].append(string)
    return dict

def add_same_problem_id(id,dict):
    if re.match(r"^[\d]{6}$",id) == None:
        print("相同题目ID",id,"有误.")
    else:
        if not id in dict["same"]:
            dict["same"].append(id)
    return(dict)

def add_related_problem_id(id,dict):
    if re.match(r"^[\d]{6}$",id) == None:
        print("关联题目ID",id,"有误.")
    else:
        if not id in dict["related"]:
            dict["related"].append(id)
    return(dict)

def add_remark(string,dict):
    if dict["remark"] == "":
        dict["remark"] = string
    elif dict["remark"] != string:
        print(dict["content"])
        choice = input("原备注:"+dict["remark"]+";\n新备注:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["remark"] = string
    return dict

def add_space(string,dict):
    if dict["space"] == "":
        dict["space"] = string
    elif dict["space"] != string:
        print(dict["content"])
        choice = input("原备注:"+dict["space"]+"; 新备注:"+string+". 确认替换(Y/N):")
        if choice.upper() == "Y":
            dict["space"] = string
    return dict
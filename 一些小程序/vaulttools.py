import re,os
def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string

def get_problem_sets(string):
    # 根据字符串返回题目列表, 每道题目从[B题目]开始, 到[E题目]结束.
    return(re.findall(r"\[B题目\][\s\S]*?\[E题目\]",string))

def get_id(string):
    #单个problem_set, 取出ID. 多个problem_set或没有problem_set会报错, ID不是六位数码也会报错
    id_list = re.findall(r"<BID>([\s\S]*?)<EID>",string)
    if len(id_list) != 1:
        if len(string)<=100:
            print(string)
        else:
            print(string[:100])
        print("题目ID数量有误.")
    elif len(re.findall(r"[0-9]{6}",id_list[0])) != 1:
        print("题目ID: ",trim(id_list[0]),", 不符合规则(6位数码).")
    else:
        return(trim(id_list[0]))

def get_content(string):
    # 返回problem_set里的题目内容
    content_list = re.findall(r"<B题目>([\s\S]*?)<E题目>",string)
    if len(content_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(content_list[0]))

def objective_test(string):
    if re.match(r"^(K[\d]{7}[BX])|(KNONE)$",string.upper()) == None:
        return False
    else:
        return True

def get_objectives_list(string):
    # 返回problem_set里的关联目标列表
    raw_list = re.findall(r"<B目标>([\s\S]*?)<E目标>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        obj_list = [trim(t) for t in raw_list[0].split("\n") if len(t)>0]
        flag = True
        for obj in obj_list:
            if objective_test(obj) == False:
                flag = False
                try:
                    id = get_id(string)
                    print("题号",id,", 目标格式有误.")
                except:
                    if len(string)<=100:
                        print(string)
                    else:
                        print(string[:100])
                    print("目标格式有误.")
        if flag:
            return(obj_list)
                
def get_tags_list(string):
    # 返回problem_set里的标签列表, 原用|隔开
    raw_list = re.findall(r"<B标签>([\s\S]*?)<E标签>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        tag_list = [trim(t) for t in raw_list[0].split("|") if len(t)>0]
        return(tag_list)

def get_genre(string):
    # 返回problem_set里的题目内容
    genre_list = re.findall(r"<B类型>([\s\S]*?)<E类型>",string)
    if len(genre_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(genre_list[0]))

def get_answer(string):
    # 返回problem_set里的答案内容
    raw_list = re.findall(r"<B答案>([\s\S]*?)<E答案>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(raw_list[0]))

def get_solution(string):
    # 返回problem_set里的解答或提示内容
    raw_list = re.findall(r"<B解答或提示>([\s\S]*?)<E解答或提示>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(raw_list[0]))

def get_duration(string):
    # 返回problem_set里的预计耗时
    raw_list = re.findall(r"<B预计耗时>([\s\S]*?)<E预计耗时>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        duration_string = trim(raw_list[0])
        if duration_string == "":
            duration = -1
            return(duration)
        else:
            try:
                duration = "%.2f" %float(duration_string)
                return(duration)
            except:
                try:
                    id = get_id(string)
                    print("题号",id,", 预计耗时栏目有误.")
                except:
                    if len(string)<=100:
                        print(string)
                    else:
                        print(string[:100])
                    print("预计耗时栏目有误.")
            
def get_usages_list(string):
    # 返回problem_set里的使用记录, 原用回车隔开
    raw_list = re.findall(r"<B使用记录>([\s\S]*?)<E使用记录>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        usage_list = [trim(t) for t in raw_list[0].split("\n") if len(t)>0]
        return(usage_list)

def get_origin(string):
    # 返回problem_set里的出处栏
    raw_list = re.findall(r"<B出处>([\s\S]*?)<E出处>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(raw_list[0]))

def get_edit_history_list(string):
    # 返回problem_set里的修订历史, 原用回车隔开
    raw_list = re.findall(r"<B修订历史>([\s\S]*?)<E修订历史>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        history_list = [trim(t) for t in raw_list[0].split("\n") if len(t)>0]
        return(history_list)

def get_same_problems_list(string):
    # 返回problem_set里的相同题目列表
    raw_list = re.findall(r"<B相同题目>([\s\S]*?)<E相同题目>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        sp_list = [trim(t) for t in raw_list[0].split("\n") if len(t)>0]
        flag = True
        for sp in sp_list:
            if re.match(r"^[\d]{6}$",sp) == None:
                flag = False
                try:
                    id = get_id(string)
                    print("题号",id,", 相同题目列表数据有误.")
                except:
                    if len(string)<=100:
                        print(string)
                    else:
                        print(string[:100])
                    print("相同题目列表数据有误.")
        if flag:
            return(sp_list)

def get_related_problems_list(string):
    # 返回problem_set里的关联题目列表
    raw_list = re.findall(r"<B关联题目>([\s\S]*?)<E关联题目>",string)
    if len(raw_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        rp_list = [trim(t) for t in raw_list[0].split("\n") if len(t)>0]
        flag = True
        for rp in rp_list:
            if re.match(r"^[\d]{6}$",rp) == None:
                flag = False
                try:
                    id = get_id(string)
                    print("题号",id,", 关联题目列表数据有误.")
                except:
                    if len(string)<=100:
                        print(string)
                    else:
                        print(string[:100])
                    print("关联题目列表数据有误.")
        if flag:
            return(rp_list)

def get_remark(string):
    # 返回problem_set里的备注内容
    remark_list = re.findall(r"<B备注>([\s\S]*?)<E备注>",string)
    if len(remark_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(remark_list[0]))

def get_space(string):
    # 返回problem_set里的解答空间内容
    space_list = re.findall(r"<B解答空间>([\s\S]*?)<E解答空间>",string)
    if len(space_list) != 1:
        try:
            id = get_id(string)
            print("题号",id,", 数据结构有误.")
        except:
            if len(string)<=100:
                print(string)
            else:
                print(string[:100])
            print("数据结构有误.")
    else:
        return(trim(space_list[0]))

def setup_dict(string):
    dict = {}
    dict["id"] = get_id(string) #获得id, 格式string
    dict["content"] = get_content(string) #获得题目内容, 格式string
    dict["objs"] = get_objectives_list(string) #获得关联目标, 格式list, 回车分隔
    dict["tags"] = get_tags_list(string) #获得标签, 格式list, |分隔
    dict["genre"] = get_genre(string) #获得题目类型, 格式string
    dict["ans"] = get_answer(string) #获得答案, 格式string
    dict["solution"] = get_solution(string) #获得详细解答, 格式string
    dict["duration"] = get_duration(string) #获得预计耗时, 格式float, 保留两位小数, -1表示空缺
    dict["usages"] = get_usages_list(string) #获得使用记录, 格式list, 回车分隔
    dict["origin"] = get_origin(string) #获得出处, 格式string
    dict["edit"] = get_edit_history_list(string) #获得修订历史, 格式list, 回车分隔
    dict["same"] = get_same_problems_list(string) #获得相同题目列表, 格式list, 回车分隔
    dict["related"] = get_related_problems_list(string) #获得关联题目列表, 格式list, 回车分隔
    dict["remark"] = get_remark(string) #获得备注, 格式string
    dict["space"] = get_space(string) #获得答题空间, 格式string
    return(dict)

def create_string_from_dict(dict):
    head = "[B题目]"
    delimeters_dict = {"id":"ID", "content":"题目", "objs":"目标", "tags":"标签", "genre":"类型", "ans":"答案", "solution":"解答或提示", "duration":"预计耗时", "usages":"使用记录", "origin":"出处", "edit":"修订历史", "same":"相同题目", "related":"关联题目", "remark":"备注", "space":"解答空间"}
    tail = "[E题目]"
    string = ""
    string += head + "\n"
    for item in delimeters_dict:
        string += "<B"+delimeters_dict[item]+">\n"
        if type(dict[item]) == str:
            if len(dict[item])>0:
                string += dict[item] + "\n"
            else:
                string += "\n"
        elif type(dict[item]) == float or type(dict[item]) == int:
            if dict[item] >= 0:
                string += "%.2f" %dict[item] + "\n"
            else:
                string += "\n"
        elif type(dict[item]) == list:
            if item == "tags":
                string += "|".join(dict[item]) + "\n"
            else:
                string += "\n".join(dict[item]) + "\n"
        string += "<E"+delimeters_dict[item]+">"
        string += "\n"
    string += tail
    return(string)

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

def get_problems_string_by_ID(id,string):
    return re.findall(r"\[B题目\][\s]*<BID>[\s]*"+id+r"[\s\S]*?\[E题目\]",string)[0]

def vaults_to_string_and_dicts(directory): #输入目录, 输出题库中所有题目构成的字符串, 字符串构成的词典 和 单个题目词典构成的词典
    if not directory[:-1] in ("/","\\"): 
        directory = directory + "/"
    vaults = [f for f in os.listdir(directory) if "题库" in f]
    problem_str = ""
    for v in vaults:
        with open(directory+v,"r",encoding="utf8") as f:
            problem_str += f.read()
    problem_dicts = {}
    problem_list = {}
    for p in re.findall(r"\[B题目\][\s\S]*?\[E题目\]",problem_str):
        id = get_id(p)
        dic = setup_dict(p)
        problem_list[id] = p
        problem_dicts[id] = dic
    return (problem_str,problem_list,problem_dicts)

def get_gloss_objects(directory): #输入目录, 输出题库中所有课时目标构成的字符串, 字符串构成的词典 和 单个目标词典构成的词典
    if not directory[:-1] in ("/","\\"): 
        directory = directory + "/"
    obj_files = [v for v in os.listdir(directory) if "_" in v and ".txt" in v]
    gloss_str = ""
    for f in obj_files:
        with open(directory + f,"r",encoding="utf8") as obj_f:
            gloss_str += obj_f.read()
    obj_dicts = {}
    obj_lists = {}
    for o in re.findall(r"\[B课时教学目标\][\s\S]*?\[E课时教学目标\]",gloss_str):
        id = re.findall(r"<目标编码>[\s]*(K[\d]{7}[BX])",o)[0]
        unit_obj = re.findall(r"<对应单元目标编码>[\s]*(D[\d]{5}[BX])",o)[0]
        content = trim(re.findall(r"<目标内容>([\s\S]*)<对应单元目标编码>",o)[0])
        obj_lists[id] = o
        obj_dicts[id] = {"id":id,"unit_obj":unit_obj,"content":content}
    return (gloss_str,obj_lists,obj_dicts)
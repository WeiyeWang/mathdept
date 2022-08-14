import re
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
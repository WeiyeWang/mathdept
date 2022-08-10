import os,re


def trim(string):
    string = re.sub(r"^[\s\n ]*?","",string)
    return re.sub(r"[\s\n ]*?$","",string)

def coincide(list, string):
    flag = False
    for element in list:
        if element in string:
            flag = True
    return flag

def get_color(value):
    value = float(value)
    if value>=0.5:
        (r,g,b)=(1,2-2*value,0)
    else:
        (r,g,b)=(2*value,1,0)
    return "{" + "%.3f" %(r) + "," + "%.3f" %(g) + ",0}"


def color_value(matchobj):
    value = matchobj.group(1)
    return "\t"+"\\fcolorbox[rgb]{0,0,0}"+ get_color(value) +"{" + value +"}"
    
def get_objects_list():
    with open("../单元目标叙写/课时目标/课时目标汇总.tex","r",encoding = "utf8") as f:
        objects = [o for o in f.read().split("\n") if len(o)>0]
    object_dict = {}
    for o in objects:
        o = re.sub(r"\\\\[\s]*\\hline","",o)
        o_list = [trim(s) for s in o.split("&")]
        name = o_list[0]
        unit = o_list[1]
        content = o_list[2]
        object_dict[name] = "|"+unit+"|"+content
    return(object_dict)


vault_list = [f for f in os.listdir("../题库0.2") if "题库" in f or "vault" in f]
problems_list = []
for v in vault_list:
    with open("../题库0.2/"+v,"r",encoding = "utf8") as f:
        data = f.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",data)
        for problem in problems:
            problems_list.append(problem)

#这两个需要改动, 前者是标签包含的字符串, 后者是目标中不含的字符串              
unit = "第一单元"
obj_key = "K01"
id_list = []
for p in problems_list:
    obj = re.findall(r"<B目标>([\s\S]*?)<E目标>",p)[0]
    tag = re.findall(r"<B标签>([\s\S]*?)<E标签>",p)[0]
    id = trim(re.findall(r"<BID>([\s\S]*?)<EID>",p)[0])
    if unit in tag and not obj_key in obj:
        id_list.append(id)
id_list_enter = "\n".join(id_list)
with open("../临时/ID列表.txt","w",encoding = "utf8") as f:
    f.write(id_list_enter)
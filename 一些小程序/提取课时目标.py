import os,re
def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def within_range(string,list):
    flag = False
    for item in list:
        if string == trim(item):
            flag = True
            break
        elif ":" in item:
            start, end = item.split(":")
            if start <= string <= end:
                flag = True
                break
    return flag


filelist = [f for f in os.listdir("../单元目标叙写/课时目标") if "_" in f and ".txt" in f]
objects = []
for file in filelist:
    with open("../单元目标叙写/课时目标/"+file,"r",encoding="utf8") as f:
        data = f.read()
    for obj in re.findall(r"\[B课时教学目标\][\s\S]*?\[E课时教学目标\]",data):
        objects.append(obj)

obj_dict = {}
for objdata in objects:
    id = trim(re.findall(r"<目标编码>([\s\S]*?)<目标内容>",objdata)[0])
    content = trim(re.findall(r"<目标内容>([\s\S]*?)<对应单元目标编码>",objdata)[0])
    obj_dict[id] = content

obj_str = input("目标范围:")
obj_list = obj_str.split(",")
output_string = ""
for objid in obj_dict:
    if within_range(objid,obj_list):
        output_string += objid + " & " + obj_dict[objid] + " & " + r"\\ \hline" + "\n"
with open(r"../临时/提取课时目标内容.txt","w",encoding = "utf8") as f:
    f.write(output_string)
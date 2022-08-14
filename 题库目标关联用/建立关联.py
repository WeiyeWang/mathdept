import os,re
#os.chdir("d:/mathdept/题库目标关联用")
def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def recognize_line(string):
    string = re.sub(r"[\s\n\t]+",",",trim(string))
    record = string.split(",")
    return record

#选择文件
files = [f for f in os.listdir("../题库目标关联用") if ".txt" in f]
count = 0
for i in files:
    print(count,":",files[count])
    count += 1
choice = int(input("选择用来关联的文本文件:"))
file = files[choice]
with open("../题库目标关联用/"+file,"r",encoding = "utf8") as f:
    data = f.read()
lines = [recognize_line(line) for line in data.split("\n") if len(line) > 0]

obj_files = [f for f in os.listdir("../单元目标叙写/课时目标") if "_" in f]
obj_str = ""
for f in obj_files:
    with open("../单元目标叙写/课时目标/"+f,"r",encoding="utf8") as obj_file:
        obj_str+=obj_file.read()
obj_list = [trim(t) for t in re.findall(r"<目标编码>([\s\S]*?)<目标内容>",obj_str)]

legal = True
for line in lines:
    id = line.pop(0)
    for t in line:
        if not (t in obj_list) and not (t.upper() == "KNONE"):
            legal = False
            print(t,"有问题.")



if legal:
    vaults = [f for f in os.listdir("../题库0.2") if "题库" in f]
    for line in lines:
        id = line.pop(0)
        id = id.zfill(6)
        for v in vaults:
            (startid,endid)=re.findall("(\d{6})to(\d{6})",v)[0]
            if startid <= id <= endid:
                with open("../题库0.2/"+v,"r",encoding = "utf8") as vault:
                    vault_data = vault.read()
                problem_raw = re.findall("(\[B题目\]\s*?<BID>\s*?"+id+"[\s\S]*?E题目\])",vault_data)[0]
                obj_raw = re.findall("<B目标>([\s\S]*?)<E目标>",problem_raw)[0]
                old_obj = trim(obj_raw).split("\n")
                obj_string = trim(obj_raw) +"\n"
                for obj in line:
                    if not obj in old_obj:
                        obj_string += obj + "\n"
                obj_string = trim(obj_string)+"\n"
                problem_new = problem_raw.replace("<B目标>"+obj_raw+"<E目标>","<B目标>\n"+obj_string+"<E目标>")
                vault_data = vault_data.replace(problem_raw,problem_new)
                with open("../题库0.2/"+v,"w",encoding = "utf8") as vault:
                    vault.write(vault_data)


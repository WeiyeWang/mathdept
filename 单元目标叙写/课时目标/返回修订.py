import re,os
# 修改汇总后可以回复到修改分文件的课时目标
def trim(string):
    if string == "":
        return ""
    else:
        while string[0] in [" ","\t","\n"]:
            string = string[1:]
        while string[-1] in [" ","\t","\n"]:
            string = string[:-1]
        return string
with open("课时目标汇总.tex","r",encoding="utf8") as f:
    gloss = [obj[:-9] for obj in f.read().split("\n") if len(obj)>0]
for i in range(len(gloss)):
    line = trim(gloss[i])
    if line[-1] != ".":
        line += "."
    gloss[i] = line
filelist = [f for f in os.listdir() if ".txt" in f]

for line in gloss:
    (a,b,c) = line.split("&")
    a,b,c = trim(a),trim(b),trim(c)
    for f in filelist:
        with open(f,"r",encoding="utf8") as obj_file:
            data = obj_file.read()
        res = re.findall(r"(<目标编码>\s*?"+a+r"\s*?<目标内容>([\s\S]*?)<对应单元目标编码>([\s\S]*?)<)",data)
        if len(res) > 0:
            obj_contents_new = "\n"+ c +"\n"
            obj_unitno_new = "\n"+ b +"\n"
            obj_unitno_raw = res[0][2]
            obj_contents_raw = res[0][1]
            text_raw = res[0][0]
            text_new = text_raw.replace(obj_unitno_raw,obj_unitno_new).replace(obj_contents_raw,obj_contents_new)
            data = data.replace(text_raw,text_new)
            with open(f,"w",encoding = "utf8") as output_obj:
                output_obj.write(data)
            break
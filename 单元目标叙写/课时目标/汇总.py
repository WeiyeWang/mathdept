import os,re
def trim(string):
    if string == "":
        return ""
    else:
        while string[0] in [" ","\t","\n"]:
            string = string[1:]
        while string[-1] in [" ","\t","\n"]:
            string = string[:-1]
        return string
#os.chdir(r"D:\mathdept\单元目标叙写\课时目标")
filelist = [f for f in os.listdir() if ".txt" in f]
data = ""
for f in filelist:
    with open(f,"r",encoding = "utf8") as datafile:
        data += datafile.read()
objects = []
for obj in re.findall(r"<目标编码>([\s\S]*?)<目标内容>([\s\S]*?)<对应单元目标编码>([\s\S]*?)<叙写",data):
    objects.append((trim(obj[0]),trim(obj[2]),trim(obj[1])))
texfile_string = ""
for obj in objects:
    texfile_string += obj[0] + " & " + obj[1] + " & " + obj[2] + r"\\ \hline" +"\n"
with open("课时目标汇总.tex","w",encoding="utf8") as output_file:
    output_file.write(texfile_string)
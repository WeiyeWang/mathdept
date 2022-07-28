#同时汇总了课时目标和课时划分

import os,re,time
from shutil import copyfile
def trim(string):
    string = re.sub(r"^[\s\n ]*?","",string)
    return re.sub(r"[\s\n ]*?$","",string)
#os.chdir(r"单元目标叙写")
filelist_lessons = [f for f in os.listdir("课时划分") if ".txt" in f]

objects = []
for f in filelist_lessons:
    with open("课时目标/"+f,"r",encoding = "utf8") as object_file:
        objects_raw = object_file.read()
    object_contents_raw = [trim(s) for s in re.findall(r"(\[B课时教学目标\][\s\S]+?\[E课时教学目标\])",objects_raw)]
    for o in object_contents_raw:    
        objects.append(trim(re.findall(r"(<目标编码>[\s\S]+?<叙写人员>)",o)[0]))

lessons = []
for f in filelist_lessons:
    with open("课时划分/"+f,"r",encoding = "utf8") as lesson_file:
        lessons_raw = lesson_file.read()
    lessons_contents_raw = [trim(s) for s in re.findall(r"(\[B课时\][\s\S]+?\[E课时\])",lessons_raw)]
    unit_sort = f[0]
    for l in lessons_contents_raw:
        lesson_sort = trim(re.findall(r"<课时顺序>([\s\S]+?)<起始页码>",l)[0])
        page_start = trim(re.findall(r"<起始页码>([\s\S]+?)<终止页码>",l)[0])
        page_end = trim(re.findall(r"<终止页码>([\s\S]+?)\[E课时\]",l)[0])
        lessons.append((unit_sort,lesson_sort,page_start,page_end))

output_string = ""
for l in lessons:
    (unit_sort,lesson_sort,page_start,page_end) = l
    output_string += r"\section*{第"+ unit_sort + "单元, 第"+ lesson_sort + "课时}\n"
    output_string += "起始页码: "+page_start+"; 终止页码: "+page_end + ".\n"+r"\begin{itemize}" + "\n"
    lesson_object_index = "K"+unit_sort.zfill(2)+lesson_sort.zfill(2)
    for o in objects:
        if lesson_object_index in o:
            index1 = trim(re.findall(r"<目标编码>([\s\S]*?)<目标内容",o)[0])
            index2 = trim(re.findall(r"<对应单元目标编码>([\s\S]*?)<叙写",o)[0])
            content = trim(re.findall(r"<目标内容>([\s\S]*?)<对应",o)[0])
            output_string += r"\item " + index1 + "|" + index2 + "|" + content + "\n"
    output_string += r"\end{itemize}"+"\n\n"

with open("课时划分/课时划分汇总.tex","w",encoding = "utf8") as f:
    f.write(output_string)   

filelist = [f for f in os.listdir("课时目标") if ".txt" in f]
data = ""
for f in filelist:
    with open("课时目标/"+f,"r",encoding = "utf8") as datafile:
        data += datafile.read()
objects = []
for obj in re.findall(r"<目标编码>([\s\S]*?)<目标内容>([\s\S]*?)<对应单元目标编码>([\s\S]*?)<叙写",data):
    objects.append((trim(obj[0]),trim(obj[2]),trim(obj[1])))
texfile_string = ""
for obj in objects:
    texfile_string += obj[0] + " & " + obj[1] + " & " + obj[2] + r"\\ \hline" +"\n"
with open("课时目标/课时目标汇总.tex","w",encoding="utf8") as output_file:
    output_file.write(texfile_string)

os.chdir("课时目标/课时目标汇总")
os.system("xelatex 课时目标.tex")
os.system("xelatex 课时目标.tex")
os.chdir("../../课时划分/课时划分汇总")
os.system("xelatex 课时划分.tex")
os.system("xelatex 课时划分.tex")
os.chdir("../..")
current_time = time.localtime()
time_string = "_"+str(current_time.tm_year).zfill(4)+str(current_time.tm_mon).zfill(2)+str(current_time.tm_mday).zfill(2)
copyfile("课时目标/课时目标汇总/课时目标.pdf","课时目标"+time_string+".pdf")
copyfile("课时划分/课时划分汇总/课时划分.pdf","课时划分"+time_string+".pdf")


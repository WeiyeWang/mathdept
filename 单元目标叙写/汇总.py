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

#统计每个目标, 每个课时, 每个单元对应的题目数量及题目
oid = re.findall(r"K[\d]{7}[BX]","".join(objects))
objects_id = {}
units_id = {}
lessons_id = {}
for o in oid:
    unit = o[:3]
    lesson = o[:5]
    if o in objects_id:
        objects_id[o][0] += 1
    else:
        objects_id[o] = [1,0,""]
    if unit in units_id:
        units_id[unit][0] += 1
    else:
        units_id[unit] = [1,0,""]
    if lesson in lessons_id:
        lessons_id[lesson][0] += 1
    else:
        lessons_id[lesson] = [1,0,""]

vault_list = [f for f in os.listdir("../题库0.2") if "题库" in f or "vault" in f]
for v in vault_list:
    with open("../题库0.2/"+v,"r",encoding = "utf8") as f:
        data = f.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",data)
        for problem in problems:
            p_id = trim(re.findall(r"<BID>([\s\S]*?)<EID>",problem)[0])
            p_objs = [obj for obj in trim(re.findall(r"<B目标>([\s\S]*?)<E目标>",problem)[0]).split("\n") if len(obj)>0]
            for p_obj in p_objs:
                objects_id[p_obj][1] += 1
                objects_id[p_obj][2] += p_id+", "
                if not p_id in lessons_id[p_obj[:5]][2]:
                    lessons_id[p_obj[:5]][1] += 1
                    lessons_id[p_obj[:5]][2] += p_id+", "
                if not p_id in units_id[p_obj[:3]][2]:
                    units_id[p_obj[:3]][1] += 1
                    units_id[p_obj[:3]][2] += p_id+", "

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
            output_string += r"\item " + index1 + "|" + index2 + "|" + content + "\n\n"
            output_string += r"关联题目数量: " + str(objects_id[index1][1]) + r". 关联题目id: " + objects_id[index1][2][:-2] + "\n\n"
    output_string += r"\item 本课时题目数量: " + str(lessons_id[lesson_object_index][1]) + r". 关联题目id: " + lessons_id[lesson_object_index][2][:-2] + "\n\n"
    output_string += r"\end{itemize}"+"\n\n"

objects_text = ""
for id in objects_id:
    objects_text += id + "|目标数: " + str(objects_id[id][0]) +  "|题目数: " + str(objects_id[id][1]) + "|对应题目: " + str(objects_id[id][2][:-2]) + "\n" 
lessons_text = ""
for id in lessons_id:
    lessons_text += id + "|目标数: " + str(lessons_id[id][0]) +  "|题目数: " + str(lessons_id[id][1]) + "|对应题目: " + str(lessons_id[id][2][:-2]) + "\n" 
units_text = ""
for id in units_id:
    units_text += id + "|目标数: " + str(units_id[id][0]) +  "|题目数: " + str(units_id[id][1]) + "|对应题目: " + str(units_id[id][2][:-2]) + "\n" 

with open("题库统计/目标题目汇总.txt","w",encoding = "utf8") as f:
    f.write(objects_text)
with open("题库统计/课时题目汇总.txt","w",encoding = "utf8") as f:
    f.write(lessons_text) 
with open("题库统计/单元题目汇总.txt","w",encoding = "utf8") as f:
    f.write(units_text) 

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


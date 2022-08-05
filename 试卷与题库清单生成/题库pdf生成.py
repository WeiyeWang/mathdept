import os,re

def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string

def color_value(matchobj):
    value = matchobj.group(1)
    return "\t"+"\\textcolor{red!"+ "%.3f" %(100*float(value)) +"!green}{" + value +"}"

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

vault_files = [f for f in os.listdir("../题库0.2") if "题库" in f]
problems = ""
for filename in vault_files:
    with open("../题库0.2/"+filename,"r",encoding="utf8") as vault:
        problems += vault.read()
#读入全部题库数据

ids = [trim(x) for x in re.findall("<BID>([\s\d]*?)<EID>",problems)]
#生成题号列表

data_teachers = ""
data_students = "" 

obj_dict = get_objects_list()

for id in ids:
    regular_expression = str(id).zfill(6)+"\n<EID>[\s\S]*?\[E题目\]"
    problem_pos = re.search(regular_expression,problems)
    if not problem_pos == None:
        problem_set = problems[problem_pos.start():problem_pos.end()]
        problem = trim(re.findall("<B题目>([\s\S]*?)<E题目>",problem_set)[0])
        solution = trim(re.findall("<B解答或提示>([\s\S]*?)<E解答或提示>",problem_set)[0])
        if len(solution) == 0:
            solution = "暂无解答与提示"
        answer = trim(re.findall("<B答案>([\s\S]*?)<E答案>",problem_set)[0])
        if len(answer) == 0:
            answer = "暂无答案"
        usage = trim(re.findall("<B使用记录>([\s\S]*?)<E使用记录>",problem_set)[0]).replace("\n","\n\n")
        if len(usage) > 0:
            usage = re.sub("\\t([\d]\.[\d]{0,10})",color_value,usage)
            usage = re.sub("[\\t ]([\d]\.[\d]{0,10})",color_value,usage)
        else:
            usage = "暂无使用记录"
        origin = trim(re.findall("<B出处>([\s\S]*?)<E出处>",problem_set)[0])
        if len(origin) == 0:
            origin = "出处不详"
        objects = trim(re.findall("<B目标>([\s\S]*?)<E目标>",problem_set)[0])
        if len(objects) == 0:
            objects = "暂未关联目标\n\n"
        elif "KNONE" in objects:
            objects = "该题的考查目标不在目前的集合中\n\n"
        else:
            objects_string = ""
            for obj in [ob for ob in objects.split("\n") if len(ob)>0]:
                try:
                    objects_string += obj + obj_dict[obj] + "\n\n"
                except:
                    print(id,"题, 目标",obj,":目标id有错误.")
            objects = objects_string
        students_string = "\\item ("+id+")"+problem+"\n"
        teachers_string = students_string+"\n\n关联目标:\n\n"+ objects +"答案: "+answer + "\n\n" + "解答或提示: " + solution + "\n\n使用记录:\n\n"+ usage + "\n" + "\n\n出处: "+origin + "\n"
        data_teachers += teachers_string
        data_students += students_string
#生成学生的文件和教师的源文件

try:
    os.remove("题库teachers.pdf")
except:
    a=1
try:
    os.remove("题库students.pdf")
except:
    a=1
#删除已有的文件

with open("problems_file.tex","w",encoding="utf8") as f:
    f.write(data_teachers)
os.system("xelatex to_compile.tex")
os.rename("to_compile.pdf","题库teachers.pdf")
with open("problems_file.tex","w",encoding="utf8") as f:
    f.write(data_students)
os.system("xelatex to_compile.tex")
os.rename("to_compile.pdf","题库students.pdf")
#生成学生的pdf和教师的pdf(含答案)

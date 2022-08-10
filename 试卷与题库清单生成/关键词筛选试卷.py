import os,re,time,shutil

#这里四行每次需要改动
keywords_in_problem = ["集合"]
keywords_in_objects = ["K0101","K0102","K0103","K0104"]

keywords_in_tag = ["第一单元"]
keywords_in_classification = ["选择题","填空题","解答题"]
#keywords_in_classification = ["填空题","选择题","解答题"]

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

id_list = ""

for p in problems_list:
    p_id = trim(re.findall("<BID>([\s\S]*?)<EID>",p)[0])
    p_problem = trim(re.findall("<B题目>([\s\S]*?)<E题目>",p)[0])
    p_tag = trim(re.findall("<B标签>([\s\S]*?)<E标签>",p)[0])
    p_objects = trim(re.findall("<B目标>([\s\S]*?)<E目标>",p)[0])
    p_classification = trim(re.findall("<B类型>([\s\S]*?)<E类型>",p)[0])
    #print([p_id,p_problem,p_tag,p_objects,p_classification])
    if coincide(keywords_in_tag,p_tag) and (p_classification in keywords_in_classification) and (coincide(keywords_in_problem,p_problem) or  coincide(keywords_in_objects,p_objects)):
        id_list += p_id + ","

if len(id_list) > 0:
    id_list = id_list[:-1]

output_string = "关键字筛选结果:\n\n"
output_string += "题目关键词: " + ", ".join(keywords_in_problem) + "\n"
output_string += "标签关键词: " + ", ".join(keywords_in_tag) + "\n"
output_string += "目标关键词: " + ", ".join(keywords_in_objects) + "\n"
output_string += "包含题型: " + ", ".join(keywords_in_classification) + "\n\n"
output_string += "题目数量: " + str((len(id_list)+1)//7) + "\n\n"
output_string += id_list

current_time = str(time.localtime().tm_year)+str(time.localtime().tm_mon).zfill(2)+str(time.localtime().tm_mday).zfill(2)+str(time.localtime().tm_hour).zfill(2)+str(time.localtime().tm_min).zfill(2)+str(time.localtime().tm_sec).zfill(2)
with open(r"选题/题目列表_"+current_time+".txt","w",encoding = "utf8") as f:
    f.write(output_string) 

tex_template = "选题tex/模板.tex"
with open(tex_template,"r", encoding = "utf8") as f:
    template = f.read()
head,tail = re.findall(r"^([\s\S]*?)编译模板([\s\S]*?)$",template)[0]
head += r"\begin{enumerate}[1.]" + "\n\n"
tail = r"\end{enumerate}" + "\n\n" + tail

data_teachers = ""
data_students = "" 

vault_files = [f for f in os.listdir("../题库0.2") if "题库" in f]
problems = ""
for filename in vault_files:
    with open("../题库0.2/"+filename,"r",encoding="utf8") as vault:
        problems += vault.read()

obj_dict = get_objects_list()

for id in id_list.split(","):
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
        tag = trim(re.findall("<B标签>([\s\S]*?)<E标签>",problem_set)[0])
        if len(tag) == 0:
            tag = "暂无标签"
        students_string = "\\item "+"{\\tiny ("+id+")}"+problem+"\n"
        teachers_string = students_string.replace("\\tiny","")+"\n\n关联目标:\n\n"+ objects + "\n\n标签: " + tag + "\n\n答案: "+answer + "\n\n" + "解答或提示: " + solution + "\n\n使用记录:\n\n"+ usage + "\n" + "\n\n出处: "+origin + "\n"
        data_teachers += teachers_string
        data_students += students_string

filedata_teachers = head + data_teachers+tail
filedata_students = head + data_students+tail

tex_filename = current_time+"_compile.tex"
    
with open(tex_filename,"w",encoding = "utf8") as f:
    f.write(filedata_students)
os.system("xelatex " + tex_filename)
os.system("xelatex " + tex_filename)
shutil.copy(tex_filename,"选题tex/选题_学生版_"+current_time+".tex")
shutil.copy(tex_filename[:-4]+".pdf","选题pdf/选题_学生版_"+current_time+".pdf")
with open(tex_filename,"w",encoding = "utf8") as f:
    f.write(filedata_teachers)
os.system("xelatex " + tex_filename)
os.system("xelatex " + tex_filename)
shutil.copy(tex_filename,"选题tex/选题_教师版_"+current_time+".tex")
shutil.copy(tex_filename[:-4]+".pdf","选题pdf/选题_教师版_"+current_time+".pdf")

to_delete = [f for f in os.listdir() if tex_filename[:-4] in f]
for f in to_delete:
    os.remove(f)
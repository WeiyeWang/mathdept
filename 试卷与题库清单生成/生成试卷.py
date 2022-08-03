import os,re

def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def color_value(matchobj):
    value = matchobj.group(1)
    return "\t"+"\\textcolor{red!"+ "%.3f" %(100*float(value)) +"!green}{" + value +"}"
    
vault_files = [f for f in os.listdir("../题库0.2") if "题库" in f]
problems = ""
for filename in vault_files:
    with open("../题库0.2/"+filename,"r",encoding="utf8") as vault:
        problems += vault.read()
#读入全部题库数据

idstr = input("选择题号:")
id_list = idstr.split(",")
ids = []
for term in id_list:
    if not ":" in term:
        ids.append(str(term).zfill(6))
    else:
        [start,end] = term.split(":")
        for k in range(int(start),int(end)+1):
            ids.append(str(k).zfill(6))
#生成题号列表

data_teachers = ""
data_students = ""    

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
        students_string = "\\item ("+id+")"+problem+"\n"
        teachers_string = students_string+"\n\n答案: "+answer + "\n\n" + "解答或提示: " + solution + "\n\n使用记录:\n\n"+ usage + "\n" + "\n\n出处: "+origin + "\n"
        data_teachers += teachers_string
        data_students += students_string
#生成学生的文件和教师的源文件

try:
    os.remove("teachers.pdf")
except:
    a=1
try:
    os.remove("students.pdf")
except:
    a=1
#删除已有的文件

with open("problems_file.tex","w",encoding="utf8") as f:
    f.write(data_teachers)
os.system("xelatex to_compile.tex")
os.rename("to_compile.pdf","teachers.pdf")
with open("problems_file.tex","w",encoding="utf8") as f:
    f.write(data_students)
os.system("xelatex to_compile.tex")
os.rename("to_compile.pdf","students.pdf")
#生成学生的pdf和教师的pdf(含答案)

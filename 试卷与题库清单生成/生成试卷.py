import os,re

def trim(string):
    while string[0] in (" ","\t","\n"):
        string = string[1:]
    while string[-1] in (" ","\t","\n"):
        string = string[:-1]
    return string

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
    regular_expression = str(id).zfill(6)+"[\s\S]*?\[E题目\]"
    problem_pos = re.search(regular_expression,problems)
    if not problem_pos == None:
        problem_set = problems[problem_pos.start():problem_pos.end()]
        problem = trim(re.findall("<B题目>([\s\S]*?)<E题目>",problem_set)[0])
        try:
            answer = trim(re.findall("<B答案>([\s\S]*?)<E答案>",problem_set)[0])
        except:
            answer = "暂无答案"
        students_string = "\\item "+problem+"\n"
        teachers_string = students_string+"\n\n答案: "+answer + "\n"
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

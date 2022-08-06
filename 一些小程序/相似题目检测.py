import os,re,difflib,Levenshtein,time

def generate_number_set(string):
    string = re.sub(r"[\n\s]","",string)
    string_list = string.split(",")
    numbers_list = []
    for s in string_list:
        if not ":" in s:
            numbers_list.append(s.zfill(6))
        else:
            start,end = s.split(":")
            for ind in range(int(start),int(end)+1):
                numbers_list.append(str(ind).zfill(6))
    return numbers_list
def difflab_get_equal_rate(str1, str2):
    str1 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str1)
    str1 = re.sub(r"(displaystyle)|(overrightarrow)","",str1)
    str1 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str1)
    str2 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str2)
    str2 = re.sub(r"(displaystyle)|(overrightarrow)","",str2)
    str2 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str2)
    return difflib.SequenceMatcher(None, str1.replace("\t","").replace(" ","").replace("\n",""), str2.replace("\t","").replace(" ","").replace("\n","")).ratio()
def jaro_get_equal_rate(str1,str2):
    str1 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str1)
    str1 = re.sub(r"(displaystyle)|(overrightarrow)","",str1)
    str1 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str1)
    str2 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str2)
    str2 = re.sub(r"(displaystyle)|(overrightarrow)","",str2)
    str2 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str2)
    return Levenshtein.jaro(str1.replace("\t","").replace(" ","").replace("\n",""), str2.replace("\t","").replace(" ","").replace("\n",""))
def Lev_get_equal_rate(str1,str2):
    str1 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str1)
    str1 = re.sub(r"(displaystyle)|(overrightarrow)","",str1)
    str1 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str1)
    str2 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str2)
    str2 = re.sub(r"(displaystyle)|(overrightarrow)","",str2)
    str2 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str2)
    return Levenshtein.ratio(str1.replace("\t","").replace(" ","").replace("\n",""), str2.replace("\t","").replace(" ","").replace("\n",""))
def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def trim_tuple(tuple):
    return (trim(tuple[0]),trim(tuple[1]),trim(tuple[2]),trim(tuple[3]))

def trimpic(string):
    string1 = re.sub(r"\\begin\{center[\s\S]*?\\end\{center\}","",string)
    string1 = re.sub(r"\\begin\{tikz[\s\S]*?\\end\{tikzpicture\}","",string1)
    return string1

vault_files = [f for f in os.listdir("../题库0.2") if "题库" in f]
problems = ""
for filename in vault_files:
    with open("../题库0.2/"+filename,"r",encoding="utf8") as vault:
        problems += vault.read()
#读入全部题库数据

# 重要!!! 新题目的范围
id_new_problems = "10017:10922"
sim_test = jaro_get_equal_rate
threshold = 0.85

problems_formatted = [x for x in re.findall(r"\[B题目\]([\s\S]*?)\[E题目\]",problems)]

problem_list = []
for p in problems_formatted:
    problem_list.append(trim_tuple(re.findall(r"<BID>([\s\S]*?)<EID>[\s\S]*?<B题目>([\s\S]*?)<E题目>[\s\S]*?<B相同题目>([\s\S]*?)<E相同题目>[\s\S]*?<B关联题目>([\s\S]*?)<E关联题目>",p)[0]))


new_id_list = generate_number_set(id_new_problems)
#生成题号列表
new_problems = []
old_problems = []
for p in problem_list:
    if p[0] in new_id_list:
        new_problems.append(p)
    else:
        old_problems.append(p)

print("旧题目数:",len(old_problems),", 新题目数:",len(new_problems))

start_time = time.time()
count = 0
remarked = 0

alike_problems = ""
for i in range(len(new_problems)):
    if i // 50 == i / 50:
        print(i)
    for j in range(len(old_problems)):
        similar_rate = sim_test(new_problems[i][1],old_problems[j][1])
        similar_case = ""
        if old_problems[j][0] in new_problems[i][2] or new_problems[i][0] in old_problems[j][2]:
            similar_case = " 相同"
        elif  old_problems[j][0] in new_problems[i][3] or new_problems[i][0] in old_problems[j][3]:
            similar_case = " 关联"
        if similar_rate>threshold or similar_case != "":
            count += 1
            remarked += 1 if similar_case != "" else 0
            alike_problems += (("%.4f" %similar_rate)+similar_case+"\n\n"+new_problems[i][0]+"\t"+new_problems[i][1]+"\n\n"+old_problems[j][0]+"\t"+old_problems[j][1]+"\n\n")

for i in range(len(new_problems)):
    if i // 50 == i / 50:
        print(i)
    for j in range(i+1,len(new_problems)):
        similar_rate = sim_test(new_problems[i][1],new_problems[j][1])
        similar_case = ""
        if new_problems[j][0] in new_problems[i][2] or new_problems[i][0] in new_problems[j][2]:
            similar_case = " 相同"
        elif  new_problems[j][0] in new_problems[i][3] or new_problems[i][0] in new_problems[j][3]:
            similar_case = " 关联"
        if similar_rate>threshold or similar_case != "":
            count += 1
            remarked += 1 if similar_case != "" else 0
            alike_problems += (("%.4f" %similar_rate)+similar_case+"\n\n"+new_problems[i][0]+"\t"+new_problems[i][1]+"\n\n"+new_problems[j][0]+"\t"+new_problems[j][1]+"\n\n")

end_time = time.time()

print("总耗时:",end_time-start_time,"秒.")
print("发现相似: ",count,", 其中已标注: ",remarked,".")

with open("../题库0.2/相似题目.txt","w",encoding="utf8") as f:
    f.write(alike_problems)
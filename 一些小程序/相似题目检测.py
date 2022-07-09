import os,re,difflib

def get_equal_rate_1(str1, str2):
    str1 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str1)
    str2 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str2)
    return difflib.SequenceMatcher(None, str1.replace("\t","").replace(" ","").replace("\n",""), str2.replace("\t","").replace(" ","").replace("\n","")).ratio()
def trim(string):
    while string[0] in (" ","\t","\n"):
        string = string[1:]
    while string[-1] in (" ","\t","\n"):
        string = string[:-1]
    return string
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

# 重要!!!最初的新题的id
starting_ID = 4572

problem_list = [[x[0],trimpic(trim(x[1]))] for x in re.findall("<BID>\\n([\s\S]*?)\\n<EID>[\s\S]*?<B题目>([\s\S]*?)<E题目>",problems)]
#生成题号列表
old_problems = [f for f in problem_list if f[0] < str(starting_ID).zfill(6)]
new_problems = [f for f in problem_list if f[0] >= str(starting_ID).zfill(6)]
print("旧题目数:",len(old_problems),",新题目数:",len(new_problems))

alike_problems = ""
for i in range(len(new_problems)):
    if i // 50 == i / 50:
        print(i)
    for j in range(len(old_problems)):
        similar_rate = get_equal_rate_1(new_problems[i][1],old_problems[j][1])
        if similar_rate>0.92:
            alike_problems += (("%.4f" %similar_rate)+"\n"+new_problems[i][0]+"\t"+new_problems[i][1]+"\n"+old_problems[j][0]+"\t"+old_problems[j][1]+"\n\n")

for i in range(len(new_problems)):
    if i // 50 == i / 50:
        print(i)
    for j in range(i+1,len(new_problems)):
        similar_rate = get_equal_rate_1(new_problems[i][1],new_problems[j][1])
        #print(similar_rate)
        if similar_rate>0.92:
            alike_problems += (("%.4f" %similar_rate)+"\n"+new_problems[i][0]+"\t"+new_problems[i][1]+"\n"+new_problems[j][0]+"\t"+new_problems[j][1]+"\n\n")



with open("../题库0.2/相似题目.txt","w",encoding="utf8") as f:
    f.write(alike_problems)
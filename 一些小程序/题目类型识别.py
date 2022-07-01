import re,os
def trim(string):
    while len(string)>0 and string[0] in [" ","\n","\t"]:
        string = string[1:]
    while len(string)>0 and string[-1] in [" ","\n","\t"]:
        string = string[:-1]
    return(string)
def cata(string):
    if "\\blank" in string:
        return "填空题"
    elif "\\bracket" in string:
        return "选择题"
    else:
        return "解答题"
def crop_text(string,substr1,substr2):
    start_pos = string.index(substr1)
    end_pos = string.index(substr2)+len(substr2)
    return string[start_pos:end_pos]
os.chdir(r"..\题库0.2")
vaults = [f for f in os.listdir() if "题库" in f]
for i in range(len(vaults)):
    file = vaults[i]
    with open(r"../题库0.2/"+file,"r",encoding="utf8") as vault:
        data = vault.read()
    problems = re.findall("\[B题目\]([\s\S]*?)\[E题目\]",data)
    problem_count = len(problems)
    catagories = []
    for p in problems:
        catagory = re.findall("<B类型>([\s\S]*?)<E类型>",p)[0]
        catagories.append(trim(catagory))
    catagoried_count = 0
    for c in catagories:
        if len(c)>0:
            catagoried_count += 1
    print(i,":",file,". ",catagoried_count,"/",problem_count,"题已分类.")
choice = input("选择需要赋予类型的文件(0-"+str(len(vaults)-1)+":")
file = vaults[int(choice)]
with open(r"../题库0.2/"+file,"r",encoding="utf8") as vault:
    data = vault.read()
problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",data)
problems_modified = ""
for p in problems:
    catagory = trim(re.findall("<B类型>([\s\S]*?)<E类型>",p)[0])
    if len(catagory) == 0:
        catagory = cata(p)
    head = crop_text(p,"[B题目]","<B类型>\n")
    tail = crop_text(p,"<E类型>","[E题目]")
    problems_modified += (head+catagory+"\n"+tail+"\n\n")
with open(r"../题库0.2/"+file,"w",encoding="utf8") as vault:
    vault.write(problems_modified)
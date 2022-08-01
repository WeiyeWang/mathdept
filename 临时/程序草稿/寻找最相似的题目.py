import os,re,Levenshtein

to_test = r"""已知$z=3+4\mathrm{i}$, 求$|z|$"""

def jaro_get_equal_rate(str1,str2):
    str1 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str1)
    str1 = re.sub(r"(displaystyle)|(overrightarrow)","",str1)
    str1 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str1)
    str2 = re.sub(r"[\s\\\{\}\$\(\)\[\]]","",str2)
    str2 = re.sub(r"(displaystyle)|(overrightarrow)","",str2)
    str2 = re.sub(r"\\begin\{center\}[\s\S]*?\\end\{center\}","",str2)
    return Levenshtein.jaro(str1,str2)

def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def trim_tuple(tuple):
    return (trim(tuple[0]),trim(tuple[1]),trim(tuple[2]))

os.chdir("d:/mathdept/一些小程序")

vault_files = [f for f in os.listdir("../题库0.2") if "题库" in f]
problems = ""
for filename in vault_files:
    with open("../题库0.2/"+filename,"r",encoding="utf8") as vault:
        problems += vault.read()
problems_formatted = [x for x in re.findall(r"\[B题目\]([\s\S]*?)\[E题目\]",problems)]

problem_list = []
for p in problems_formatted:
    problem_list.append(trim_tuple(re.findall(r"<BID>([\s\S]*?)<EID>[\s\S]*?<B题目>([\s\S]*?)<E题目>[\s\S]*?<B类型>([\s\S]*?)<E类型>",p)[0]))



similarity = []

output_string = ""
for p in problem_list:
    ID = p[0]
    problem = p[1]
    similarity.append(jaro_get_equal_rate(to_test,p[1]))
similarity.sort()
similarity_threshold = similarity[-10]
for p in problem_list:
    ID = p[0]
    problem = p[1]
    jaro = jaro_get_equal_rate(to_test,p[1])
    if jaro>=similarity_threshold:
        output_string += r"\item ("+ID+r")"+"[sim:"+("%.3f" %jaro)+"]"+problem+"\n"    
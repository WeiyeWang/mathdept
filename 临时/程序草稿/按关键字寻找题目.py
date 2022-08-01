import os,re
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

output_string = ""
for p in problem_list:
    ID = p[0]
    problem = p[1]
    if r"\mathrm{C}" in problem or r"\mathrm{P}" in problem:
        output_string += r"\item ("+ID+r")"+problem+"\n"
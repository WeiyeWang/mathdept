import os,re
def trim(string):
    string = re.sub(r"^[\s]*","",string)
    string = re.sub(r"[\s]*$","",string)
    return string
def crop_text(string,substr1,substr2):
    start_pos = string.index(substr1)
    end_pos = string.index(substr2)+len(substr2)
    return string[start_pos:end_pos]
#文件名须修改
with open(r"题库0.1\上海2020教材习题选择性必修第二册.tex","r",encoding = "utf8") as f:
    data = f.read()
with open(r"题库0.2\模板.txt","r",encoding = "utf8") as f1:
    template = f1.read()
data = re.findall(r"\\begin\{document\}([\s\S]*?)\\end\{document\}",data)[0]
data = re.sub(r"\n[\s]*?\%[\s\S]*?\n","\n",data)
data = re.sub(r"\n{2,}","\n",data)
data = re.sub(r"\\item",r"\\enditem\\item",data)
data = re.sub(r"\\end\{enumerate\}",r"\\enditem",data)
problems_raw = [trim(p) for p in re.findall(r"\\item([\s\S]*?)\\enditem",data)]
problems = []
answers = []
for p_raw in problems_raw:
    split_p = re.findall(r"(^[\s\S]*?)[\\]*\s*解答在这里([\s\S]*?$)",p_raw)
    if len(split_p) == 0:
        problems.append(p_raw)
        answers.append("")
    else:
        problems.append(trim(split_p[0][0]))
        answers.append(trim(split_p[0][1]))
#以上已经生成了题目列表，以下出处、使用记录、修订历史等须设定
origin = "新教材选择性必修第二册习题"
usage = ""
editor = "20220806\t王伟叶"
# 重要！！！初始ID
starting_ID = 10789

head_str = crop_text(template,"[B题目]","<BID>\n")
body_str_1 = crop_text(template,"\n<EID>","<B题目>\n")
body_str_2 = crop_text(template,"\n<E题目>","<B解答或提示>\n")
body_str_3 = crop_text(template,"\n<E解答或提示>","<B使用记录>\n")
body_str_4 = crop_text(template,"\n<E使用记录>","<B出处>\n")
body_str_5 = crop_text(template,"\n<E出处>","<B修订历史>\n")
body_str_6 = crop_text(template,"\n<E修订历史>","[E题目]")+"\n\n"

problems_str = ""
id = starting_ID

for i in range(len(problems)):
    p = problems[i]
    a = answers[i]
    problems_str += (head_str + str(id).zfill(6) + body_str_1 + p + body_str_2 + a +  body_str_3 + usage + body_str_4 + origin + body_str_5 + editor + body_str_6)
    id += 1

with open(r"题库0.2/("+str(starting_ID).zfill(6)+"to"+str(starting_ID-1+len(problems)).zfill(6)+")"+origin+r"题库.txt","w",encoding = "utf8") as f2:
    f2.write(problems_str)
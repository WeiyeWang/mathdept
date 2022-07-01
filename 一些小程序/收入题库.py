import os,re
def trim(string):
    while string[0] in [" ","\n","\t"]:
        string = string[1:]
    while string[-1] in [" ","\n","\t"]:
        string = string[:-1]
    return(string)
def crop_text(string,substr1,substr2):
    start_pos = string.index(substr1)
    end_pos = string.index(substr2)+len(substr2)
    return string[start_pos:end_pos]
#文件名须修改
with open(r"..\题库0.1\2022届第一轮讲义例题与习题.tex","r",encoding = "utf8") as f:
    data = f.read()
with open(r"..\题库0.2\模板.txt","r",encoding = "utf8") as f1:
    template = f1.read()
data = re.findall(r"\\begin\{document\}([\s\S]*?)\\end\{document\}",data)[0]
data = re.sub(r"\n[\s]*?\%[\s\S]*?\n","\n",data)
data = re.sub(r"\n{2,}","\n",data)
data = re.sub(r"\\item",r"\\enditem\\item",data)
data = re.sub(r"\\end\{enumerate\}",r"\\enditem",data)
problems = [trim(p) for p in re.findall(r"\\item([\s\S]*?)\\enditem",data)]
#以上已经生成了题目列表，以下出处、使用记录、修订历史等须设定
origin = "2022届高三第一轮复习讲义"
usage = ""
editor = "20220701\t王伟叶"
# 重要！！！初始ID
starting_ID = 2692

head_str = crop_text(template,"[B题目]","<BID>\n")
body_str_1 = crop_text(template,"\n<EID>","<B题目>\n")
body_str_2 = crop_text(template,"\n<E题目>","<B使用记录>\n")
body_str_3 = crop_text(template,"\n<E使用记录>","<B出处>\n")
body_str_4 = crop_text(template,"\n<E出处>","<B修订历史>\n")
body_str_5 = crop_text(template,"\n<E修订历史>","[E题目]")+"\n\n"

problems_str = ""
id = starting_ID
for p in problems:
    problems_str += (head_str + str(id).zfill(6) + body_str_1 + p + body_str_2 + usage + body_str_3 + origin + body_str_4 + editor + body_str_5)
    id += 1
with open(r"..\题库0.2\valut_output.txt","w",encoding = "utf8") as f2:
    f2.write(problems_str)
import os,re
import pandas as pd
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
with open(r"题库0.1\2022届高三四次统考试卷.tex","r",encoding = "utf8") as f:
    data = f.read()
with open(r"题库0.2\模板.txt","r",encoding = "utf8") as f1:
    template = f1.read()
data = re.findall(r"\\begin\{document\}([\s\S]*?)\\end\{document\}",data)[0]
data = re.sub(r"\n[\s]*?\%[\s\S]*?\n","\n",data)
data = re.sub(r"\n{2,}","\n",data)
data = re.sub(r"\\item",r"\\enditem\\item",data)
data = re.sub(r"\\end\{enumerate\}",r"\\enditem",data)
problems = [trim(p) for p in re.findall(r"\\item([\s\S]*?)\\enditem",data)]
#以上已经生成了题目列表，以下出处、使用记录、修订历史等须设定
origin = ""
editor = "20220711\t王伟叶"
# 重要！！！初始ID
starting_ID = 4661

head_str = crop_text(template,"[B题目]","<BID>\n")
body_str_1 = crop_text(template,"\n<EID>","<B题目>\n")
body_str_2 = crop_text(template,"\n<E题目>","<B使用记录>\n")
body_str_3 = crop_text(template,"\n<E使用记录>","<B出处>\n")
body_str_4 = crop_text(template,"\n<E出处>","<B修订历史>\n")
body_str_5 = crop_text(template,"\n<E修订历史>","[E题目]")+"\n\n"

#生成对应的得分率
originlist = ["2022届高三上期中区统考","2022届高三上一模","2022届高三下期中区统考","2022届高三下二模"]
dates = ["20210924","20211209"]
usage = []
for i in range(2):
    current_usage = dates[i] + "\t" + "2022届高三"
    df = pd.read_excel("g:/Temp/0712/exam"+str(i)+".xlsx",sheet_name = "统计")
    cols = df.columns[2:]
    current_problem = 1
    col_index = 0
    while col_index < len(cols):
        col = cols[col_index]
        problem_index = str(current_problem)
        if str(col)[:len(problem_index)] == problem_index:
            current_usage += "\t" + ("%.3f" %df[col][14])
            col_index += 1
        else:
            current_problem += 1
            usage.append(current_usage)
            current_usage = dates[i] + "\t" + "2022届高三"
    usage.append(current_usage)

problems_str = ""
id = starting_ID
count = 0
for p in problems:
    origin = originlist[count//21] + "第" + str((count % 21)+1) + "题"
    problems_str += (head_str + str(id).zfill(6) + body_str_1 + p + body_str_2 + usage[count] + body_str_3 + origin + body_str_4 + editor + body_str_5)
    id += 1
    count += 1
with open(r"题库0.2\vault_output.txt","w",encoding = "utf8") as f2:
    f2.write(problems_str)
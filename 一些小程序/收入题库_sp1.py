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
with open(r"..\题库0.1\2022届高三下学期测验卷.tex","r",encoding = "utf8") as f:
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
origin_raw = "2022届高三下学期测验卷"
usage = ""
editor = "20220705\t王伟叶"
# 重要！！！初始ID
starting_ID = 4059

head_str = crop_text(template,"[B题目]","<BID>\n")
body_str_1 = crop_text(template,"\n<EID>","<B题目>\n")
body_str_2 = crop_text(template,"\n<E题目>","<B使用记录>\n")
body_str_3 = crop_text(template,"\n<E使用记录>","<B出处>\n")
body_str_4 = crop_text(template,"\n<E出处>","<B修订历史>\n")
body_str_5 = crop_text(template,"\n<E修订历史>","[E题目]")+"\n\n"

problems_str = ""
id = starting_ID

results_raw = ""
statsfile = [f for f in os.listdir(r"C:\Users\Wang Weiye\Documents\wwy sync\22届\高三数学教学\考试测验练习相关\统计数据") if "quiz" in f and "20220101" < f[:8] and "xlsx" in f]
for f in statsfile:
    df=pd.read_excel(r"C:\Users\Wang Weiye\Documents\wwy sync\22届\高三数学教学\考试测验练习相关\统计数据"+"\\"+f)
    for col in df.columns[3:]:
        results_raw += (f[f.index("quiz")+4:(-5)]+","+str(col)+","+"%.3f" %df[col][46] + "\n")
results_raw_list = [r for r in results_raw.split("\n") if len(r)>0]
results_list = []
for r in results_raw_list:
    record = r.split(",")
    if len(record[1])<3:
        results_list.append(r)
        last_problem = "0"
    elif last_problem != record[1][:2]:
        last_problem = record[1][:2]
        new_record = record[0]+","+record[1][:2]+","+record[2]
        results_list.append(new_record)
    else:
        results_list[-1] += "\t"+record[2]
records = [r.split(",") for r in results_list if len(r)>0]

for i in range(14):
    for j in range(21):
        p = problems[i*21+j]
        origin = origin_raw + str(i+1).zfill(2) + "第" + str(j+1) + "题"
        usage = ""
        for r in records:
            if r[0] == str(i+1) and r[1] == str(j+1):
                usage = "2022届高三1班\t" + r[2]
        problems_str += (head_str + str(id).zfill(6) + body_str_1 + p + body_str_2 + usage + body_str_3 + origin + body_str_4 + editor + body_str_5)
        id += 1
with open(r"..\题库0.2\vault_output.txt","w",encoding = "utf8") as f2:
    f2.write(problems_str)
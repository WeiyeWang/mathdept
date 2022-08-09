import os,re
def trim(string):
    string = re.sub(r"^[\s\n ]*?","",string)
    return re.sub(r"[\s\n ]*?$","",string)
vault_list = [f for f in os.listdir("../题库0.2") if "题库" in f or "vault" in f]
problems_list = []
for v in vault_list:
    with open("../题库0.2/"+v,"r",encoding = "utf8") as f:
        data = f.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",data)
        for problem in problems:
            problems_list.append(problem)
with open("../题库0.2/标签对应.txt","r",encoding = "utf8") as f:
    raw_id_str = f.read()
    raw_id_str = raw_id_str.replace("：",":").replace("，",",")

raw_id_list = [line for line in raw_id_str.split("\n") if len(line)>0]
id_tag_dict = []
for i in range(len(raw_id_list)//2):
    id_tag_dict.append((raw_id_list[2*i],raw_id_list[2*i+1]))

for item in id_tag_dict:
    idstr = item[0]
    tag = trim(item[1])
    id_list = idstr.split(",")
    ids = []
    for term in id_list:
        if not ":" in term:
            ids.append(str(term).zfill(6))
        else:
            [start,end] = term.split(":")
            for k in range(int(start),int(end)+1):
                ids.append(str(k).zfill(6))
    for id in ids:
        for v in vault_list:
            if v[1:7] <= id <= v[9:15]:
                with open("../题库0.2/"+v,"r",encoding="utf8") as f:
                    raw_data = f.read()
                problem = re.findall(r"(\[B题目\][\s\n]*?<BID>[\s\n]*?"+id+r"[\s\n]*?<EID>[\s\S]*?\[E题目\])",raw_data)[0]
                current_tag = trim(re.findall(r"<B标签>([\s\S]*?)<E标签>",problem)[0])
                if tag in current_tag:
                    new_tag = current_tag
                elif len(current_tag) > 0:
                    new_tag = current_tag + "|" + tag
                else:
                    new_tag = tag
                modified_problem = re.sub(r"<B标签>([\s\S]*?)<E标签>","<B标签>\n"+new_tag+"\n<E标签>",problem)
                modified_data = raw_data.replace(problem,modified_problem)
                with open("../题库0.2/"+v,"w",encoding="utf8") as f:
                    f.write(modified_data)
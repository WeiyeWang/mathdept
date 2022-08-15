import os,re
import vaulttools as vt

def form_decimals(string):
    numerals_list = [n for n in string.split("\t") if len(n)>0]
    for i in range(len(numerals_list)):
        numeral = numerals_list[i]
        str_numeral = "%.3f" %float(numeral)
        numerals_list[i] = str_numeral
    return "\t".join(numerals_list)
#os.chdir("d:/mathdept")
vaults = [f for f in os.listdir("题库0.2") if "题库" in f]

with open("一些小程序/统计结果.txt","r",encoding = "utf8") as results_file:
    results_data = results_file.read()


results_each_class_list = re.findall("\[BEGIN\]([\s\S]*?)\[END\]",results_data)#寻找所有结果记录

records = []
for results_each_class in results_each_class_list:
    temp_list = results_each_class.split("\n")
    result_line_list = []
    for line in temp_list:
        if line[:2] == "##":
            date = vt.trim(line[2:])
        elif line[:2] == "**":
            current_class = vt.trim(line[2:])
        else:
            if len(line)>0:
                separating_pos = re.search("\s",line).span(0)[0]
                result_line_list.append(vt.trim(line[:separating_pos])+":"+form_decimals(vt.trim(re.sub("\s+?","\t",line[separating_pos:]))))
    for r in result_line_list:
        records.append(r.split(":")[0].zfill(6) + ";" + date + "\t" + current_class + "\t" + r.split(":")[1])
#根据结果记录生成records记录每一条结果，格式为题目ID;日期\t班级\t正确率
for r in records:
    [id,content] = r.split(";")
    date = content.split("\t")[0]
    current_class = content.split("\t")[1]
    for v in vaults:
        (startid,endid)=re.findall("(\d{6})to(\d{6})",v)[0]
        if startid <= id <= endid:
            with open("题库0.2/"+v,"r",encoding = "utf8") as vault:
                vault_data = vault.read()
            problem_raw = re.findall("(\[B题目\]\s*?<BID>\s*?"+id+"[\s\S]*?E题目\])",vault_data)[0]
            usage_raw = re.findall("<B使用记录>([\s\S]*?)<E使用记录>",problem_raw)[0]
            old_usages = usage_raw.split("\n")
            record_in_vault = False
            for u in old_usages:
                if date in u and current_class in u:
                    record_in_vault = True
            if not record_in_vault:
                usage_new = usage_raw + content + "\n"
                #print(usage_new)
                if not usage_raw == "\n\n":
                    problem_new = problem_raw.replace("<B使用记录>"+usage_raw+"<E使用记录>","<B使用记录>"+usage_new+"<E使用记录>")
                else:
                    problem_new = problem_raw.replace("<B使用记录>"+usage_raw+"<E使用记录>","<B使用记录>"+usage_new[1:]+"<E使用记录>")
                #print(vault_data.index(problem_raw),problem_raw == problem_new)
                vault_data = vault_data.replace(problem_raw,problem_new)
            with open("题库0.2/"+v,"w",encoding = "utf8") as vault:
                vault.write(vault_data)
#每条记录改写一下题库中的结果
import re

def trim(string):
    string = re.sub(r"^[ \t\n]*","",string)
    string = re.sub(r"[ \t\n]*$","",string)
    return string
def recognize_line(string):
    string = re.sub(r"[\s\n\t]+",",",trim(string))
    record = string.split(",")
    return record

def get_spaces(data):#每道题以\item开头, 空间用\vspace给出
    list = [i for i in data.split("item") if "vspace" in i]
    output = []
    for line in list:
        id = re.findall(r"\((\d{6})\)",line)[0]
        space = re.findall(r"vspace\*{0,1}\{([\S]*?)\}",line)[0]
        output.append((id,space))

def give_spaces(resp):
    lines = [recognize_line(line) for line in resp.split("\n") if len(line) > 0]
    vaults = [f for f in os.listdir("../题库0.2") if "题库" in f]
    for line in lines:
        id = line.pop(0)
        id = id.zfill(6)
        for v in vaults:
            (startid,endid)=re.findall("(\d{6})to(\d{6})",v)[0]
            if startid <= id <= endid:
                with open("../题库0.2/"+v,"r",encoding = "utf8") as vault:
                    vault_data = vault.read()
                problem_raw = re.findall("(\[B题目\]\s*?<BID>\s*?"+id+"[\s\S]*?E题目\])",vault_data)[0]
                problem_new = re.sub("<B解答空间>[\s\S]*?<E解答空间>","<B解答空间>\n"+line[0]+"\n<E解答空间>",problem_raw)
                vault_data = vault_data.replace(problem_raw,problem_new)
                with open("../题库0.2/"+v,"w",encoding = "utf8") as new_vault:
                    new_vault.write(vault_data)

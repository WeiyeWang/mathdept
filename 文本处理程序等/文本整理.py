import os,re
#os.chdir(r"D:\mathdept\文本处理程序等")
with open("textfile.txt", "r", encoding = "utf8") as textfile:
    data = textfile.read()

def full_stop(matchobj):
    if matchobj.group(1) == "。":
        return ". "
    elif matchobj.group(1) == "。\\n":
        return ".\\n"
    else:
        return ".\\n"

def refine_brackets(matchobj):
    return matchobj.group(1)[1:-1]

def boldsymbols(matchobj):
    return "\\i"+matchobj.group(1)[:-1]+"\\mathbf{"+matchobj.group(1)[-1]+"}"

def insert_a_blank(matchobj):
    return matchobj.group(1)[:-1]+" "+matchobj.group(1)[-1]

data = re.sub("([\d]+. )",r"\\item ",data)
data = re.sub("\\\\\[",r"$",data)
data = re.sub("\\\\\]",r"$",data)
data = data.replace("\\frac","\\dfrac")

data = re.sub("(。[\n]*)",full_stop,data)
data = re.sub("，[\n]*",", ",data)
data = re.sub("：[\n]*",": ",data)
data = re.sub("；[\n]*","; ",data)
data = re.sub("（[\n]*","(",data)
data = re.sub("）[\n]*",")",data)
data = re.sub("“[\n]*","``",data)
data = re.sub("”[\n]*","''",data)

data = re.sub("   [ ]+",r"\\blank{50}",data)
data = re.sub("__[_]+",r"\\blank{50}",data)


for i in range(10):
    data = re.sub("(\{\\\\[\w]+[ ]*\}|\{\}|\{\w\})",refine_brackets,data)

data = re.sub("(\\\\overrightarrow[\w])",insert_a_blank,data)

data = data.replace("\\bigc","\\c")
data = re.sub("\\\i(n[ ]+[R|Q|Z|N|C])",boldsymbols,data)

with open("outputfile.txt","w",encoding = "utf8") as f:
    f.write(data)
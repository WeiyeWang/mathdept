import os,re
try:
    os.chdir(r"D:\mathdept\mathdept\文本处理程序等")
except:
    os.chdir(r"D:\mathdept\文本处理程序等")
with open("textfile.txt", "r", encoding = "utf8") as textfile:
    data = textfile.read()

def full_stop(matchobj):
    if matchobj.group(1) == "。" or matchobj.group(1) == "．":
        return ". "
    else:
        return ".\n"

def refine_brackets(matchobj):
    return matchobj.group(1)[1:-1]

def boldsymbols(matchobj):
    return "\\i"+matchobj.group(1)[:-1]+"\\mathbf{"+matchobj.group(1)[-1]+"}"

def insert_a_blank(matchobj):
    return matchobj.group(1)[:-1]+" "+matchobj.group(1)[-1]

def limit(matchobj):
    return "\\displaystyle\\lim_{"+matchobj.group(1)+"\\to\\infty}"

def outer_brackets(matchobj):
    return "$"+ matchobj.group(1) + "$"

def replace_i(matchobj):
    string = matchobj.group(1)
    length = len(string)
    for i in range(length-1,-1,-1):
        if string[i] == "i" and not "item" in string[i:]:
            string = string[:i] + "\\mathrm{i}" + string[i+1:]
    return string

data = re.sub(r"([\d]\\)",insert_a_blank,data)

data = data.replace(r"\left","").replace(r"\right.","").replace(r"\right","")

data = re.sub("　","  ",data)
data = re.sub("(。[\n]*)",full_stop,data)
data = re.sub("(．[\n]*)",full_stop,data)
data = re.sub("，[\n]*",", ",data)
data = re.sub("：[\n]*",": ",data)
data = re.sub("；[\n]*","; ",data)
data = re.sub("（[\n]*","(",data)
data = re.sub("）[\n]*",")",data)
data = re.sub("“[\n]*","``",data)
data = re.sub("”[\n]*","''",data)

data = re.sub("([0-9]+\.[\s]+)",r"\\item ",data)
data = re.sub("\\\\\[",r"$",data)
data = re.sub("\\\\\]",r"$",data)
data = data.replace("\\frac","\\dfrac")

data = re.sub("[ _]{3,}",r"\\blank{50}",data)

data = re.sub("\\\\[!,]","",data)
data = re.sub("\{ *?\}","",data)
data = re.sub("\( *?","(",data)
data = re.sub(" *?\)",")",data)
data = re.sub("\$ *?","$",data)
data = re.sub(" *?\$","$",data)

data = re.sub("\\\\text","",data)

for i in range(10):
    data = re.sub("(\{[\w+\-]\})",refine_brackets,data)
for i in range(10):
    data = re.sub("(\{\{.*?\}\})",refine_brackets,data)

data = re.sub("(\\\\overrightarrow[\w])",insert_a_blank,data)

data = data.replace("\\bigc","\\c")
data = re.sub("\\\i(n[ ]+[R|Q|Z|N|C])",boldsymbols,data)

data = re.sub(r"\\underset{([\w])\\to \\infty }{\\mathop\\lim }\\,",limit,data) 
data = re.sub(r"\\underset{([\w])\\to \\infty }{\\mathop{lim}}\\,",limit,data) 
data = re.sub(r"\\underset{([\w])\\to \\infty }{\\mathop{\\lim }}\\,",limit,data)
data = re.sub(r"\\underset{([\w])\\to \\infty }{\\mathop{\\lim }}",limit,data)
data = re.sub("\$\{([^\{\}]{0,10})\}\$",outer_brackets,data)

data = re.sub("(\\n.*?复数.*?\\n)",replace_i,data)
data = re.sub("\{\([\w]\)\^\{\-1\}\}"


with open("outputfile.txt","w",encoding = "utf8") as f:
    f.write(data)
import os,re

def full_stop(matchobj):
    if matchobj.group(1) == "。" or matchobj.group(1) == "．":
        return ". "
    else:
        return ".\n"
def refine_brackets(matchobj):
    return matchobj.group(1)[1:-1]
def insert_a_blank(matchobj):
    return matchobj.group(1)[:-1]+" "+matchobj.group(1)[-1]
def multiple_choice(matchobj):
    string = "\\fourch" + "{" + matchobj.group(1) + "}{" + matchobj.group(2) + "}{" + matchobj.group(3) + "}{" + matchobj.group(4) + "}"
    return string
def boldsymbols(matchobj):
    return "\\i"+matchobj.group(1)[:-1]+"\\mathbf{"+matchobj.group(1)[-1]+"}"
def singleboldsymbols(matchobj):
    return "$\\mathbf{" + matchobj.group(1) + "}$"
def blackboardbold(matchobj):
    string = "\\mathbf" + "{" + matchobj.group(1) + "}"
    return string
def limit(matchobj):
    return "\\displaystyle\\lim_{"+matchobj.group(1)+"}"
def replace_i(matchobj):
    string = matchobj.group(1)
    length = len(string)
    for i in range(length-1,-1,-1):
        if string[i] == "i" and not "item" in string[i:]:
            string = string[:i] + "\\mathrm{i}" + string[i+1:]
    return string
    
try:
    os.chdir(r"D:\mathdept\mathdept\文本处理程序等")
except:
    os.chdir(r"D:\mathdept\文本处理程序等")
with open("textfile.txt", "r", encoding = "utf8") as textfile:
    data = textfile.read()



#去除左右括号的前缀
data = data.replace(r"\left","").replace(r"\right.","").replace(r"\right","")

#全角半角符号替换
data = re.sub("　","  ",data)
data = re.sub("(。[\n]*)",full_stop,data)
data = re.sub("(．[\n]*)",full_stop,data)
data = re.sub("，",", ",data)
data = re.sub("：",": ",data)
data = re.sub("；","; ",data)
data = re.sub("（","(",data)
data = re.sub("）",")",data)
data = re.sub("？","? ",data)
data = re.sub("“","``",data)
data = re.sub("”","''",data)

#替换全角数字等
data = re.sub("α",r"\\alpha",data)
data = re.sub("β",r"\\beta",data)
data = re.sub("｛","\{",data)
data = re.sub("｝","\}",data)
data = re.sub("∪",r"\\cup ",data)
data = re.sub("∩",r"\\cap ",data)
data = re.sub("∞",r"\\infty",data)
data = re.sub("γ",r"\\gamma",data)
data = re.sub("δ",r"\\delta",data)
data = re.sub("≤",r"\\le ",data)
data = re.sub("≥",r"\\ge ",data)
data = re.sub("槡",r"\\sqrt ",data)
data = re.sub("ｌｏｇ",r"\\log ",data)
data = re.sub("ｌｇ",r"\\lg ",data)
data = re.sub("≠",r"\\ne ",data)
data = re.sub("π",r"\\pi ",data)
data = re.sub("θ",r"\\theta ",data)
data = re.sub("ｓｉｎ",r"\\sin ",data)
data = re.sub("ｃｏｓ",r"\\cos ",data)
data = re.sub("ｔａｎ",r"\\tan ",data)
data = re.sub("ｃｏｔ",r"\\cot ",data)
data = re.sub("△",r"\\triangle ",data)
data = re.sub("φ",r"\\varphi ",data)
data = re.sub("ω",r"\\omega ",data)
data = re.sub("珗",r"\\overrightarrow ",data)
data = re.sub("珤犲",r"\\overrightarrow e_ ",data)
data = re.sub("λ",r"\\lambda e_ ",data)
data = re.sub("ｉ",r"\\mathrm{i}",data)
data = re.sub("∈",r"\\in ",data)
data = re.sub("⊥",r"\\perp ",data)
data = re.sub("∥",r"\\parallel ",data)


whole_numbers = "０１２３４５６７８９＋－＝狆狇狉犕犖＞＜犃犅犆犇狓犝［］｜犪狔犙犽犘犚犫犛犮犈犗犿犣狀犳犵犺狋犻犼狕犉犾′"
correct_numbers = "0123456789+-=pqrMN><ABCDxU[]|ayQkPRbScEOmZnfghtijzFl'"



for i in range(len(whole_numbers)):
    data = re.sub(whole_numbers[i],correct_numbers[i],data)

data = re.sub("A1",r"A_1",data)
data = re.sub("B1",r"B_1",data)
data = re.sub("C1",r"C_1",data)
data = re.sub("D1",r"D_1",data)
#替换题号
data = re.sub("([例]*[0-9]+\.[\s]+)","\\\\item ",data)

#公式标志换成$符号
data = re.sub("\\\\\[",r"$",data)
data = re.sub("\\\\\]",r"$",data)
data = re.sub("\$\$","",data)

#选择题替换成标准格式
data = re.sub("A\.([\s\S]*?)B\.([\s\S]*?)C\.([\s\S]*?)D\.([\s\S]*?)\\n",multiple_choice,data)
data = re.sub("\(A\)([\s\S]*?)\(B\)([\s\S]*?)\(C\)([\s\S]*?)\(D\)([\s\S]*?)\\n",multiple_choice,data)
data = re.sub("Ａ\.([\s\S]*?)Ｂ\.([\s\S]*?)Ｃ\.([\s\S]*?)Ｄ\.([\s\S]*?)\\n",multiple_choice,data)
data = re.sub("\(Ａ\)([\s\S]*?)\(Ｂ\)([\s\S]*?)\(Ｃ\)([\s\S]*?)\(Ｄ\)([\s\S]*?)\\n",multiple_choice,data)
data = re.sub("\$[ ]+\}","$}",data)
data = re.sub("\{[ ]+\$","{$",data)

#替换多余的空行
for i in range(20):
    data = re.sub("\n[\t ]*\n","\n",data)
#复数变成正体i
data = re.sub("(\\n.*?复数.*?\\n)",replace_i,data)



data1 = data #替换后暂存data1



#分离文字和公式
raw_texts = [] #文字数组
raw_equations = [] #公式数组
d = data
while len(d) > 0:
    interval = re.search(r"\$[\s\S]*?\$",d)
    if not interval == None:
        (start, end) = interval.span()
        raw_texts.append(d[:start])
        raw_equations.append(d[start:end])
        d = d[end:]
    else:
        raw_texts.append(d)
        d = ""
#至此已经分离了文字和公式，公式在两个$之内，包含两个$

modified_texts = []
modified_equations = []

for text in raw_texts:
    #填空题的处理
    text1 = re.sub("[ __]{5,}",r"\\blank{50}",text)
    #选择题的处理
    text1 = re.sub(r"\(\\blank\{50\}\)","\\\\bracket{20}",text1)
    #逗号后面加空格
    text1 = re.sub(",[ ]*",", ",text1)
    modified_texts.append(text1)

for equation in raw_equations:
    equation1 = equation
    # 去除单个字周围的大括号和去除双重无意义的大括号
    for i in range(20):
        equation1 = re.sub("(\{[\w\+\-*]?\})",refine_brackets,equation1)
    for i in range(20):
        equation1 = re.sub("(\{\{.*?\}\})",refine_brackets,equation1)
    #有分数或根号的判定之后去除无意义的大括号
    sqrt_or_frac = False
    if not "sqrt" in equation1 and not "frac" in equation1:
        equation1 = re.sub("(\{[\d\w]+?\^[\d\w]+?\})",refine_brackets,equation1)
    #去除公式中的无意义的空格
    equation1 = re.sub("\\\\[!,]|\\\\quad|\\\\qquad","",equation1)
    equation1 = re.sub("\{ *\}","",equation1)
    equation1 = re.sub("\( *","(",equation1)
    equation1 = re.sub(" *\)",")",equation1)
    equation1 = re.sub("\$ *","$",equation1)
    equation1 = re.sub(" *\$","$",equation1)
    #固定公式和字母之间加空格
    equation1 = re.sub("(arrow[\w]|frac[\w\d]|sqrt[\w\d]|overline[\w\d])",insert_a_blank,equation1)
    #改善交集和并集
    equation1 = equation1.replace("\\bigc","\\c")
    #在数集中的数集改为粗黑体
    equation1 = re.sub("\\\i(n[ ]*[R|Q|Z|N|C])",boldsymbols,equation1)
    equation1 = re.sub(r"\\mathbf([ZRNQC])",blackboardbold,equation1)
    equation1 = re.sub(r"\\text([ZRNQC])",blackboardbold,equation1)
    #equation1 = re.sub("\$([R|Q|Z|N|C])\$",singleboldsymbols,equation1)
    #有关数列极限
    equation1 = re.sub(r"\\underset{([\w]\\to \\infty) }{\\mathop\\lim }\\,",limit,equation1) 
    equation1 = re.sub(r"\\underset{([\w]\\to \\infty) }{\\mathop{lim}}\\,",limit,equation1) 
    equation1 = re.sub(r"\\underset{([\w]\\to \\infty) }{\\mathop{\\lim }}\\,",limit,equation1)
    equation1 = re.sub(r"\\underset{([\w]\\to \\infty) }{\\mathop{\\lim }}",limit,equation1)
    equation1 = re.sub(r"\\underset{([\w]\\to \\infty) }{\\mathop{\\lim }",limit,equation1)
    #分情况和方程组的处理
    equation1 = re.sub("align\}[\s]*","cases}",equation1)
    equation1 = re.sub(r"\\\\[\s]*","\\\\\\\\",equation1)
    equation1 = re.sub(r"&",r"",equation1)
    equation1 = re.sub(r"\\\{[\s]*\\begin",r"\\begin",equation1)
    equation1 = re.sub(r"\\\\\\end",r"\\end",equation1)


    modified_equations.append(equation1)

#整合修改过的文本和公式    
modified_data = ""
for i in range(len(modified_texts)):
    try:
        modified_data += modified_texts[i]
    except:
        a = 1
    try:
        modified_data += modified_equations[i]
    except:
        a = 1
modified_data = re.sub(r"[ ]+\n","\n",modified_data)
with open("outputfile.txt","w",encoding = "utf8") as f:
    f.write(modified_data)
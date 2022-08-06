import os
def dollared(string):
    flag = True
    for c in string:
        if not c in "1234567890.+-:[]()":
            flag = False
            break
    if flag:
        string = "$" + string + "$"
    return string


try:
    os.chdir(r"D:\mathdept\mathdept\文本处理程序等")
except:
    os.chdir(r"D:\mathdept\文本处理程序等")
with open("textfile.txt", "r", encoding = "utf8") as textfile:
    data = textfile.read()

data1 = ""
for c in data:
    if 65296 <= ord(c) < 65306:
        data1 += str(ord(c)-65296)
    else:
        data1 += c
data = data1
data = data.replace("．",".").replace("：",":")
elements = data.split("\n")
elements_per_line = int(elements.pop(-1)) #这里需要修改
contents = "\\begin{center}\n\\begin{tabular}{|"
for i in range(elements_per_line):
    contents += "c|"
contents += "}\n"
contents += r"\hline"+"\n"
col = 1
for element in elements:
    if col != 1:
        contents += " & "
    contents += dollared(element)
    if col == elements_per_line:
        contents += r" \\ \hline"+"\n"
    col += 1
    if col > elements_per_line:
        col = 1
contents += "\\end{tabular}" + "\n" + "\\end{center}"

with open("tablefile.txt","w",encoding = "utf8") as f:
    f.write(contents)
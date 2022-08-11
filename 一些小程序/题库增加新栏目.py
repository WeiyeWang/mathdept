import os,re
os.chdir("d:/mathdept/题库0.2")
vaults = [f for f in os.listdir() if "题库" in f]
for f in vaults:
    with open(f,"r",encoding = "utf8") as oldfile:
        data = oldfile.read()
    data1 = re.sub("<E备注>[\s]*?\[E题目\]","<E备注>\n<B解答空间>\n\n<E解答空间>\n[E题目]",data) #这一行需要替换
    with open(f,"w",encoding = "utf8") as newfile:
        newfile.write(data1)
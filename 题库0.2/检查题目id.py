import re
#os.chdir(r"d:\mathdept\mathdept\题库0.2")
vaults = [f for f in os.listdir() if "题库" in f and f[-4:] == ".txt"]
s = [str(i).zfill(6) for i in range(1,99999)]
errorid = []
for file in vaults:
    with open(file,"r",encoding = "utf8") as f:
        data = f.read()
    ids = re.findall("<BID>[\s]*?([\d]+?)[\s]*?<EID>",data)
    for id in ids:
        if not id in s:
            errorid.append(id)
        else:
            s.pop(s.index(id))
print("重复的ID:",errorid)
print("可以用的前100个ID:",s[:100])
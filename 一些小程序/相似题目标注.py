import os,re
def find_file(id,files):
    for f in files:
        if f[1:7]<id<f[9:15]:
            break
    return f

with open("../题库0.2/相似题目处理中.txt","r",encoding = "utf8") as f:
    similar_text = "\n"+f.read()
pairs = re.findall("\\n(\d\.\d\d\d\d) (\w\w)[\s\S]*?\\n(\d{6})[\s\S]*?\\n(\d{6})",similar_text)
files = [f for f in os.listdir("../题库0.2") if f[0]=="("]
for pair in pairs:    
    if pair[1] == "相同":
        file1 = find_file(pair[2],files)
        file2 = find_file(pair[3],files)
        print("相同",pair[2],pair[3],file1,file2)
        with open("../题库0.2/"+file1,"r",encoding = "utf8") as f1:
            file1_data = f1.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",file1_data)
        for p in problems:
            if pair[2] in p:
                problem_to_mark = p
                #print(problem_to_mark)
        same_record = re.findall("<B相同题目>[\s\S]*?<E相同题目>",problem_to_mark)[0]
        if not pair[3] in same_record:
            modified_record = same_record.replace("\n\n","\n").replace("<E相同题目>",pair[3]+"\n"+"<E相同题目>")
        else:
            modified_record = same_record
        problem_marked = problem_to_mark.replace(same_record,modified_record)
        #print(problem_marked)
        file1_data_modified = file1_data.replace(problem_to_mark,problem_marked)
        with open("../题库0.2/"+file1,"w",encoding = "utf8") as f1:
            f1.write(file1_data_modified)

        with open("../题库0.2/"+file2,"r",encoding = "utf8") as f2:
            file2_data = f2.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",file2_data)
        for p in problems:
            if pair[3] in p:
                problem_to_mark = p
                #print(problem_to_mark)
        same_record = re.findall("<B相同题目>[\s\S]*?<E相同题目>",problem_to_mark)[0]
        if not pair[2] in same_record:
            modified_record = same_record.replace("\n\n","\n").replace("<E相同题目>",pair[2]+"\n"+"<E相同题目>")
        else:
            modified_record = same_record
        problem_marked = problem_to_mark.replace(same_record,modified_record)
        #print(problem_marked)
        file2_data_modified = file2_data.replace(problem_to_mark,problem_marked)
        with open("../题库0.2/"+file2,"w",encoding = "utf8") as f2:
            f2.write(file2_data_modified)

        
    elif pair[1] == "关联":
        file1 = find_file(pair[2],files)
        file2 = find_file(pair[3],files)
        print("关联",pair[2],pair[3],file1,file2)
        with open("../题库0.2/"+file1,"r",encoding = "utf8") as f1:
            file1_data = f1.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",file1_data)
        for p in problems:
            if pair[2] in p:
                problem_to_mark = p
                #print(problem_to_mark)
        same_record = re.findall("<B关联题目>[\s\S]*?<E关联题目>",problem_to_mark)[0]
        if not pair[3] in same_record:
            modified_record = same_record.replace("\n\n","\n").replace("<E关联题目>",pair[3]+"\n"+"<E关联题目>")
        else:
            modified_record = same_record
        problem_marked = problem_to_mark.replace(same_record,modified_record)
        #print(problem_marked)
        file1_data_modified = file1_data.replace(problem_to_mark,problem_marked)
        with open("../题库0.2/"+file1,"w",encoding = "utf8") as f1:
            f1.write(file1_data_modified)

        with open("../题库0.2/"+file2,"r",encoding = "utf8") as f2:
            file2_data = f2.read()
        problems = re.findall("(\[B题目\][\s\S]*?\[E题目\])",file2_data)
        for p in problems:
            if pair[3] in p:
                problem_to_mark = p
                #print(problem_to_mark)
        same_record = re.findall("<B关联题目>[\s\S]*?<E关联题目>",problem_to_mark)[0]
        if not pair[2] in same_record:
            modified_record = same_record.replace("\n\n","\n").replace("<E关联题目>",pair[2]+"\n"+"<E关联题目>")
        else:
            modified_record = same_record
        problem_marked = problem_to_mark.replace(same_record,modified_record)
        #print(problem_marked)
        file2_data_modified = file2_data.replace(problem_to_mark,problem_marked)
        with open("../题库0.2/"+file2,"w",encoding = "utf8") as f2:
            f2.write(file2_data_modified)
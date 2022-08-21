import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import vaulttools as vt

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("测试")
        self.resize(1000,700)

        self.button1 = QPushButton("读取题目", self)
        self.button1.move(0, 0)
        self.button1.clicked.connect(self.read_problem)

        self.button2 = QPushButton("写入题库", self)
        self.button2.move(520, 0)
        self.button2.clicked.connect(self.modify_problem)

        self.contentbrowser = QTextBrowser(self)
        self.contentbrowser.move(0, 50)
        self.contentbrowser.resize(480,150)
        self.contentbrowser.setFont(QFont("Consolas"))


        self.contentedit = QTextEdit(self)
        self.contentedit.move(520,50)
        self.contentedit.resize(480,150)
        self.contentedit.setFont(QFont("Consolas"))
        self.contentedit.textChanged.connect(self.coloringcontent)

        self.anslabel1 = QLabel("答案",self)
        self.anslabel1.move(0,200)
        self.anslabel1.resize(50,20)
        self.anslabel2 = QLabel("答案",self)
        self.anslabel2.move(520,200)
        self.anslabel2.resize(520,20)

        self.answerbrowser = QTextBrowser(self)
        self.answerbrowser.move(0, 220)
        self.answerbrowser.resize(480,40)
        self.answerbrowser.setFont(QFont("Consolas"))

        self.answeredit = QTextEdit(self)
        self.answeredit.move(520,220)
        self.answeredit.resize(480,40)
        self.answeredit.setFont(QFont("Consolas"))
        self.answeredit.textChanged.connect(self.coloringanswer)




        self.id_input = QTextEdit(self)
        self.id_input.move(200,0)
        self.id_input.resize(100,40)
        self.id_input.setFont(QFont("Consolas"))

        dir = os.getcwd()
        if dir[-5:] == "一些小程序":
            os.chdir("..")

        (self.problems_str,self.problems_list,self.problems_dict) = vt.vaults_to_string_and_dicts("题库0.2/")  
        self.vaults = [f for f in os.listdir("题库0.2/") if "题库" in f]

    def read_problem(self):
        try:
            self.problem = self.problems_dict[str(self.id_input.toPlainText()).zfill(6)]
            self.raw_problem = self.problems_list[str(self.id_input.toPlainText()).zfill(6)]
            self.contentbrowser.setText(self.problem["content"])
            self.contentedit.setText(self.contentbrowser.toPlainText())
            self.answerbrowser.setText(self.problem["ans"])
            self.answeredit.setText(self.answerbrowser.toPlainText())
            
        except:
            print(self.id_input.toPlainText(),"有误")
        self.id = str(self.id_input.toPlainText()).zfill(6)
        print(self.id)

    def modify_problem(self):
        self.problem["content"] = vt.trim(self.contentedit.toPlainText())
        self.problem["ans"] = vt.trim(self.answeredit.toPlainText())
        print("题目:",self.contentedit.toPlainText())
        print("答案:",self.answeredit.toPlainText())
        self.new_problem = vt.create_string_from_dict(self.problem)
        for v in self.vaults:
            if v[1:7] <= self.id <= v[9:15]:
                with open("题库0.2/"+v,"r",encoding="utf8") as f:
                    data = f.read()
                newdata = data.replace(self.raw_problem,self.new_problem)
                with open("题库0.2/"+v,"w",encoding="utf8") as f:
                    f.write(newdata)
                break
    def coloringcontent(self):
        if not vt.trim(self.contentedit.toPlainText()) == vt.trim(self.contentbrowser.toPlainText()):
            self.contentbrowser.setStyleSheet('''QWidget{background-color:#66CCFF;}''')
        else:
            self.contentbrowser.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
    def coloringanswer(self):
        if not vt.trim(self.answeredit.toPlainText()) == vt.trim(self.answerbrowser.toPlainText()):
            self.answerbrowser.setStyleSheet('''QWidget{background-color:#66CCFF;}''')
        else:
            self.answerbrowser.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')


        







app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
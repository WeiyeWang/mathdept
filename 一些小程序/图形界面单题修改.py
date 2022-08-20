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

        self.textbrowser = QTextBrowser(self)
        self.textbrowser.move(0, 50)
        self.textbrowser.resize(480,150)
        self.textbrowser.setFont(QFont("Consolas"))


        self.textedit = QTextEdit(self)
        self.textedit.move(520,50)
        self.textedit.resize(480,150)
        self.textedit.setFont(QFont("Consolas"))
        self.textedit.textChanged.connect(self.coloring)


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
            self.textbrowser.setText(self.problems_dict[str(self.id_input.toPlainText()).zfill(6)]["content"])
            self.textedit.setText(self.textbrowser.toPlainText())
            self.problem = self.problems_dict[str(self.id_input.toPlainText()).zfill(6)]
            self.raw_problem = self.problems_list[str(self.id_input.toPlainText()).zfill(6)]
        except:
            print(self.id_input.toPlainText(),"有误")
        self.id = str(self.id_input.toPlainText()).zfill(6)
        print(self.id)

    def modify_problem(self):
        self.problem["content"] = vt.trim(self.textedit.toPlainText())
        print(self.textedit.toPlainText())
        self.new_problem = vt.create_string_from_dict(self.problem)
        for v in self.vaults:
            if v[1:7] <= self.id <= v[9:15]:
                with open("题库0.2/"+v,"r",encoding="utf8") as f:
                    data = f.read()
                newdata = data.replace(self.raw_problem,self.new_problem)
                with open("题库0.2/"+v,"w",encoding="utf8") as f:
                    f.write(newdata)
                break
    def coloring(self):
        if not vt.trim(self.textedit.toPlainText()) == vt.trim(self.textbrowser.toPlainText()):
            self.textbrowser.setStyleSheet('''QWidget{background-color:#66CCFF;}''')
        else:
            self.textbrowser.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')


        







app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
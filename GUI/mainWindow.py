# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import csv, io
from pert import Aktivnost
from pert import Cvor
from pert import Pert

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1103, 828)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1098, 771))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setHorizontalSpacing(7)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 2)
        self.textBox = QtWidgets.QTextEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBox.sizePolicy().hasHeightForWidth())
        self.textBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.textBox.setFont(font)
        self.textBox.setStyleSheet("")
        self.textBox.setObjectName("textBox")
        self.gridLayout.addWidget(self.textBox, 3, 0, 1, 2)
        self.labelSlikaGrafa = QtWidgets.QLabel(self.gridLayoutWidget)
        self.labelSlikaGrafa.setObjectName("labelSlikaGrafa")
        self.gridLayout.addWidget(self.labelSlikaGrafa, 10, 0, 1, 1)
        self.labelRezultat = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(10)
        self.labelRezultat.setFont(font)
        self.labelRezultat.setObjectName("labelRezultat")
        self.gridLayout.addWidget(self.labelRezultat, 9, 0, 1, 1)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.doubleSpinBox.setFont(font)
        self.doubleSpinBox.setMaximum(1.0)
        self.doubleSpinBox.setSingleStep(0.1)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 4, 1, 1, 1)
        self.buttonIzracunaj = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonIzracunaj.sizePolicy().hasHeightForWidth())
        self.buttonIzracunaj.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(16)
        self.buttonIzracunaj.setFont(font)
        self.buttonIzracunaj.setStyleSheet("justifyContent: \'center\';\n"
"background-color: rgb(51, 133, 255);\n"
"height: 40;\n"
"width: 250;\n"
"margin: 10;\n"
"borderRadius: 30;\n"
"paddingHorizontal: 30;\n"
"marginTop: 30;\n"
"alignItems: \'center\';\n"
"fontSize: 20;\n"
"color: \"#FFF\";\n"
"fontWeight: \"bold\"")
        self.buttonIzracunaj.setObjectName("buttonIzracunaj")
        self.gridLayout.addWidget(self.buttonIzracunaj, 5, 0, 1, 2, QtCore.Qt.AlignHCenter)

        self.buttonIzracunaj.clicked.connect(self.on_click)

        self.naslov = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.naslov.setFont(font)
        self.naslov.setAlignment(QtCore.Qt.AlignCenter)
        self.naslov.setObjectName("naslov")
        self.gridLayout.addWidget(self.naslov, 1, 0, 1, 2)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1, QtCore.Qt.AlignLeft)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1103, 26))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(mainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.labelSlikaGrafa.setText(_translate("mainWindow", "TextLabel"))
        self.labelRezultat.setText(_translate("mainWindow", "Ovdje ispisati rezultat"))
        self.buttonIzracunaj.setText(_translate("mainWindow", "Izračunaj"))
        self.naslov.setText(_translate("mainWindow", "PERT/TIME algoritam"))
        self.label.setText(_translate("mainWindow", " Naziv, Preduvjeti, Optimistično vrijeme, Modalno vrijeme, Pesimistično vrijeme"))
        self.label_2.setText(_translate("mainWindow", "Vjerovatnoća za procjenu:"))
        self.label_3.setText(_translate("mainWindow", "Rezultat:"))
        self.menuAbout.setTitle(_translate("mainWindow", "File"))
        self.actionAbout.setText(_translate("mainWindow", "About"))

    def on_click(self):
        #dobavljanje teksta iz text box-a
        # očekivani unos je formata: naziv,preduvjet1 preduvjet2 preduvjet3,optimisticno,modalno,pesimisticno
        mytext = self.textBox.toPlainText()
        #pretvaranje u velika slova
        mytext=mytext.upper()
        mytext= "naziv,preduvjeti,optimisticno,modalno,pesimisticno\n"+mytext

        # pretvara uneseni csv tekst u listu dict objekata
        reader = csv.DictReader(io.StringIO(mytext))
        userInput= list(reader)
        #todo ovako citajuci kreirati niz aktivnosti i izracunati sve pomocu Pert objekta
        # nakon toga tako izracunate vrijednosti prikazati i kreirati crtez (graf)
        # print(userInput[0]['naziv'])

        self.createPert(userInput)


        # ovo se moze pretvoriti i u json objekat
        # json_data = json.dumps(list(reader))
        # print(json_data)

    def validate(self,naziv,preduvjeti):
        if not isinstance(naziv, str):
            raise ValueError("Naziv treba biti string!")
        if not all(isinstance(s, str) for s in preduvjeti):
            raise ValueError("Preduvjeti trebaju biti stringovi odvjeni znakom razmaka!")
        # if not isinstance(optimisticno, (int, float)):
        #     raise ValueError("Optimisticno vrijeme treba biti broj!")
        # if not isinstance(modalno, (int, float)):
        #     raise ValueError("Modalno vrijeme treba biti broj!")
        # if not isinstance(pesimisticno, (int, float)):
        #     raise ValueError("Pesimisticno vrijeme treba biti broj!")


    def createPert(self,userInput:list):
        g=Pert()
        for element in userInput:
            try:
                naziv = element['naziv']
                preduvjeti = element['preduvjeti'].split()
                try:
                    optimisticno = float(element['optimisticno'])
                    modalno = float(element['modalno'])
                    pesimisticno = float(element['pesimisticno'])
                except ValueError as e:
                    raise ValueError("Optimistično, modalno i pesimistično vrijeme trebaju biti brojevi!")
                self.validate(naziv,preduvjeti)
                # kreiranje i dodavanje aktivnosti
                a=Aktivnost(naziv,preduvjeti,optimisticno,modalno,pesimisticno)
                g.dodajAktivnost(a)
                # self.labelRezultat.setText("OK")
            except Exception as e:
                self.labelRezultat.setText(str(e))

        try:
            g.azurirajGraf()
            self.labelRezultat.setText(str(g))
        except Exception as e:
            self.labelRezultat.setText(str(e))






# a,,1,2,3
# b,a,4,5,6

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

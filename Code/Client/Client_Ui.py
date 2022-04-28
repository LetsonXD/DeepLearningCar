from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Client(object):
    def setupUi(self, Client):
        Client.setObjectName("Client")
        Client.resize(1000, 700)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(72, 72, 72))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Client.setPalette(palette)
        Client.setStyleSheet("QWidget{\n"
"background:#536B78;\n"
"}\n"
"QAbstractButton{\n"
"border-style:none;\n"
"border-radius:0px;\n"
"padding:5px;\n"
"color:#DCDCDC;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #CEE5F2,stop:1 #536B78)\n"
"}\n"
"QAbstractButton:hover{\n"
"color:#FFFFFF;\n"
"background-color:#637081;\n"
"}\n"
"QAbstractButton:pressed{\n"
"color:#DCDCDC;\n"
"border-style:solid;\n"
"border-width:0px 0px 0px 2px;\n"
"padding:4px 4px 4px 2px;\n"
"border-color:#637081;\n"
"background-color:#444444;\n"
"}\n"
"QLabel{\n"
"color:#DCDCDC;\n"
"border:1px solid #637081;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #ACCBE1,stop:1 #536B78);\n"
"}\n"
"QLabel:focus{\n"
"border:1px solid #637081;\n"
"background:qlineargradient(spread:pad,x1:0,y1:0,x2:0,y2:1,stop:0 #646464,stop:1 #525252);\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#CEE5F2;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"border:1px solid #242424;\n"
"border-radius:3px;\n"
"padding:2px;\n"
"background:none;\n"
"selection-background-color:#CEE5F2;\n"
"selection-color:#DCDCDC;\n"
"}\n"
"\n"
"QLineEdit:focus,QLineEdit:hover{\n"
"border:1px solid #242424;\n"
"}\n"
"QLineEdit{\n"
"lineedit-password-character:9679;\n"
"}\n"
"QSlider::groove:horizontal,QSlider::add-page:horizontal{\n"
"height:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::sub-page:horizontal{\n"
"height:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:horizontal{\n"
"width:12px;\n"
"margin-top:-5px;\n"
"margin-bottom:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);\n"
"}\n"
"\n"
"\n"
"QSlider::groove:vertical,QSlider::sub-page:vertical{\n"
"width:3px;\n"
"border-radius:3px;\n"
"background:#18181a;\n"
"}\n"
"\n"
"\n"
"QSlider::add-page:vertical{\n"
"width:8px;\n"
"border-radius:3px;\n"
"background:#008aff;\n"
"}\n"
"\n"
"\n"
"QSlider::handle:vertical{\n"
"height:12px;\n"
"margin-left:-5px;\n"
"margin-right:-4px;\n"
"border-radius:6px;\n"
"background:qradialgradient(spread:pad,cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0.6 #565656,stop:0.8 #565656);\n"
"}\n"
"")
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        Client.setFont(font)
        self.Btn_ForWard = QtWidgets.QPushButton(Client)
        self.Btn_ForWard.setGeometry(QtCore.QRect(120, 300, 93, 81))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_ForWard.setFont(font)
        self.Btn_ForWard.setStyleSheet("")
        self.Btn_ForWard.setObjectName("Btn_ForWard")
        self.Btn_Turn_Left = QtWidgets.QPushButton(Client)
        self.Btn_Turn_Left.setGeometry(QtCore.QRect(30, 380, 93, 81))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Turn_Left.setFont(font)
        self.Btn_Turn_Left.setStyleSheet("")
        self.Btn_Turn_Left.setObjectName("Btn_Turn_Left")
        self.Btn_BackWard = QtWidgets.QPushButton(Client)
        self.Btn_BackWard.setGeometry(QtCore.QRect(120, 460, 93, 81))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_BackWard.setFont(font)
        self.Btn_BackWard.setStyleSheet("")
        self.Btn_BackWard.setObjectName("Btn_BackWard")
        self.Btn_Turn_Right = QtWidgets.QPushButton(Client)
        self.Btn_Turn_Right.setGeometry(QtCore.QRect(210, 380, 93, 81))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Turn_Right.setFont(font)
        self.Btn_Turn_Right.setStyleSheet("")
        self.Btn_Turn_Right.setObjectName("Btn_Turn_Right")
        self.Btn_Video = QtWidgets.QPushButton(Client)
        self.Btn_Video.setGeometry(QtCore.QRect(310, 552, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Video.setFont(font)
        self.Btn_Video.setStyleSheet("")
        self.Btn_Video.setObjectName("Btn_Video")
        self.label_Video = QtWidgets.QLabel(Client)
        self.label_Video.setGeometry(QtCore.QRect(310, 70, 661, 481))
        self.label_Video.setText("")
        self.label_Model = QtWidgets.QLabel(Client)
        self.label_Model.setGeometry(QtCore.QRect(100, 60,113, 160))
        self.label_Model.setText("")
        self.label_Level = QtWidgets.QLabel(Client)
        self.label_Level.setGeometry(QtCore.QRect(625, 600,80, 100))
        self.label_Level.setText("1")
        self.label_Video.setObjectName("label_Video")
        self.Window_Close = QtWidgets.QPushButton(Client)
        self.Window_Close.setGeometry(QtCore.QRect(950, 1, 50, 40))
        self.Window_Close.setObjectName("Window_Close")
        self.IP = QtWidgets.QLineEdit(Client)
        self.IP.setGeometry(QtCore.QRect(1, 1, 101, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.IP.setFont(font)
        self.IP.setStyleSheet("")
        self.IP.setObjectName("IP")
        self.Btn_Connect = QtWidgets.QPushButton(Client)
        self.Btn_Connect.setGeometry(QtCore.QRect(102, 1, 90, 30))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.Btn_Connect.setFont(font)
        self.Btn_Connect.setObjectName("Btn_Connect")
        self.HSlider_Servo1 = QtWidgets.QSlider(Client)
        self.HSlider_Servo1.setGeometry(QtCore.QRect(300, 580, 671, 61))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(10)
        self.HSlider_Servo1.setFont(font)
        self.HSlider_Servo1.setStyleSheet("")
        self.HSlider_Servo1.setOrientation(QtCore.Qt.Horizontal)
        self.HSlider_Servo1.setObjectName("HSlider_Servo1")
        self.label_Servo1 = QtWidgets.QLabel(Client)
        self.label_Servo1.setGeometry(QtCore.QRect(545, 570, 180, 31))
        font = QtGui.QFont()
        font.setFamily("3ds")
        font.setPointSize(14)
        self.Window_Min = QtWidgets.QPushButton(Client)
        self.Window_Min.setGeometry(QtCore.QRect(900, 1, 50, 40))
        self.Window_Min.setObjectName("Window_Min")
        self.retranslateUi(Client)
        QtCore.QMetaObject.connectSlotsByName(Client)

    def retranslateUi(self, Client):
        _translate = QtCore.QCoreApplication.translate
        self.Btn_ForWard.setText(_translate("Client", "ForWard"))
        self.Btn_Turn_Left.setText(_translate("Client", "Turn Left"))
        self.Btn_BackWard.setText(_translate("Client", "BackWard"))
        self.Btn_Turn_Right.setText(_translate("Client", "Turn Right"))
        self.Btn_Video.setText(_translate("Client", "Open Video"))
        self.Window_Close.setText(_translate("Client", "x"))
        self.IP.setText(_translate("Client", "192.168.1.151"))
        self.Btn_Connect.setText(_translate("Client", "Connect"))
        self.Window_Min.setText(_translate("Client", "-"))
        self.label_Level.setText(_translate("Client", "1"))


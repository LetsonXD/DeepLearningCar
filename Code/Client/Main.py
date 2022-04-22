#!/usr/bin/python 
# -*- coding: utf-8 -*-
import numpy as np
import cv2
import socket
import os
import io
import time
import imghdr
import sys
from threading import Timer
from threading import Thread
from PIL import Image
from Command import COMMAND as cmd
from Thread import *
from Client_Ui import Ui_Client
from levelThreeAI import levelThreeAI
from Video import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
class mywindow(QMainWindow,Ui_Client):
    def __init__(self):
        global timer
        super(mywindow,self).__init__()
        self.setupUi(self)
        self.endChar='\n'
        self.intervalChar='#'
        self.h=self.IP.text()
        self.TCP=VideoStreaming()
        self.m_DragPosition=self.pos()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.Key_W=False
        self.Key_A=False
        self.Key_S=False
        self.Key_D=False
        self.Key_Space=False
        self.setFocusPolicy(Qt.StrongFocus)
        self.label_Servo1.setText('Levels of Control')
        self.HSlider_Servo1.setMinimum(1)
        self.HSlider_Servo1.setMaximum(5)
        self.HSlider_Servo1.setSingleStep(2)
        self.HSlider_Servo1.valueChanged.connect(self.Level_Change)
        self.label_Video.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.label_Model.setPixmap(QPixmap('./model.jpg').scaled(113, 165, QtCore.Qt.KeepAspectRatio))
        self.level_three_ai = levelThreeAI(self)
        
        self.Btn_ForWard.pressed.connect(self.on_btn_ForWard)
        self.Btn_ForWard.released.connect(self.on_btn_Stop)

        self.Btn_Turn_Left.pressed.connect(self.on_btn_Turn_Left)
        self.Btn_Turn_Left.released.connect(self.on_btn_Stop)

        self.Btn_BackWard.pressed.connect(self.on_btn_BackWard)
        self.Btn_BackWard.released.connect(self.on_btn_Stop)

        self.Btn_Turn_Right.pressed.connect(self.on_btn_Turn_Right)
        self.Btn_Turn_Right.released.connect(self.on_btn_Stop)

        self.Btn_Video.clicked.connect(self.on_btn_video)
        self.Btn_Connect.clicked.connect(self.on_btn_Connect)
        
        self.Window_Min.clicked.connect(self.windowMinimumed)
        self.Window_Close.clicked.connect(self.close)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.time)
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
 
    def mouseMoveEvent(self, QMouseEvent):
        if QMouseEvent.buttons() and Qt.LeftButton:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
 
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        
    def on_btn_ForWard(self):
        ForWard=self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+ForWard)

    def on_btn_Turn_Left(self):
        Turn_Left=self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+ Turn_Left)

    def on_btn_BackWard(self):
        BackWard=self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+BackWard)

    def on_btn_Turn_Right(self):
        Turn_Right=self.intervalChar+str(1500)+self.intervalChar+str(1500)+self.intervalChar+str(-1500)+self.intervalChar+str(-1500)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+Turn_Right)

    def Level_Change(self):#Up or Down
        self.level=self.HSlider_Servo1.value()
        self.label_Level.setText("%d"%self.level)
        
    def on_btn_Stop(self):
        Stop=self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+Stop)

    def on_btn_video(self):
        if self.Btn_Video.text()=='Open Video':
            self.timer.start(34)
            self.Btn_Video.setText('Close Video')
        elif self.Btn_Video.text()=='Close Video':
            self.timer.stop()
            self.Btn_Video.setText('Open Video')  

    def windowMinimumed(self):
        self.showMinimized()
                            
    def on_btn_Connect(self):
        if self.Btn_Connect.text() == "Connect":
            self.h=self.IP.text()
            self.TCP.StartTcpClient(self.h,)
            try:
                self.streaming=Thread(target=self.TCP.streaming,args=(self.h,))
                self.streaming.start()
            except:
                print ('video error')
            try:
                self.recv=Thread(target=self.recvmassage)
                self.recv.start()
            except:
                print ('recv error')
            self.Btn_Connect.setText( "Disconnect")
            print ('Server address:'+str(self.h)+'\n')
        elif self.Btn_Connect.text()=="Disconnect":
            self.Btn_Connect.setText( "Connect")
            try:
                stop_thread(self.recv)
                stop_thread(self.power)
                stop_thread(self.streaming)
            except:
                pass
            self.TCP.StopTcpcClient()


    def close(self):
        self.timer.stop()
        try:
            stop_thread(self.recv)
            stop_thread(self.streaming)
        except:
            pass
        self.TCP.StopTcpcClient()
        try:
            os.remove("video.jpg")
        except:
            pass
        QCoreApplication.instance().quit()
        os._exit(0)

    def Power(self):
        while True:
            try:
                self.TCP.sendData(cmd.CMD_POWER+self.endChar)
                time.sleep(60)
            except:
                break
    def recvmassage(self):
            self.TCP.socket1_connect(self.h)
            self.power=Thread(target=self.Power)
            self.power.start()
            restCmd=""
            while True:
                Alldata=restCmd+str(self.TCP.recvData())
                restCmd=""
                print (Alldata)
                if Alldata=="":
                    break
                else:
                    cmdArray=Alldata.split("\n")
                    if(cmdArray[-1] != ""):
                        restCmd=cmdArray[-1]
                        cmdArray=cmdArray[:-1]
                for oneCmd in cmdArray:
                    Massage=oneCmd.split("#")
                    if cmd.CMD_SONIC in Massage:
                        self.Ultrasonic.setText('Obstruction:%s cm'%Massage[1])
                    elif cmd.CMD_LIGHT in Massage:
                        self.Light.setText("Left:"+Massage[1]+'V'+' '+"Right:"+Massage[2]+'V')
                    elif cmd. CMD_POWER in Massage:
                        percent_power=int((float(Massage[1])-7)/1.40*100)
                        self.progress_Power.setValue(percent_power) 

    def is_valid_jpg(self,jpg_file):
        try:
            bValid = True
            if jpg_file.split('.')[-1].lower() == 'jpg':  
                with open(jpg_file, 'rb') as f:
                    buf=f.read()
                    if not buf.startswith(b'\xff\xd8'):
                        bValid = False
                    elif buf[6:10] in (b'JFIF', b'Exif'):
                        if not buf.rstrip(b'\0\r\n').endswith(b'\xff\xd9'):
                            bValid = False
                    else:
                        try:
                            Image.open(f).verify()
                        except:
                            bValid = False               
            else:  
                return bValid
        except:
            pass
        return bValid

    def time(self):
        self.TCP.video_Flag=False
        try:
            if  self.is_valid_jpg('video.jpg'):
                self.label_Video.setPixmap(QPixmap('video.jpg').scaled(661, 661, QtCore.Qt.KeepAspectRatio))
        except Exception as e:
            print(e)
        self.TCP.video_Flag=True

    def levelThreeAI(self, image):
        image = self.level_three_ai.follow_lane(self)
        return image

    def drive(self, speed = 1500):

        self.back_wheels.speed = speed
        i = 0
        while self.camera.isOpened():
            _, image_lane = self.camera.read()
            image_objs = image_lane.copy()
            i += 1
            self.video_orig.write(image_lane)

            image_objs = self.process_objects_on_road(image_objs)
            self.video_objs.write(image_objs)
            show_image('Detected Objects', image_objs)

            image_lane = self.follow_lane(image_lane)
            self.video_lane.write(image_lane)
            show_image('Lane Lines', image_lane)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cleanup()
                break
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow=mywindow()
    myshow.show();   
    sys.exit(app.exec_())
    



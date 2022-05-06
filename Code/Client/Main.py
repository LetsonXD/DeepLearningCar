import numpy as np
import cv2
import os
import time
import sys
from keras.models import load_model
from threading import Thread
from PIL import Image
from PIL import ImageFile
from Command import COMMAND as cmd
from Thread import *
from Client_Ui import Ui_Client
from levelThreeAI import levelThreeAI
from Video import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# The main file used to display the U.I and all the revelvant features
ImageFile.LOAD_TRUNCATED_IMAGES = True
_SPEED = 1000

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
        self.ai_flag=False
        self.record_flag = False
        self.Key_Space=False
        self.imgArray = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.label_Servo1.setText('Levels of Control')
        self.HSlider_Servo1.setMinimum(1)
        self.HSlider_Servo1.setMaximum(5)
        self.HSlider_Servo1.setSingleStep(2)
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.HSlider_Servo1.valueChanged.connect(self.Level_Change)
        self.label_Video.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        self.label_Model.setPixmap(QPixmap('./model.jpg').scaled(113, 165, QtCore.Qt.KeepAspectRatio))
        self.level_three_ai = levelThreeAI()
        self.model = load_model('Code/AIModel/b200_e300_15_b200_200_4.7e01_96.09_check.h5')
        
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
        self.Btn_Record.clicked.connect(self.on_btn_Record)
        self.Btn_Record.hide()
        self.Btn_levelThree.clicked.connect(self.on_btn_Three)
        self.Btn_levelThree.hide()
        
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

    def on_btn_Stop(self):
        Stop=self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.intervalChar+str(0)+self.endChar
        self.TCP.sendData(cmd.CMD_MOTOR+Stop)
        
    def Level_Change(self):
        self.level = self.HSlider_Servo1.value()
        self.label_Level.setText("%d"%self.level)

    def on_btn_video(self):
        if self.Btn_Video.text()=='Open Video':
            self.timer.start(34)
            self.Btn_Video.setText('Close Video')
        elif self.Btn_Video.text()=='Close Video':
            self.timer.stop()
            self.Btn_Video.setText('Open Video')  

    def on_btn_Three(self):
        if self.Btn_levelThree.text() == 'Turn On A.I. Control':
            self.ai_flag = True
            self.Btn_levelThree.setText("Turn Off A.I. Control")
        else:
            self.Btn_levelThree.setText("Turn On A.I. Control")
            self.ai_flag = False
            self.on_btn_Stop()

    def on_btn_Record(self):
        if self.Btn_Record.text() == 'Start recording':
            self.Btn_Record.setText('Create record')
            self.record_flag = True
        else:
            if self.Btn_Record.text() == 'Create record':
                self.Btn_Record.setText('Start recording')

            self.Btn_Record.setText("Start recording")
            video = cv2.VideoWriter('tester.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (400, 300))
            for i in range(len(self.imgArray)):
                video.write(self.imgArray[i])
            video.release()
            self.record_flag = False

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
            os.remove("ai.png")
        except:
            pass
        QCoreApplication.instance().quit()
        os._exit(0)

    def Power(self):
        while True:
            try:
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
            if self.HSlider_Servo1.value() == 3:
                try:
                    self.Btn_levelThree.show()
                    self.Btn_Record.show()
                    frame = Image.open('ai.png')
                    frame = np.array(frame)
                    if len(frame.shape) == 3 and frame.shape[2] == 4:
                        frame = frame[:, :, : 3]
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    if np.shape(frame) != ():
                        self.steering_angle = self.levelThreeAI(frame)
                        left_wheel, right_wheel, left_wheel_back, right_wheel_back = self.deg_to_revs(self.steering_angle)
                        direction = '#'+ str(left_wheel)+'#'+str(left_wheel_back)+'#'+str(right_wheel)+'#'+str(right_wheel_back)+'\n'
                    if self.ai_flag:
                        self.TCP.sendData(cmd.CMD_MOTOR + direction)
                except Exception as e:
                    print(e)
            else:
                self.Btn_levelThree.hide()
            if self.HSlider_Servo1.value() == 5:
                frame = self.my_imread('ai.png')
                cv2.imshow('A.I. Vision', frame)
                Y_pred = self.model.predict_on_batch(self.img_preprocess(frame))
                print(str(Y_pred[0][0]))
                left_wheel, right_wheel, left_wheel_back, right_wheel_back = self.deg_to_revs(Y_pred[0][0])
                direction = '#'+ str(left_wheel)+'#'+str(left_wheel_back)+'#'+str(right_wheel)+'#'+str(right_wheel_back)+'\n'
                self.TCP.sendData(cmd.CMD_MOTOR + direction)
        except Exception as e:
            print(e)
        self.TCP.video_Flag=True

    def levelThreeAI(self, image):
        self.imgArray, steering_angle, _ = self.level_three_ai.follow_lane(image, self.record_flag)
        return steering_angle

    def deg_to_revs(self, curr_steering_angle):
        if curr_steering_angle == -90:
            left_wheel = 0
            right_wheel = 0
            left_wheel_back = 0
            right_wheel_back = 0
        else:
            if curr_steering_angle > 0 and curr_steering_angle <= 45:
                left_wheel = -_SPEED
                right_wheel = _SPEED * 2
                left_wheel_back = _SPEED
                right_wheel_back = _SPEED

            else:
                if curr_steering_angle > 45 and curr_steering_angle <= 90:
                    left_wheel = (_SPEED/45 * curr_steering_angle) - (_SPEED * 1.5)
                    right_wheel = _SPEED/2
                    right_wheel_back = _SPEED
                    left_wheel_back = _SPEED
                else:
                    if curr_steering_angle > 90 and curr_steering_angle <= 135:
                        left_wheel = _SPEED/2
                        right_wheel = ((-_SPEED)/45 * curr_steering_angle) + (_SPEED * 2.5)
                        left_wheel_back = _SPEED
                        right_wheel_back = _SPEED
                    else:
                        if curr_steering_angle > 135:
                            left_wheel = 2 * _SPEED
                            right_wheel = -_SPEED
                            left_wheel_back = _SPEED
                            right_wheel_back = _SPEED

        return round(left_wheel), round(right_wheel), round(left_wheel_back), round(right_wheel_back)

    def img_preprocess(self, image):
        ai_array = []
        height, _, _ = image.shape
        image = image[int(height/2):,:,:]  
        image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
        image = cv2.GaussianBlur(image, (3,3), 0) 
        image = cv2.resize(image, (200,66)) 
        image = image / 255
        ai_array.append(image)
        imgarray = np.asarray(ai_array)
        return imgarray

    def my_imread(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myshow=mywindow()
    myshow.show();   
    sys.exit(app.exec_())
    



#!/usr/bin/python 
# -*- coding: utf-8 -*-
import io
import socket
import struct
import time
import picamera
import fcntl
import  sys
import threading
from Motor import *
from ADC import *
from Thread import *
from threading import Thread
from Command import COMMAND as cmd

class Server:   
    def __init__(self):
        self.PWM=Motor()
        self.adc=Adc()
        self.tcp_Flag = True
        self.sonic=False
        self.Light=False
        self.Mode = 'one'
        self.endChar='\n'
        self.intervalChar='#'
    def get_interface_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                            0x8915,
                                            struct.pack('256s',b'wlan0'[:15])
                                            )[20:24])
    def StartTcpServer(self):
        HOST=str(self.get_interface_ip())
        self.server_socket1 = socket.socket()
        self.server_socket1.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket1.bind((HOST, 5000))
        self.server_socket1.listen(1)
        self.server_socket = socket.socket()
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
        self.server_socket.bind((HOST, 8000))              
        self.server_socket.listen(1)
        print('Server address: '+HOST)
        
        
    def StopTcpServer(self):
        try:
            self.connection.close()
            self.connection1.close()
        except Exception as e:
            print ('\n'+"No client connection")
         
    def Reset(self):
        self.StopTcpServer()
        self.StartTcpServer()
        self.SendVideo=Thread(target=self.sendvideo)
        self.ReadData=Thread(target=self.readdata)
        self.SendVideo.start()
        self.ReadData.start()
    def send(self,data):
        self.connection1.send(data.encode('utf-8'))    
    def sendvideo(self):
        try:
            self.connection,self.client_address = self.server_socket.accept()
            self.connection=self.connection.makefile('wb')
        except:
            pass
        self.server_socket.close()
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (400,300)      # pi camera resolution
                camera.framerate = 15               # 15 frames/sec
                time.sleep(2)                       # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()
                # send jpeg format video stream
                print ("Start transmit ... ")
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                    try:
                        self.connection.flush()
                        stream.seek(0)
                        b = stream.read()
                        length=len(b)
                        if length >5120000:
                            continue
                        lengthBin = struct.pack('L', length)
                        self.connection.write(lengthBin)
                        self.connection.write(b)
                        stream.seek(0)
                        stream.truncate()
                    except Exception as e:
                        print(e)
                        print ("End transmit ... " )
                        break
        except:
            #print "Camera unintall"
            pass
                 
    def stopMode(self):
        try:
            stop_thread(self.infraredRun)
            self.PWM.setMotorModel(0,0,0,0)
        except:
            pass
        try:
            stop_thread(self.lightRun)
            self.PWM.setMotorModel(0,0,0,0)
        except:
            pass            
        try:
            stop_thread(self.ultrasonicRun)
            self.PWM.setMotorModel(0,0,0,0)
            self.servo.setServoPwm('0',90)
            self.servo.setServoPwm('1',90)
        except:
            pass
        
    def readdata(self):
        try:
            try:
                self.connection1,self.client_address1 = self.server_socket1.accept()
                print ("Client connection successful !")
            except:
                print ("Client connect failed")
            restCmd=""
            self.server_socket1.close()
            while True:
                try:
                    AllData=restCmd+self.connection1.recv(1024).decode('utf-8')
                except:
                    if self.tcp_Flag:
                        self.Reset()
                    break
                print(AllData)
                if len(AllData) < 5:
                    restCmd=AllData
                    if restCmd=='' and self.tcp_Flag:
                        self.Reset()
                        break
                restCmd=""
                if AllData=='':
                    break
                else:
                    cmdArray=AllData.split("\n")
                    if(cmdArray[-1] != ""):
                        restCmd=cmdArray[-1]
                        cmdArray=cmdArray[:-1]     
            
                for oneCmd in cmdArray:
                    data=oneCmd.split("#")
                    if data==None:
                        continue
                    elif cmd.CMD_MODE in data:
                        if data[1]=='one' or data[1]=="1":
                            self.stopMode()
                            self.Mode='one'
                            
                    elif (cmd.CMD_MOTOR in data) and self.Mode=='one':
                        try:
                            data1=int(data[1])
                            data2=int(data[2])
                            data3=int(data[3])
                            data4=int(data[4])
                            if data1==None or data2==None or data2==None or data3==None:
                                continue
                            self.PWM.setMotorModel(data1,data2,data3,data4)
                        except:
                            pass
        except Exception as e: 
            print(e)
        self.StopTcpServer()    
if __name__=='__main__':
    pass

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import threading
import QtUi_designed
from PyQt5 import QtWidgets, QtCore
from time import sleep,asctime,time,localtime
from socket import *
# TODO need to fix * later


def client_send(ip, port, obj, times):
    global sendIsTrue
    sendIsTrue = True
    size = 1
    if times == 0:
        size = 0
    sockObj = socket(AF_INET, SOCK_STREAM)
    print("开始连接...")
    print(times)
    print(sendIsTrue)
    sockObj.connect((ip, port))
    # dump data obj from json to str.
    #send_message = json.loads(obj).encode()
    send_message = json.dumps(obj).encode()
    # print(send_message)
    # 数据按1024分片
    send_message_fragment = send_message[:1024]
    #send_message = send_message[1024:]
    print("开始发送...")
    while times > 0 and sendIsTrue:
        # while send_message_fragment:
        sockObj.send(send_message_fragment)
        # time delay
        sleep(1)
        # encode()
        # send_message_fragment = send_message[:1024]
        # send_message = send_message[1024:]
        times -= size
        print("times is: ",times)
    rcv_message = sockObj.recv(1024)
    print(">>>", rcv_message)
    print("...发送结束")
    sockObj.close()


def click_on_stop():
    thread2 = threading.Thread(target=cmd_stop())
    #thread2.stop()
    thread2.start()


def cmd_stop():
    global sendIsTrue
    sendIsTrue = False

def cmd_check(ip,port,obj,timeS):
    print("IP：", ip)
    if len(ip) == 0:
        print("Error: IP to send is NULL!\n")
        return
    print("端口：", port)
    if len(port) == 0:
        print("Error: port to send is NULL!\n")
        return
    port = int(port)
    print("发送次数：", timeS, "  [次数为0 则持续发送]")
    '''if len(obj) == 0:
        print("Error: data to send is NULL!\n")
        return
    else:'''
    print("发送数据：[", obj, "]")
    timeS = int(timeS)
    thread1 = threading.Thread(target=client_send, args=(ip,port,obj,timeS))
    thread1.setDaemon(True)
    thread1.start()


class RunTest(QtUi_designed.Ui_Dialog):
    def __init__(self, myinherit):
        QtUi_designed.Ui_Dialog.setupUi(self, myinherit)
        myinherit.setObjectName("广播")
        self.pushButton.clicked.connect(lambda:self.click_on_send())
        self.pushButton_2.clicked.connect(click_on_stop)
        self.pushButton_3.clicked.connect(lambda:self.click_on_send2())
        self.pushButton_4.clicked.connect(click_on_stop)
        self.mytranslateUi(myinherit)

    def mytranslateUi(self, myinherit):
        _translate = QtCore.QCoreApplication.translate
        myinherit.setWindowTitle(_translate("Dialog", "广播小程序"))

    def click_on_send(self):
        print("准备发送on")
        # self.log_print("准备发送")
        print("...")
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        timeS = self.lineEdit_3.text()
        # data2send = self.plainTextEdit.toPlainText()
        data2send = cmd_on
        # use try exception here.
        cmd_check(ip, port, data2send, timeS)

    def click_on_send2(self):
        print("准备发送off")
        # self.log_print("准备发送")
        print("...")
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        timeS = self.lineEdit_3.text()
        #data2send = self.plainTextEdit.toPlainText()
        data2send = cmd_off
        # use try exception here.
        cmd_check(ip, port, data2send, timeS)

    def log_print(self,log):
        logTime = asctime(localtime(time()))
        self.plainTextEdit_2.setPlainText(logTime+"："+log)



if __name__ == "__main__":
    sendIsTrue = True
    threads = []
    cmd_on = {"st":{"on":1},"code":1006,"gid":0,"control":23,"devaddr":"ffffffff","objtname":"lrgroup","serial":507,"appskey":"dd98929b92f09e2daf676d646d0fffff","nwkskey":"dd98929b92f09e2daf676d646d0ffffe","sendtime":1619056370,"objtop":4,"sendoffset":2}
    cmd_off = {"st":{"on":0},"code":1006,"gid":0,"control":23,"devaddr":"ffffffff","objtname":"lrgroup","serial":507,"appskey":"dd98929b92f09e2daf676d646d0fffff","nwkskey":"dd98929b92f09e2daf676d646d0ffffe","sendtime":1619056370,"objtop":4,"sendoffset":2}
    mypro = QtWidgets.QApplication(sys.argv)
    mywin = QtWidgets.QMainWindow()
    RunTest(mywin)
    mywin.show()
    sys.exit(mypro.exec_())
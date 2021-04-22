#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import threading
import QtUi_designed
from PyQt5 import QtWidgets, QtCore
from time import sleep, asctime, time, localtime
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
    # loads to get json from str and then dumps it to encode
    # can not just dumps or we will get double dumps
    # send_message = json.dumps(json.loads(obj)).encode()
    if type(obj) == str:
        send_message = obj.encode()
    else:
        send_message = json.dumps(obj).encode()
    print(send_message)
    # 数据按1024分片
    send_message_fragment = send_message
    # [:1024]
    # send_message = send_message[1024:]
    print("开始发送...")
    while times > 0 and sendIsTrue:
        # while send_message_fragment:
        sockObj.send(send_message_fragment)
        # time delay
        sleep(1)
        # send_message_fragment = send_message[:1024]
        # send_message = send_message[1024:]
        times -= size
        print("times is: ", times)
    rcv_message = sockObj.recv(1024)
    print(">>>", rcv_message)
    print("...发送结束")
    sockObj.close()


def click_on_stop():
    thread2 = threading.Thread(target=cmd_stop())
    thread2.start()


def cmd_stop():
    global sendIsTrue
    sendIsTrue = False


def cmd_check(ip, port, obj, times):
    print("IP：", ip)
    if len(ip) == 0:
        print("Error: IP to send is NULL!\n")
        return
    print("端口：", port)
    if len(port) == 0:
        print("Error: port to send is NULL!\n")
        return
    port = int(port)
    print("发送次数：", times, "  [次数为0 则持续发送]")
    '''if len(obj) == 0:
        print("Error: data to send is NULL!\n")
        return
    else:'''
    print("发送数据：[", obj, "]")
    times = int(times)
    thread1 = threading.Thread(target=client_send, args=(ip, port, obj, times))
    thread1.setDaemon(True)
    thread1.start()


class RunTest(QtUi_designed.Ui_Dialog):
    def __init__(self, my_inherit):
        QtUi_designed.Ui_Dialog.setupUi(self, my_inherit)
        my_inherit.setObjectName("广播")
        self.pushButton.clicked.connect(lambda: self.click_on_send())
        self.pushButton_2.clicked.connect(click_on_stop)
        self.pushButton_3.clicked.connect(lambda: self.click_on_send2())
        self.pushButton_4.clicked.connect(click_on_stop)
        self.mytranslateUi(my_inherit)

    def mytranslateUi(self, my_inherit):
        _translate = QtCore.QCoreApplication.translate
        my_inherit.setWindowTitle(_translate("Dialog", "广播小程序"))

    def click_on_send(self):
        print("准备发送on")
        # self.log_print("准备发送")
        print("...")
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        times = self.lineEdit_3.text()
        # data2send = self.plainTextEdit.toPlainText()
        data2send = cmd_on
        # use try exception here.
        cmd_check(ip, port, data2send, times)

    def click_on_send2(self):
        print("准备发送off")
        # self.log_print("准备发送")
        print("...")
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        times = self.lineEdit_3.text()
        # data2send = self.plainTextEdit.toPlainText()
        data2send = cmd_off
        # use try exception here.
        cmd_check(ip, port, data2send, times)

    def log_print(self, log):
        log_time = asctime(localtime(time()))
        self.plainTextEdit_2.setPlainText(log_time + "：" + log)


if __name__ == "__main__":
    sendIsTrue = True
    threads = []
    cmd_on = {"st": {"on": 1}, "code": 1006, "gid": 0, "control": 23, "devaddr": "ffffffff", "objtname": "lrgroup",
              "serial": 507, "appskey": "dd98929b92f09e2daf676d646d0fffff",
              "nwkskey": "dd98929b92f09e2daf676d646d0ffffe", "sendtime": 1619056370, "objtop": 4, "sendoffset": 2}
    cmd_off = {"st": {"on": 0}, "code": 1006, "gid": 0, "control": 23, "devaddr": "ffffffff", "objtname": "lrgroup",
               "serial": 507, "appskey": "dd98929b92f09e2daf676d646d0fffff",
               "nwkskey": "dd98929b92f09e2daf676d646d0ffffe", "sendtime": 1619056370, "objtop": 4, "sendoffset": 2}
    my_project = QtWidgets.QApplication(sys.argv)
    my_win = QtWidgets.QMainWindow()
    RunTest(my_win)
    my_win.show()
    sys.exit(my_project.exec_())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import threading
import QtUi_designed
from PyQt5 import QtWidgets, QtCore, QtGui
from time import sleep, asctime, time, localtime
from socket import *


# TODO need to fix * later
# console
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))
#console end


def client_send(ip, port, obj, times):
    global sendIsTrue, cmd, send_status
    sendIsTrue = True
    send_status = True
    size = 1
    if times == 0:
        size = 0
    print("开始连接...")
    print(times)
    print(sendIsTrue)
    global  test
    if test:
        my_print("test...")
    else:
        sockObj = socket(AF_INET, SOCK_STREAM)
        sockObj.connect((ip, port))
    # dump data obj from json to str.
    # loads to get json from str and then dumps it to encode
    # can not just dumps or we will get double dumps
    # send_message = json.dumps(json.loads(obj)).encode()
    if type(obj) == str:
        send_message = obj.encode()
    else:
        send_message = json.dumps(obj).encode()
    send_on = json.dumps(cmd_on).encode()
    send_off = json.dumps(cmd_off).encode()
    # 数据按1024分片
    send_message_fragment = send_message
    # [:1024]
    # send_message = send_message[1024:]
    print("开始发送...")
    while times > 0 and sendIsTrue:
        # while send_message_fragment:
        if cmd == 1:
            send_message_fragment = send_message
        elif cmd == 2:
            send_message_fragment = send_on
        elif cmd == 3:
            send_message_fragment = send_off
        my_print("发送数据：", send_message_fragment.decode())
        # my_print("]")
        if test:
            my_print("test in while...")
        else:
            sockObj.send(send_message_fragment)
        # time delay
        sleep(1)
        # send_message_fragment = send_message[:1024]
        # send_message = send_message[1024:]
        times -= size
        my_print("剩余发送次数 ", times)
    cmd = 1
    send_status = False
    my_print("...发送结束")
    if test:
        my_print("test stop...")
    else:
        rcv_message = sockObj.recv(1024)
        print(">>>", rcv_message)
        sockObj.close()


def my_print(log, *args):
    log_time = asctime(localtime(time()))
    print(log_time,"：",log, *args)


def cmd_check(ip, port, obj, times):
    print("IP：", ip)
    if len(ip) == 0:
        my_print("Error: IP to send is NULL!\n")
        return
    print("端口：", port)
    if len(port) == 0:
        my_print("Error: port to send is NULL!\n")
        return
    port = int(port)
    print("发送次数：", times, "  [次数为0 则持续发送]")
    times = int(times)
    thread1 = threading.Thread(target=client_send, args=(ip, port, obj, times))
    thread1.setDaemon(True)
    thread1.start()


class RunTest(QtUi_designed.Ui_Dialog):
    def __init__(self, my_inherit):
        QtUi_designed.Ui_Dialog.setupUi(self, my_inherit)
        my_inherit.setObjectName("广播")
        self.pushButton.clicked.connect(lambda: self.cmd_send_control(2))
        self.pushButton_2.clicked.connect(lambda: self.cmd_send_control(3))
        self.pushButton_3.clicked.connect(lambda: self.click_on_send())
        self.pushButton_4.clicked.connect(lambda: self.cmd_send_control(4))
        self.pushButton_5.clicked.connect(lambda: self.cmd_send_control(4))
        self.mytranslateUi(my_inherit)
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)

    def mytranslateUi(self, my_inherit):
        _translate = QtCore.QCoreApplication.translate
        my_inherit.setWindowTitle(_translate("Dialog", "广播小程序"))

    # console
    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def outputWritten(self, text):
        cursor = self.textBrowser_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textBrowser_2.setTextCursor(cursor)
        self.textBrowser_2.ensureCursorVisible()
    # console.end

    def cmd_send_control(self,code):
        global cmd
        global send_status
        if code == 2:
            cmd = 2
            my_print("群开发送>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        elif code == 3:
            cmd = 3
            my_print("群关发送>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        elif code == 4:
            global sendIsTrue
            sendIsTrue = False
            my_print("停止发送>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            return
        if send_status:
            return
        else:
            self.click_on_send()

    def click_on_send(self):
        global send_status, sendIsTrue
        if send_status:
            sendIsTrue = False
            my_print("停止当前发送中 请等待...")
            sleep(5)
        my_print("...")
        ip = self.lineEdit.text()
        port = self.lineEdit_2.text()
        times = self.lineEdit_3.text()
        data2send = self.plainTextEdit.toPlainText()
        # use try exception here.
        cmd_check(ip, port, data2send, times)


if __name__ == "__main__":
    sendIsTrue = True
    send_status = False
    test = False
    threads = []
    cmd = 1
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

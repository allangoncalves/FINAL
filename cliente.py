# -*- coding: utf-8 -*-
import socket
from Tkinter import *
import tkMessageBox
from Criptos import *
from calculadoraDH import *


class Client:
    
    BUFFER_SIZE = 1024
    
    def sendMsg(self, msg):
        self.tcpServer.send(msg)

    def __init__(self, TCP_IP, TCP_PORT):
        
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT
        self.identity = socket.gethostbyaddr(socket.gethostname())[0]
        self.tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
    	connectionTuple = (self.TCP_IP, int(self.TCP_PORT))
        self.tcpServer.connect(connectionTuple)

    def disconnect(self):
        self.tcpServer.shutdown(1)
    	self.tcpServer.close()

    


# -*- coding: utf-8 -*-
import socket
from threading import Thread

class Server:

    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self,TCP_IP="0.0.0.0", TCP_PORT=8080, BUFFER_SIZE=128):
    	self.TCP_IP = TCP_IP
    	self.connections = []
    	self.TCP_PORT = TCP_PORT
    	self.BUFFER_SIZE = BUFFER_SIZE
        self.encryption = "S-DES"
        self.previous = self.encryption

    def handler(self, clientSocket, address):
        ans = 0
        while True:
            data = clientSocket.recv(self.BUFFER_SIZE)
            print(data)
            if not data:
                self.connections.remove(clientSocket)
                clientSocket.close()
                print(str(len(self.connections)) + " - " + str(address) + " - disconnected")
                break
            if data == "NO":
                ans = 0
                self.encryption = self.previous
                for connection in self.connections:
                        connection.send("NEGATIVE "+self.previous)
            elif data == "YES":
                ans +=1
                if ans == len(self.connections):
                    self.previous = self.encryption
                    for connection in self.connections:
                        connection.send("POSITIVE "+self.encryption)
                    ans = 0
            elif data == "RC4" or data == "S-DES":
                self.encryption = data
                for connection in self.connections:
                    connection.send(data)
            else:
                for connection in self.connections:
                    connection.send(data)

    def run(self):
    	self.tcpServer.bind((self.TCP_IP, self.TCP_PORT))
        self.tcpServer.listen(1)
        print("Server: "+self.TCP_IP)
        while True:
            clientSocket, address = self.tcpServer.accept()
            newThread = Thread(target=self.handler, args=(clientSocket, address))
            newThread.daemon = True
            newThread.start()
            self.connections.append(clientSocket)
            print(str(len(self.connections))+" - "+str(address)+" - connected")

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	TCP_IP = str(s.getsockname()[0])
	s.close()

	server = Server(TCP_IP)
	server.run()

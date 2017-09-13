# -*- coding: utf-8 -*-
from threading import Thread
from cliente import *
import socket
from Criptos import *
from calculadoraDH import *
from random import randint


class userGUI:
    
    def __init__(self, master=None):

        self.numberSend = 0
        self.numberPrivate = randint(1,352)
        self.numberPrime = 353
        self.numberInt = 399
        self.key = ""
        self.keyR = "12ASasdasdfasda322"
        self.keyS = "1010101010"
        self.changeClient = DH(int(self.numberInt),int(self.numberPrime))
    

    	master.title("CriptoChat")

        self.client = None
        self.frame = Frame(master)
        self.frame["pady"] = 0
        self.frame.pack()

        self.frame2 = Frame(master)
        self.frame2["pady"] = 0
        self.frame2.pack()

        self.frameLate = Frame(master)
        self.frameLate["pady"] = 0
        self.frameLate.pack()

        self.frame3 = Frame(master)
        self.frame3["pady"] = 0
        self.frame3.pack()

        self.ipText = StringVar()
        self.ipLabel = Label(self.frame, text="IP")
        self.ipLabel.pack(side='left')        
        self.ipField = Entry(self.frame, textvariable=self.ipText)
        self.ipField.pack(side='left')

        self.portText = StringVar()
        self.portLabel = Label(self.frame, text="PORT")
        self.portLabel.pack(side='left')    
        self.portField = Entry(self.frame, textvariable=self.portText)
        self.portField.pack(side='left')
        
        self.connectButton = Button(self.frame)
        self.connectButton.config(text="Conectar", width=12, command=self.connect)
        self.connectButton.pack()

        self.alphaText = StringVar()
        self.alphaLabel = Label(self.frameLate, text="Alpha:")
        self.alphaLabel.pack(side='left')        
        self.alphaField = Entry(self.frameLate, textvariable=self.alphaText)
        self.alphaField.pack(side='left')

        self.primeText = StringVar()
        self.primeLabel = Label(self.frameLate, text="P:")
        self.primeLabel.pack(side='left')        
        self.primeField = Entry(self.frameLate, textvariable=self.primeText)
        self.primeField.pack(side='left')

        self.encrypButton = Button(self.frameLate)
        self.encrypButton.config(text="Mudar", width=12, command=self.changeKeys)
        self.encrypButton.pack(side=TOP)

        self.encryption = StringVar()
        self.encryption.set("S-DES")

        self.display = Label(self.frame2, text=self.encryption.get())
        self.display.config(fg="#000000")
        self.display.pack(side=LEFT)

        self.sdesRadio = Radiobutton(self.frame2, text="S-DES", value="S-DES", variable=self.encryption)
        self.sdesRadio.pack(side=LEFT)

        self.rc4Radio = Radiobutton(self.frame2, text="RC4", value="RC4", variable=self.encryption)
        self.rc4Radio.pack(side=LEFT)

        self.encrypButton = Button(self.frame2)
        self.encrypButton.config(text="Trocar", width=12, command=self.setCrypto)
        self.encrypButton.pack(side=LEFT)
        
        self.chatDisplay = Listbox(self.frame3, width=60)
        self.chatDisplay.pack(anchor='w', fill=X, expand=YES)

        self.msgText = StringVar()
        self.msgField = Entry(self.frame3, textvariable=self.msgText)
        self.msgField.pack()
        
        self.sendButton = Button(self.frame3, state=DISABLED)
        self.sendButton.config(text="Enviar", width=12, command=self.sendMsg)
        self.sendButton.pack()
        
    def connect(self):
        ip = self.ipText.get()
        port = int(self.portText.get())
        self.client = Client(ip, port)
        self.client.connect()
        mythread = Thread(target=self.receive)
        mythread.daemon = True
        mythread.start()
        cryptoThread = Thread(target=self.setCrypto)
    	cryptoThread.daemon = True
    	cryptoThread.start()
        self.setButtonStatus(1)

    def disconnect(self):
    	self.client.disconnect()
        self.setButtonStatus(0)
    
    def sendMsg(self):
    	print(self.encryption.get())
    	message = self.msgText.get()
        if self.encryption.get() == "RC4":
            c = RC4()
            messageRC4 = c.run(message,self.keyR)
            self.client.sendMsg(messageRC4)
            
        elif self.encryption.get() == "S-DES":
            c = SDES()
            messageSDES = c.run(message,self.keyS)
            self.client.sendMsg(messageSDES)
        self.msgField.delete(0, 'end')

    def setButtonStatus(self, id):
        if id == 1:
            self.connectButton.config(command=self.disconnect, text="Disconectar")
            self.sendButton.config(state=NORMAL)
            self.ipField.config(state='readonly')
            self.portField.config(state='readonly')
        else:
            self.connectButton.config(command=self.connect, text="Conectar")
            self.sendButton.config(state=DISABLED)
            self.ipField.config(state=NORMAL)
            self.portField.config(state=NORMAL)

    def receive(self):
        while True:
            data = self.client.tcpServer.recv(self.client.BUFFER_SIZE)
            print("esse"+data)
            if not data:
                break
            elif data.split(" ")[0] == "POSITIVE" or data.split(" ")[0] == "NEGATIVE":
                self.encryption.set(data.split(" ")[1])
                self.display.config(text=self.encryption.get())
            else:
                identification = data.split()[0]
                if identification == "RC4" or identification == "S-DES":
                    self.askQuestion(identification)
                elif data.split(" ")[0] == "SYS":

                    tkMessageBox.showinfo("Mudança de chave", "Sua chave foi alterador")
                    numberGet = int(data.split(" ")[1])
                    self.alphaText.set(int(data.split(" ")[2]))
                    self.primeText.set(int(data.split(" ")[3]))
                    self.numberPrime = self.primeText.get()
                    self.numberInt = self.alphaText.get()

                    self.keyR = self.changeClient.calcKey(numberGet)
                    self.keyS = self.changeClient.calcKey(numberGet)
                    self.keyS = "0000000000"+ bin(self.keyR%255).replace('b','')[-8::]
                    self.keyS = self.keyS[-10:]
                    self.keyR = str(self.keyR)
                    self.keyS = str(self.keyS)
                    print(self.keyR,self.keyS)
                else:
                    if self.encryption.get() == "RC4":
                        print(data)
                        dc = decRC4()
                        messageDEC = dc.run(data,self.keyR)
                        print(messageDEC)
                        self.chatDisplay.insert(END, messageDEC)
                        print(str(messageDEC+ "  --> ( RC4: "+data+" )"))
                        #self.chatDisplay.insert(END, str(data))
                    elif self.encryption.get() == "S-DES":
                        dc = decSDES()
                        messageDEC = dc.run(data, self.keyS)
                        print(messageDEC)
                        self.chatDisplay.insert(END, messageDEC)
                        print(str(messageDEC+ "  --> ( S-DES: "+data+" )"))

    def setCrypto(self):
        self.client.tcpServer.send(self.encryption.get())

    def askQuestion(self, crypto):
        ans = tkMessageBox.askyesno("Mudanca de Criptografia", "Voce deseja mudar para "+crypto+"?")
        if ans == True:
            self.client.tcpServer.send("YES")
        else:
            self.client.tcpServer.send("NO") 

    def getAlpha(self):
        pass

    def changeKeys(self):
        self.changeClient = DH(int(self.alphaText.get()),int(self.primeText.get()))
        self.changeClient.setNumPrivado(self.numberPrivate)
        self.numberSend = self.changeClient.calcSendNumber()
        self.client.tcpServer.send("SYS "+str(self.numberSend)+" "+self.alphaText.get()+" "+self.primeText.get())
        
        
'''
    def listenToChanges(self):
    	while True:
    		if self.chatDisplay.get(-1):
   	'''	
    
if __name__ == '__main__':
    import sys  
    reload(sys)  
    sys.setdefaultencoding('utf8')
    app = Tk()
    userGUI(app)
    app.mainloop()
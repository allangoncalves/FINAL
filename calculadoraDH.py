class DH:
    
    def __init__(self, integer, prime):
        self.integer = integer #publico
        self.prime = prime  #publico
        self.myNumber = 0
        
    def setNumPrivado(self, myNumber):
        self.myNumber = myNumber #tem q ser menor que q o primo
        
    def calcSendNumber(self):
        sendNumber = (self.integer**self.myNumber)%self.prime
        return sendNumber #publico
        
    def calcKey(self, clientNumber):
        result = (clientNumber**self.myNumber)%self.prime
        return result #chave


    
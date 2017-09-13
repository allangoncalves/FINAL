# -*- coding: utf-8 -*-

class RC4:
    def run(self, entrada ):    
        def converterBin_Dec(n):
                decimal = 0
                n = str(n)
                n = n[::-1]
                tam = len(n)
                for i in range(tam):
                    if n[i] == "1":
                        decimal = decimal + 2**i
                return decimal
        def xOR(n1,n2):
            if  n1 == n2:
                return "0"
            else:
                return "1"        
        def binarizarMensagem(texto):
                texto_bin = list()
                for i in range(0,len(texto)):
                    a = ord(texto[i]) 
                    aux_text = "0000000"+ bin(a).replace('b','')[-8::]
                    texto_bin.append(aux_text[-8::])
                return texto_bin
        self.entrada = entrada
                
        key = "CHgst20U4sxo5aSD2caSDv5E521"
        arrayKey = list()
        for i in range(len(key)):
            arrayKey.append(ord(key[i]))
            
        # KSA - algoritmo key-scheduling
        arrayS = list()
        for i in range(256):
            arrayS.append(i)
        j=0
        for i in range(256):
            j = (j + arrayS[i] + arrayKey[i%len(arrayKey)])%256
            aux = arrayS[i]
            arrayS[i] = arrayS[j]
            arrayS[j] = aux
            
        #PRGA - Geracao de Fluxo 
        i = 0
        j = 0
        r = list()
        for k in range(len(self.entrada)):
            i = (i + 1)%256
            j = (j + arrayS[i])%256
            aux = arrayS[i]
            arrayS[i] = arrayS[j]
            arrayS[j] = aux
            r.append(arrayS[(arrayS[i]+arrayS[j])%256])

        #binarizando tudo
        binEntrada = binarizarMensagem(self.entrada)
        binRes = list()
        for i in range(len(r)):
            a = "0000000"+ bin(r[i]).replace('b','')[-8::]
            binRes.append(a[-8::])
           
        #operacoes Xor
        resultXor = list()
        auxRes = ""
        for i in range(len(self.entrada)):
            for j in range(8):
                auxRes += xOR(binRes[i][j] , binEntrada[i][j])
            resultXor.append(converterBin_Dec(auxRes))
            auxRes=""

        #cifraASCII
        textoCifrado = ""
        for i in range(len(resultXor)):
            textoCifrado += chr(resultXor[i])

        return(textoCifrado)



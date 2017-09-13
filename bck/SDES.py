# -*- coding: utf-8 -*-
class SDES:
    def run(self, texto):
        def converterBin_Dec(n):
                decimal = 0
                n = str(n)
                n = n[::-1]
                tam = len(n)
                for i in range(tam):
                    if n[i] == "1":
                        decimal = decimal + 2**i
                return decimal
        def binarizarMensagem(texto):
                texto_bin = list()
                for i in range(0,len(texto)):
                    a = ord(texto[i]) 
                    aux_text = "0000000"+ bin(a).replace('b','')[-8::]
                    texto_bin.append(aux_text[-8::])
                return texto_bin
        def xOR(n1,n2):
            if  n1 == n2:
                return "0"
            else:
                return "1"
        def geradorChaves(chave):
            p10 =  '{2}{4}{1}{6}{3}{9}{0}{8}{7}{5}'.format(*chave) #permutacao P10
            split5a = '{0}{1}{2}{3}{4}'.format(*p10) #split1
            split5b = '{5}{6}{7}{8}{9}'.format(*p10) #split2
            ls1a = '{1}{2}{3}{4}{0}'.format(*split5a) 
            ls1b = '{1}{2}{3}{4}{0}'.format(*split5b)
            conected1 = ls1a+ls1b
            keyOne = '{5}{2}{6}{3}{7}{4}{9}{8}'.format(*conected1) #permutacao P8
            #print 'KeyOne:',keyOne
            ls2a = '{2}{3}{4}{0}{1}'.format(*ls1a) 
            ls2b = '{2}{3}{4}{0}{1}'.format(*ls1b)
            conected2 = ls2a+ls2b
            keyTwo = '{5}{2}{6}{3}{7}{4}{9}{8}'.format(*conected2) #permutacao P8
            #print 'KeyTwo:',keyTwo
            return keyOne,keyTwo
        def encriptacaoDES(chave, bit, flag):
            
            if flag == 0:
                iP = '{1}{5}{2}{0}{3}{7}{4}{6}'.format(*bit) #permutacao inicial
            else:
                iP = bit
            split5left = '{0}{1}{2}{3}'.format(*iP) #split1
            split5right = '{4}{5}{6}{7}'.format(*iP) #split2
            expPer = '{3}{0}{1}{2}{1}{2}{3}{0}'.format(*split5right) #Expansao/Permutacao
            aux = ""
            for i in range(len(expPer)):
                n = xOR(expPer[i], chave[i]) #XOR com chave1
                aux += n
            n1 = '{0}{1}{2}{3}'.format(*aux) 
            n2 = '{4}{5}{6}{7}'.format(*aux)
            S0 = [(1,0,3,2),(3,2,1,0),(0,2,1,3),(3,1,3,2)]
            S1 = [(0,1,2,3),(2,0,1,3),(3,0,1,0),(2,1,0,3)]
            linha1 = converterBin_Dec(n1[0]+n1[3])
            coluna1 = converterBin_Dec(n1[1]+n1[2])
            resultS0 = bin(S0[linha1][coluna1]).replace('b','')[-2::]
            linha2 = converterBin_Dec(n2[0]+n2[3])
            coluna2 = converterBin_Dec(n2[1]+n2[2])
            resultS1 = bin(S1[linha2][coluna2]).replace('b','')[-2::]
            aux = resultS0+resultS1
            p4 = '{1}{3}{2}{0}'.format(*aux)  
            aux2=""
            for i in range(len(p4)):
                n = xOR(p4[i],split5left[i])
                aux2 += n
            cifrado = ""    
            
            if flag == 0:
                cifrado = split5right+aux2 #switch
            else:
                cifradoAux = aux2+split5right
                cifrado = '{3}{0}{2}{4}{6}{1}{7}{5}'.format(*cifradoAux) #permutacao inicial inversa
            
            return cifrado
        self.texto = texto
        #gerarChaves8bits
        chaves = geradorChaves("1010101010")
        #binarizarMensagem
        binTexto = binarizarMensagem(self.texto)
        #encriptar
        textoCifrado = ""
        for i in range(len(binTexto)):
            bloco1 = encriptacaoDES(chaves[0], binTexto[i], 0)
            bloco2 = encriptacaoDES(chaves[1], bloco1, 1)
            textoCifrado += (chr(converterBin_Dec(bloco2)))

        return(textoCifrado)


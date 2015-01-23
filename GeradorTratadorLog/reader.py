#!/usr/bin/env python
# -*- coding: utf-8 -*-
#imports

from threading import Thread, Semaphore
import datetime
import os



#vars
arquivos_abertos = []
semaforos = []


#Classe que extende Thread e faz a leitura de um arquivo do Banco de Dados
class Reader(Thread):
    
    def __init__ (self, arquivo):
    
        Thread.__init__(self)
        self.arquivo = arquivo
    
    
    def run(self):
        read(self.arquivo)
        
#Função que faz a leitura de um arquivo de log. Ele separa as mensagens por usar.name e data
#em seguida chama a função que faz escreve a mensagem em um arquivo separado por user.name
def read(arquivo):
            
    f = open(arquivo,"r")
    lines = f.readlines()
    for x in lines:
        nome = x.split("userid=")[1].strip().replace('"','')
        horario = x.split("[")[1].split('"')[0].strip()
        write(nome+"$"+horario+"$"+x)
   


#Função que recebe duas datas em forma de String e tranforma elas para Date e as compara.
#Retorna True e a data1 > data2 e False caso contrário
def compara_hora(h1,h2):
    d1 = datetime.datetime.strptime(h1, "%d/%b/%Y:%H:%M:%S")
    d2 = datetime.datetime.strptime(h2, "%d/%b/%Y:%H:%M:%S")
    if(d1>d2):
        return True
    else:
        return False

#Função que insere uma mensagem ordenadamente em uma fila, usando como referencia para ordenação a data da mensagem
def insere_orndenado_hora(lista,mod):
    lim_sup=lista.__len__()-1
    lim_inf=0
    h1=mod.split("$")[1].strip()
    while(compara_hora(h1, lista[((lim_sup-lim_inf)/2)+lim_inf].split("[")[1].split('"')[0].strip())==False or compara_hora(lista[((lim_sup-lim_inf)/2)+lim_inf+1].split("[")[1].split('"')[0].strip(),h1)==False):
        if(compara_hora(h1, lista[(lim_sup-lim_inf)/2+lim_inf].split("[")[1].split('"')[0].strip())==False):
            lim_sup=((lim_sup-lim_inf)/2)+lim_inf
        if(compara_hora(lista[((lim_sup-lim_inf)/2+lim_inf)+1].split("[")[1].split('"')[0].strip(),h1)==False):
            lim_inf=((lim_sup-lim_inf)/2)+lim_inf
    lista.insert(((lim_sup-lim_inf)/2)+lim_inf+1,mod.split("$")[2].strip()+"\n")
    return lista

class Semaphore_nome():
    
    
    def __init__ (self,nome,semaforo):
        self.nome=nome
        self.semaforo=semaforo
    

    

def write(mensagem):
    global arquivos_abertos
    global semaforos
    
    if((mensagem.split("$")[0].strip() in arquivos_abertos) == False):
        arquivos_abertos.append(mensagem.split("$")[0])
        semaforos.append(Semaphore_nome(mensagem.split("$")[0],Semaphore()))
    for obj in semaforos:
        if(mensagem.split("$")[0]==obj.nome):
            obj.semaforo.acquire()
            print(obj.nome+ " -> entrando")
            f = open("./servidor_out/"+mensagem.split("$")[0],"a")
            f.close()
            f = open("./servidor_out/"+mensagem.split("$")[0],"r")
            arq = f.readlines()
            if(arq.__len__()==0):
                f = open("./servidor_out/"+mensagem.split("$")[0],"a")
                f.write(mensagem.split("$")[2].strip()+"\n")
                f.close()
                
            else:
                if(arq.__len__()==1):
                    print(mensagem.split("$")[1].strip())
                    if(compara_hora(mensagem.split("$")[1].strip(),arq[arq.__len__()-1].split("[")[1].split('"')[0].strip())==True):
                        f = open("./servidor_out/"+mensagem.split("$")[0],"a")
                        f.write(mensagem.split("$")[2].strip()+"\n")
                        f.close()
                    else:
                        f = open("./servidor_out/"+mensagem.split("$")[0],"w")
                        arq.insert(0,mensagem.split("$")[2].strip()+"\n")
                        f.writelines(arq)
                        f.close()
                
                else:
                    if(compara_hora(mensagem.split("$")[1].strip(),arq[arq.__len__()-1].split("[")[1].split('"')[0].strip())==True):
                        f = open("./servidor_out/"+mensagem.split("$")[0],"a")
                        f.write(mensagem.split("$")[2].strip()+"\n")
                        f.close()
                    else:
                        f = open("./servidor_out/"+mensagem.split("$")[0],"w")
                        arq = insere_orndenado_hora(arq,mensagem+"\n")
                        f.writelines(arq)
                        f.close()
            obj.semaforo.release()
            print(obj.nome+ " -> saindo")
            continue
            
        
    
    
   
def leitura_servidor(nome_servidor):

    arqs = os.listdir(nome_servidor)
    for arq in arqs:
        Reader(nome_servidor+arq).start()



leitura_servidor("./servidor1/")





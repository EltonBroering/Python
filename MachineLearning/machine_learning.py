#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports
import scipy as sp
import matplotlib.pyplot as plt

##

def error(f, x, y):
	return sp.sum((f(x)-y)**2)


data = sp.genfromtxt("dadosAnosFurtosCarros.tsv", delimiter="\t")

anos = data[:,0]
roubos = data[:,1]

anos = anos[~sp.isnan(anos)]
roubos = roubos[~sp.isnan(roubos)]

fp1 = sp.polyfit(anos, roubos, 4)	#ultimo parametro grau da função de aproximação
f1 = sp.poly1d(fp1)


plt.plot(anos, f1(anos), linewidth=2)
plt.scatter(anos,roubos)
plt.title("Propor"u'ç'u'ã'"o de furtos de carros por ano em Porto Alegre")
plt.xlabel("Ano")
plt.ylabel("N"u'ú'"mero de roubos")
plt.autoscale(tight=True)
plt.grid()
plt.show()


import scipy as sp
import matplotlib.pyplot as plt

data = sp.genfromtxt("dadosAnosFurtosCarros.tsv", delimiter="\t")

anos = data[:,0]
roubos = data[:,1]

anos = anos[~sp.isnan(anos)]
roubos = roubos[~sp.isnan(roubos)]

plt.scatter(anos,roubos)
plt.autoscale(tight=True)
plt.grid()
plt.show()
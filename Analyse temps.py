#Paramètre à tenir en compte :
#coefficient de vaporisation p entre 0 et 1 (plus p est grand plus il y a vaporisation )
#initialisation des tij à 1 pour chaque sommet (tij représente la quantité de phéromones présente sur le chemin)
#coefficients alpha et beta à poser
#la quantité de phéromones à une itération t+1 est :
#tij(t+1) = (1-p)tij(t) + Somme des delta tij(t)_k où delta tij(t)_k est la quantité de phéromones posées par la kieme fourmi
#on doit également prendre en compte la distance ou poids d'une arrête
# Comme on cherche un chemlin maximisant le poids il faut modifier la formule
#car l'algorithme des fourmis cherche un chemin minimisant les distances
#proposition : plutôt que de prendre les inverses, on peut laisser les poids originaux dans la formule
#problème possible : la grandeur des poids peut potentiellement interférer (à regarder après)

#Résultats à renvoyer :
#plusieurs options :
#On peut à la fin du nombre d'itérations donné renvoyer le chemin le plus pris par les fourmis je pense faire cela
#On peut renvoyer le chemin comportant le plus de phéromones
#On peut looper jusqu'à ce qu'elles aient toutes le même chemin (pas intéressant)


#Pour se ramener au cas de l'algorithme hongrois, on décide d'ajouter des chemins de poids "infinis"
# Pour "forcer " les fourmis à emprunter ce chemin





###################### Core program #############################

#t représente le nombre d'itérations total
#m représente le nombre de fourmis

#les probabilités de suivre un chemin seront stockées dans une liste de liste [[p00,p01,p02],[p10,p11,p12]...]
#les données attendues sont une liste de liste de la même forme qu'au dessus mais avec les poids


#IMPORTANT Dans graphe, il faut que le poids de i à i soit nul
import random
import copy
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from munkres import Munkres, print_matrix
import sys
temps = []

def actuProba(pheromones,graphe): #fonction qui va créer la liste de liste de proba à une itération t
    n = len(graphe)
    proba = []
    for i in range(n): # on créer une liste [[],[],...]
        proba.append([])
    for i in range(n):
        somme= 0
        for c in range(n):
            somme += pheromones[i][c]*graphe[i][c]

        for j in range(n):
            proba[i].append((pheromones[i][j]*graphe[i][j])/somme)

    return proba


def actuPhero(pheromones,pherotemp,p): #p coefficient de vaporisation des phéromones sur chaque chemin
    n = len(pheromones)
    for i in range(n):
        for j in range(n):
            pheromones[i][j] = (1-p)*pheromones[i][j] + pherotemp[i][j]
    return pheromones



def ant(graphe,t,m):
    p = 0.5 #coefficient de diffusion
    n = len(graphe)
    chemfourmis = []
    pheromones = []
    pherotemp = [] #pherotemp est une liste de liste qui contiendra les dépots de phéromones à
    for j in range(m):
        chemfourmis.append([])
        for i in range(n):
            chemfourmis[j].append(-1)
    for i in range(n) :

            pheromones.append([])
            pherotemp.append([])
            for j in range(n):
                pheromones[i].append(1)
                pherotemp[i].append(0)


    proba = actuProba(pheromones,graphe)
    l = [i for i in range(n)] #liste des sommets


    for i in range(t):
        phero = copy.deepcopy(pherotemp)
        for j in range(m):
            tempproba = copy.deepcopy(proba) #copie de proba pour une fourmi utile pour ligne 96 où on empeche à une fourmi de visiter un sommet déjà découvert
            #print(proba)
            #dejapasse = []
            for k in range(n):
                #nondejapasse = [i for i in l if i not in dejapasse]
                #s = random.choice(nondejapasse)

                chemfourmis[j][k] = random.choices(l,weights = tempproba[k])[0] #on récupère les probabilités liées à la position de la fourmis wtf la fonctions choices renvoie une liste de 1 elm wtf
                #print(chemfourmis[j][k])
                phero[k][chemfourmis[j][k]] += graphe[k][chemfourmis[j][k]]
                #dejapasse.append(s)
                for z in range(n):
                    tempproba[z][chemfourmis[j][k]] = 0 #on empeche la fourmi de revenir sur une ville qu'elle a déjà trouvé en mettant à 0 la probabilité d'y aller depuis n'importe quel sommet
        pheromones = actuPhero(pheromones,phero,p)
        proba = actuProba(pheromones,graphe)
    return chemfourmis


#graphe = [[5,1,9],[0,7,8],[2,3,6]]
#print(ant(graphe,1,3))




################################################ Générateur aléatoire ##########################
L = []
n = int(input("Nombre de clients"))
for i in range(n): #partie du programme pour ajouter les n listes dans une liste globale
    Temp = []
    for j in range(n):
    #    Temp.append(int(input("Temps de trajet avec le transporteur {0}".format(j+1))))
        Temp.append(random.randint(1,15))
    L.append(Temp)
fig = plt.figure()
ax = Axes3D(fig)
m = int(input('Nombre de passages'))
f = int(input('Nombre de fourmis '))
X = np.arange(0, m, 1)
Y = np.arange(0, f, 1)

X, Y = np.meshgrid(X, Y)
Z=np.zeros((m,f))
for i in range(m):
    for j in range(f):

        start = time.time()
#print(ant(L,m,f))
        ant(L,m,f)
        end = time.time()
        t = end - start
        Z[i][j] = t
################################################ Munkres ######################################
cost_matrix = []
matrix = L
p = m
Z2 = np.zeros((m,f))
start = time.time()
for row in matrix:
    cost_row = []
    for col in row:
        cost_row += [sys.maxsize - col]
    cost_matrix += [cost_row]

m = Munkres()
indexes = m.compute(cost_matrix)
#print_matrix(matrix, msg='Profit max:')
total = 0
for row, column in indexes:
    value = matrix[row][column]
    total += value




end = time.time()
for j in range(p):
    for k in range(f):
        Z2[j][k] = end-start
print(Z2)






####################################### Plot 3D ##########################################
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hot,linewidth=0, antialiased=False)
#ax.plot_surface(X, Y, Z2, rstride=1, cstride=1, cmap=plt.cm.gray,alpha = 1)
ax.set_zlim(np.amin(Z),np.amax(Z))
#set_autoscale_on(true)
ax.set_xlabel('Nombre de passages')
ax.set_ylabel('Nombre de fourmis')
ax.set_zlabel('Temps')

plt.show()


'''fichier = open('datafourmi.txt', 'a')
t = str(t)
n = str(n)
m = str(m)
f = str(f)
fichier.write("\n n = ")
fichier.write(n)
fichier.write("m = ")
fichier.write(m)
fichier.write("f = ")
fichier.write(f)
fichier.write(" t = ")
fichier.write(t)
fichier.close()
'''

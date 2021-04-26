from module_partie import Partie 
from module_vehicule import Vehicule
from module_fenetre_partie import FenetrePartie
from tkinter import*
from gestion_son import Musique
from random import randint
from copy import deepcopy

def redondant(M:list,etats:list):
    return M in etats


def Position_Depart(M:list, nbCoup:int, lim:int, nbVoit: int, etats: list, vehicules : list):
    if nbCoup>= lim and M[3][1]==M[3][2]==1 and M[3][1:].count(0)<=1 : #On a une configuration intiale "suffisamment" mélangée
        return M
    else :
        if nbCoup%10==0:
            print(nbCoup, ":")
            #print("---")
        #On cherche à déplacer la voiture 1 vers sa position de départ (se trouvant derrière lui)
        i = M[3].index(1)
        while i > 1 and M[3][i-1]==0 :
            M[3][i+1]=0
            M[3][i-1]=1
            i-=1
        nums=[i for i in range(2,nbVoit+1)]
        while nums != [] :
            k=randint(2,nbVoit)
            while k not in nums :
                k=randint(2,nbVoit)
            #print(k)
            nums.remove(k)
            vehicule=vehicules[k-1]
            y1,x1=vehicule.coor()
            ver=vehicule.est_verticale()
            y2,x2=(y1+vehicule.longueur()-1,x1) if ver else (y1,x1+vehicule.longueur()-1)
            
            vehicule.avancer()
            y,x=vehicule.coor()
            if (y,x)!=(y1,x1): #Gestion du bord
                #print("A")
                if M[y2+ver][x2+(not ver)]==0: #Gestion d'une collision
                    #print("B")
                    M[y1][x1]=0
                    M[y2+ver][x2+(not ver)]=k
                    if not redondant(M,etats):
                        #print("C")
                        etats.append(deepcopy(M))
                        Mf=Position_Depart(M,nbCoup+1,lim,nbVoit,etats,vehicules)
                        if Mf is not None:
                            return Mf
                        etats.pop()
                    M[y2+ver][x2+(not ver)]=0
                    M[y1][x1]=k
                vehicule.reculer()
                
            vehicule.reculer()
            y,x=vehicule.coor()
            if (y,x)!=(y1,x1): #Gestion du bord
                #print("D")
                if M[y][x]==0: #Gestion d'une collision
                    #print("E")
                    M[y][x]=k
                    M[y2][x2]=0
                    if not redondant(M,etats):
                        #print("F")
                        etats.append(deepcopy(M))
                        Mf=Position_Depart(M,nbCoup+1,lim,nbVoit,etats,vehicules)
                        if Mf is not None:
                            return Mf
                        etats.pop()
                    M[y2][x2]=k
                    M[y][x]=0
                vehicule.avancer()
            #print(nums)
    return None


   
def creer_Partie(M:list):
    voitures=[]
    numero=[]
    N=6
    for y in range(N):
        for x in range(N):
            num=M[y][x]
            if num>0 and num not in numero:
                k=M[y].count(num)
                numero.append(num)
                if k==1:
                    voitures.append(Vehicule((y,x),"V",3 if y<N-2 and num==M[y+2][x] else 2,num))
                else :
                    voitures.append(Vehicule((y,x),"H",k,num if y!=3 else 1))
    T=sorted(list(voitures),key=Vehicule.num)

    return Position_Depart(M,0,40,max([max(L) for L in M]),[],T)             


M=[ [11,11,11,0,12,12],
    [10,7,7,0,0,0],
    [10,0,4,3,3,3],
    [0,0,4,1,1,2],
    [9,5,5,0,6,2],
    [9,0,8,8,6,2]]


A=creer_Partie(M)

test=Tk()
Musique()
Musique.pause()

if A is not None :
    laPremierePartie=FenetrePartie(A,test)
    laPremierePartie.afficher()
else :
    print("pouet")

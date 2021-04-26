from module_vehicule import Vehicule 


class Deplacement:
    '''represente le mouvement de l'arriere d'un vehicule selon les coord de la tete,
    la direction et sa longueur'''
    def __init__(self,coord,direction,lg):
        self.coord=coord
        self.direction=direction
        self.lg=lg

    def __str__(self):
        return f'deplacement de {self.coord} de direction : {self.direction} et de longueur {self.lg}'


class Partie:
    '''La classe Partie représente la partie jouee actuellement 
    Attributs:
        int[6][6] matrice : représente la matrice 6x6 ou seront stockés les ID des véhicules
                           l'ID = 0 représente une case vide.
        [ int : Vehicule} : représente une map  id -> Vehicule pour accéder plus facilement
                            au véhicule de la case selectionnéé

        int deplacements : nombre de mouvements du joueur durant la partie incrémenté lorsque le joueur
                    a déplacé un véhicule.
        time chrono : durée de la partie

        int difficulty : echelle de difficulté ( a voir l'intervalle de niveau) '''
              
    def __init__(self,vehicules):
        ''' initialise une Partie à l'aide d'une liste de d'objets Véhicule 
            
            Le premier véhicule de la liste donc l'ID: 1 sera toujours le véhicule
            du joueur.

            Chaque Véhicule sera considéré comme orienté :
                 vers la droite si horizontal
                 vers le bas si vertical
                 car on parcourt la matrice de haut en bas et de gauche à droite '''
        
        
         
        #Cas vehicules : liste de vehicules
        if  isinstance(vehicules[0],Vehicule):
            self.vehicules = { v.id : v for v in vehicules}
            self.matrice=self.init_matrice(vehicules)
        #Cas vehicules : matrice 6x6    
        else:
            self.vehicules=self.init_vehicules(vehicules)
            self.matrice=vehicules
        self.est_gagnee=self.estGagnee()
        self.pile_deplacements=[]
        self.pile_deplacements_retour=[]
        
               


        
        

        #self.difficulty


    def __str__(self):
         return '\n'.join( str(self.matrice[i]) for i in range(6))
       


    def __eq__(self,other):
        '''retourne vrai si la partie possede la meme matrice'''
        for i in range(6):
            for j in range(6):
                if self.matrice[i][j]!=other.matrice[i][j]:
                    return False
        return True

    def init_matrice(self,vehicules):
        matrice=[ [0]*6 for _ in range(6)]
        for vehicule in self.vehicules.values():
            (y,x)=vehicule.coord # y : ligne  x : colonne
            (xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
            for i in range(vehicule.lg):
                matrice[y+i*yD][x+i*xD]=vehicule.id
        return matrice

    def init_vehicules(self,L:list):
        """Entrée : une matrice correspondant à une partie Valide
        Cette matrice contient des nombres ou le caractère X pour les
        obstacles.
        Sortie : Une liste de Voitures"""
        voitures={}
        N=6
        for y in range(N):
            for x in range(N):
                id=L[y][x]
                if id>0 and id not in voitures:
                    k=L[y].count(id)
                    if k==1:
                        voitures[id]=Vehicule((y,x),"V",3 if y<N-2 and id==L[y+2][x] else 2,id)
                    else :
                        voitures[id]=Vehicule((y,x),"H",k,id)
                    
        return voitures

        
    def recommencer(self):
        while self.pile_deplacements:
            self.retour_arriere()
        self.pile_deplacements_retour=[]
        self.est_gagnee=self.estGagnee()


    def estGagnee(self):
        '''retourne Vrai si le vehicule dont l'ID = 1 est sur la case gagnante '''
        (i,j)=self.vehicules[1].coord
        while (j+2<6) and self.matrice[i][j+2]==0:
            j+=1
        return j+2==6


        
    def vehiculePossibleDeplacement(self,vehicule):
        ''' retourne la liste des coordonnées l'arriere du Vehicule dans la matrice telle que 
        le Vehicule puisse se déplacer sans collision et selon son orientation '''
        (y,x)=vehicule.coord
        vehicule_possible_deplacement=[]
        if vehicule.orientation=="H":
            x_queue=x
            x_tete=x+vehicule.lg-1
            while x_queue-1 >=0 and self.matrice[y][x_queue-1]==0:   # on peut se déplacer vers une case a droite
                x_queue-=1
                vehicule_possible_deplacement.append((y,x_queue))
            while x_tete+1 <=5 and self.matrice[y][x_tete+1]==0:    # on peut se déplacer vers une case a gauche
                x_tete+=1
                vehicule_possible_deplacement.append((y,x_tete-vehicule.lg))
                
        else: # deplacement vertical 
            y_queue=y
            y_tete=y+vehicule.lg-1
            while y_queue-1 >=0 and self.matrice[y_queue-1][x]==0:  # on peut monter d'une case
                y_queue-=1
                vehicule_possible_deplacement.append((y_queue,x))
            while y_tete+1 <=5 and self.matrice[y_tete+1][x]==0:   # on peut décendre d'une case 
                y_tete+=1
                vehicule_possible_deplacement.append((y_tete-vehicule.lg,x))
        return vehicule_possible_deplacement
                
   
    #########################
    def updatePartie(self,vehicule,coord):
        ''' Modifie la matrice en prenant en compte les nouvelles coord de Vehicule'''
        (y,x)=vehicule.coord
        (y_new,x_new)=coord
        if y==y_new:
            direction,lg=("Droite",x_new-x) if (x<x_new) else ("Gauche",x-x_new)
        else:
            direction,lg=("Bas",y_new-y) if (y<y_new) else ("Haut",y-y_new)
        le_deplacement=Deplacement(vehicule.coord,direction,lg)
        self.pile_deplacements.append(le_deplacement)
        self.deplacer(le_deplacement)


    def retour_arriere(self):
        deplacement=self.pile_deplacements.pop()
        (y,x),direction,lg=deplacement.coord,deplacement.direction,deplacement.lg
        
        if direction=="Haut":
            d=Deplacement((y-lg,x),"Bas",lg)
        elif direction=="Bas":
            d=Deplacement((y+lg,x),"Haut",lg)
        elif direction=="Droite":
            d=Deplacement((y,x+lg),"Gauche",lg)
        else:
           d=Deplacement((y,x-lg),"Droite",lg)
        self.deplacer(d)
        self.pile_deplacements_retour.append(deplacement)

    def retour_avant(self):
        deplacement=self.pile_deplacements_retour.pop()
        self.deplacer(deplacement)
        self.pile_deplacements.append(deplacement)
        
           

    def deplacements_possibles(self):
        '''Renvoie la liste de tous les deplacements possibles de longueur 1 pour la matrice donnée'''
        answer=[]
        for vehicule in self.vehicules.values():
            (yV,xV)=vehicule.coord
            #Vertical
            if vehicule.orientation=="V":
                #  cordonnée dans la matrice  et la case est vide au dessus/dessous
                if yV-1>=0 and self.matrice[yV-1][xV]==0:  #HAUT
                    answer.append(deplacement((yV,xV),"Haut",1))
                if yV+vehicule.lg<6 and self.matrice[yV+vehicule.lg][xV]==0: #BAS
                    answer.append(deplacement((yV,xV),"Bas",1))
            #Horizontal
            else:
                #  cordonnée dans la matrice  et la case est vide a gauche/droite
                if xV-1>=0 and self.matrice[yV][xV-1]==0:  #GAUCHE
                    answer.append(deplacement((yV,xV),"Gauche",1))
                if xV+vehicule.lg<6 and self.matrice[yV][xV+vehicule.lg]==0: #DROITE
                    answer.append(deplacement((yV,xV),"Droite",1))

        return answer


    def deplacer(self,deplacement):
        '''modifie la matrice et les coordonnées du vehicule impliqué du deplacement
        en_avant est un boolean verifiant si on se deplace dans le sens normal en arriere'''
        (y,x)=deplacement.coord
        vehicule=self.vehicules[self.matrice[y][x]] #on récupère le véhicule que l'on veut déplacer.
        (dX,dY)=Vehicule.DIRECTIONS[deplacement.direction]
        (xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
        
        for i in range(vehicule.lg): # on clean
            self.matrice[y+i*yD][x+i*xD]=0
        for i in range(vehicule.lg): # remet le vehicule selon le deplacement
            self.matrice[y+i*yD+dY*deplacement.lg][x+i*xD+dX*deplacement.lg]=vehicule.id # on vides les cases
        vehicule.coord=(y+dY*deplacement.lg,x+dX*deplacement.lg)
        
            



        ###############
        ###TO DO###
        ################
        #créer une partie en partant de la fin 
        #le solveur ( en partant de la fin ?)


        ####module_script pour en créer 100 m, on mesure le temps
        ###enregister
        ###main  -> acces au data 
        ##verification des matrices -> rendondance, ect...



            




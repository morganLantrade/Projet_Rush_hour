from module_vehicule import Vehicule 

class Move():
	'''represente le mouvement de l'arriere d'un vehicule selon les coord de la tete,
	la direction et sa longueur'''
	def __init__(self,coord,direction,lg):
		self.coord=coord
		self.direction=direction
		self.lg=lg

	def __str__(self):
		return f'Move de {self.coord} de direction : {self.direction} et de longueur {self.lg}'


class Partie():
	'''La classe Partie représente la partie jouee actuellement 
	Attributs:
		int[6][6] matrice : représente la matrice 6x6 ou seront stockés les ID des véhicules
						   l'ID = 0 représente une case vide.
		[ int : Vehicule} : représente une map  id -> Vehicule pour accéder plus facilement
							au véhicule de la case selectionnéé

		int moves : nombre de mouvements du joueur durant la partie incrémenté lorsque le joueur
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


		def init_matrice(vehicules):
			matrice=[ [0]*6 for _ in range(6)]
			for vehicule in self.vehicules.values():
				(y,x)=vehicule.coord # y : ligne  x : colonne
				(xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
				for i in range(vehicule.lg):
					matrice[y+i*yD][x+i*xD]=vehicule.id
			return matrice

		

		self.vehicules = { v.id : v for v in vehicules}
		self.matrice=init_matrice(vehicules)
		self.moves=0
		#self.chrono
		#self.difficulty
		
	


	def estGagnee(self):
		'''retourne Vrai si le vehicule dont l'ID = 1 est sur la case gagnante '''
		(i,j)=self.vehicules[1].coord
		while (j+2<6) and self.matrice[i][j+2]==0:
			j+=1
		return j+2==6


	def addMove(self):
		'''incremente le nombre de mouvement '''
		self.moves+=1
	


	
	def vehiculePossibleMove(self,vehicule):
		''' retourne la liste des coordonnées l'arriere du Vehicule dans la matrice telle que 
		le Vehicule puisse se déplacer sans collision et selon son orientation '''
		(y,x)=vehicule.coord
		vehicule_possible_move=[]
		if vehicule.orientation=="H":
			x_queue=x
			x_tete=x+vehicule.lg-1
			while x_queue-1 >=0 and self.matrice[y][x_queue-1]==0:   # on peut se déplacer vers une case a droite
				x_queue-=1
				vehicule_possible_move.append((y,x_queue))
			while x_tete+1 <=5 and self.matrice[y][x_tete+1]==0:    # on peut se déplacer vers une case a gauche
				x_tete+=1
				vehicule_possible_move.append((y,x_tete-vehicule.lg))
				
		else: # deplacement vertical 
			y_queue=y
			y_tete=y+vehicule.lg-1
			while y_queue-1 >=0 and self.matrice[y_queue-1][x]==0:  # on peut monter d'une case
				y_queue-=1
				vehicule_possible_move.append((y_queue,x))
			while y_tete+1 <=5 and self.matrice[y_tete+1][x]==0:   # on peut décendre d'une case 
				y_tete+=1
				vehicule_possible_move.append((y_tete-vehicule.lg,x))
		return vehicule_possible_move
				
	########################
	# TO DO 
    # a modifier sans parcourir toute la matrice ( ou dans la classe fenetre partie ) 
    #########################""
	def updateMatrice(self,vehicule,coord):
		''' Modifie la matrice en prenant en compte les nouvelles coord de Vehicule'''
		vehicule.coord=coord
		(y,x)=vehicule.coord
		(xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
		for i in range(6):
			for j in range(6):
				if self.matrice[i][j]==vehicule.id:
					self.matrice[i][j]=0
		# avant #############################
		for i in range(vehicule.lg):
			self.matrice[y+i*yD][x+i*xD]=vehicule.id
		
			

	def __str__(self):
		answer=""
		for i in range(6):
			answer+= self.matrice[i] + " \n"
		return answer


	def __eq__(self,other):
		'''retourne vrai si la partie possede la meme matrice'''
		for i in range(6):
			for j in range(6):
				if self.matrice[i][j]!=other.matrice[i][j]:
					return False
		return True
	
	
		

	def moves_possibles(self):
		'''Renvoie la liste de tous les moves possibles de longueur 1 pour la matrice donnée'''
		answer=[]
		for vehicule in self.vehicules.values():
			(yV,xV)=vehicule.coord
			#Vertical
			if vehicule.orientation=="V":
				#  cordonnée dans la matrice  et la case est vide au dessus/dessous
				if yV-1>=0 and self.matrice[yV-1][xV]==0:  #HAUT
					answer.append(Move((yV,xV),"Haut",1))
				if yV+vehicule.lg<6 and self.matrice[yV+vehicule.lg][xV]==0: #BAS
					answer.append(Move((yV,xV),"Bas",1))
			#Horizontal
			else:
				#  cordonnée dans la matrice  et la case est vide a gauche/droite
				if xV-1>=0 and self.matrice[yV][xV-1]==0:  #GAUCHE
					answer.append(Move((yV,xV),"Gauche",1))
				if xV+vehicule.lg<6 and self.matrice[yV][xV+vehicule.lg]==0: #DROITE
					answer.append(Move((yV,xV),"Droite",1))

		return answer


	def mouvement(self,move):
		'''modifie la matrice et les coordonnées du vehicule impliqué du move'''
		(y,x)=move.coord
		vehicule=self.vehicules[self.matrice[y][x]] #on récupère le véhicule que l'on veut déplacer.
		(dX,dY)=Vehicule.DIRECTIONS[move.direction]
		(xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
		for i in range(vehicule.lg):
			self.matrice[y+i*yD][x+i*xD]=0
			self.matrice[y+i*yD+dY*move.lg][x+i*xD+dX*move.lg]=vehicule.id # on vides les cases
			vehicule.coord=(y+dY*move.lg,x+dX*move.lg)
			






			






class Vehicule:
	''' La classe Vehicule représente les objets que nous allons manipuler
	sur le plateau de taille 6x6
		Attributs :
			int id : identifiant
			int coord : représente l'arrière du véhicule qui permet de 
					    determiner les autres coordonnees dans la matrice.
			string orientation : V pour vertical et H pour horizontal
			int lg : un véhicule de longueur 2 cases ou 3 cases. '''

	ID=1 #Attribut de classe 
	DIRECTIONS= {"Bas":(0,1), "Haut" : (0,-1),"Droite":(1,0),"Gauche":(-1,0)}
	
	def __init__(self,coord,orientation,lg):
		self.id=Vehicule.ID
		Vehicule.ID+=1  # incrémentation 
		self.coord=coord  
		assert orientation=="V" or orientation=="H" , "Orientation incorrecte"
		self.orientation=orientation
		self.lg=lg
			


	def __str__(self):
		answer= f'Un vehicule de longueur {self.lg} ou l\' arriere est '
		answer+=f'placé en {self.coord} et d \'une orientation {self.orientation} '
		return answer
	
	def __eq__(self,other):
		''' la fonction __eq__ vérifie si les deux objets sont des véhicules et ont la même id '''
		return isinstance(other,Vehicule) and self.id==other.id

		

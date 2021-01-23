from Vehicule import*

class Grille():
	vide=[ [0]*6 for _ in range(6)]
	coords=[ (i,j) for i in range(6) for j in range(6)]
	selected=None
			           #list(Vehicule)
	def __init__(self,vehicules):
		self.vehicules= vehicules
		self.laGrille=self.vide[:]
		for vehicule in vehicules:
			(x,y)=vehicule.coord
			(xD,yD)=vehicule.direction
			for i in range(vehicule.lg):
				self.laGrille[x+i*yD][y+i*xD]=vehicule.id
		
	def __str__(self):
		return "\n".join(str(self.laGrille[i])for i in range(6))



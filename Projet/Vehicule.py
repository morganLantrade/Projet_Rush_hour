class Vehicule:
	DIRECTIONS = { "H" : (0,-1),"B":(0,1),"D":(1,0),"G":(-1,0)}
	ID=1
				#coord 6*6 min(i,j), "H"B"D"G  
	def __init__(self,coord,direction,lg):
		self.id=Vehicule.ID
		Vehicule.ID+=1
		self.coord=coord  
		self.direction=Vehicule.DIRECTIONS[direction]
		self.lg=lg

	def __str__(self):
		return (f'Un vehicule de longueur {self.lg} placé en {self.coord} orienté vers la direction {self.direction} ')
	def __eq__(self,other):
		return isinstance(other,Vehicule) and self.id==other.id

		

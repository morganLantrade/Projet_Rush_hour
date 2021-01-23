from Grille import*
from Vehicule import*
from Graphisme import*

lesVehicules= [ Vehicule((2,1),'D',2), #1
		    	Vehicule((0,0),"D",2), #2
			    Vehicule((0,2),'D',3), #3
			    Vehicule((1,0),'B',3), #4 
			    Vehicule((1,3),'D',2), #5
				Vehicule((1,5),"B",3), #6
				Vehicule((2,3),'B',3), #7
				Vehicule((2,4),'B',2), #8
				Vehicule((3,2),"B",2) #9
				]

test=Grille(lesVehicules)
show(test)
print(test)
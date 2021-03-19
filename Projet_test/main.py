from module_partie import Partie 
from module_vehicule import Vehicule
from module_fenetre_partie import FenetrePartie


'''WARNING : double click peut entrainer des bugs '''

lesVehicules= [ Vehicule((3,1),"H",2), #1
		    	Vehicule((0,3),"H",2), #2
			    Vehicule((1,3),"H",2), #3
			    Vehicule((1,0),"V",3), #4 
			    Vehicule((5,0),"H",3), #5
				Vehicule((1,2),"V",2), #6
				Vehicule((2,3),"V",3), #7
				Vehicule((2,5),"V",3) #8
				]

laPremierePartie=FenetrePartie(lesVehicules)
laPremierePartie.show()


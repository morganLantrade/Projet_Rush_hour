from tkinter import *
from module_partie import Partie
from module_vehicule import Vehicule

'''CONSTANTES  a voir ou les stocker '''
CASE=120 # Modifiable 
BOARD=CASE//20
WIDTH=7*CASE+BOARD
HEIGHT=6*CASE+BOARD

COLORS=["white",'red',"yellow","blue","green","orange",
"purple","grey","light green","salmon","brown","pink","dark green"]



class FenetrePartie(Partie):
	''' La classe FenetrePartie est hérite de la classe Partie et représente
	graphiquement le plateau de jeu et les différents attributs de la Partie.
	Elle sera capable de gérer les évènements.

	
		Nouveaux attributs :
		int selected : représente l'id du véhicule selectionné ( par la souris ) 
		(int,int) vector_deplacement
		(int,int) origin_click
		(int,int) selected_coord


	'''
	
	def __init__(self,vehicules):
		super().__init__(vehicules)
		self.vector_deplacement=(0,0)
		self.origin_click=(0,0)
		self.selectedCoord=(0,0)
		self.selected=None
		

	
	def coordFrame_coordMatrice(self,x,y):
		''' retourne les coordonnées (i,j) de la matrice selon les coordonnées
		(x,y) de la fenetre  '''
		(i,j)=((y-BOARD)//CASE,(x-BOARD)//CASE)
		return (i,j)

		
		
	#return le coin sup gauche,inf droit et couleur du rectangle representant la voiture
	def vehiculeIntoRect(self,vehicule):
		''' Retourne selon les coordonnées du vehicule dans la matrice et la taille CASE:
		A : les coordonnées du coin sup gauche dans la fenetre
		B : les coordonnées du in droit dans la fenetre  
				
		Pour ensuite créer le rectangle dans le canvas '''		
		
		(y,x)=vehicule.coord
		(xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
		A=(a1,a2)=BOARD+x*CASE,BOARD+y*CASE
		if (yD==0): 
			B=b1,b2=(a1+CASE*vehicule.lg,a2+CASE) #mouvement lateral
		else:
			B=b1,b2=(a1+CASE,a2+CASE*vehicule.lg) #mouvement horizontal
		
		return (A,B)
	
	#########################
	#TO DO 
	#Deplacer les rectangles au lieu de clear canvas et redessiner par desssus
	#########################
	def selectedIntoRect(self):
		''' Retourne les nouvelles coordonnées du véhicule selectionné selon le mouvement de la souris
		et gère les collisions '''
		vehicule=self.vehicules[self.selected]
		(aX,aY),(bX,bY)= self.vehiculeIntoRect(vehicule)
		vX,vY=self.vector_deplacement
		possible_move=self.vehiculePossibleMove(vehicule)
		if vehicule.orientation=="V":
			try_move=self.coordFrame_coordMatrice(aX,aY+vY)  # coord du mouvement d'arrivée dans la matrice
			if try_move in possible_move :
				aY+=vY
				bY+=vY
			elif possible_move: 
				# prend le min ou le max des moves possibles comme collision
				aY=BOARD+CASE*(max(possible_move)[0]+1 if vY>0 else min(possible_move)[0]) 
				bY=aY+CASE*vehicule.lg
		else:
			try_move=self.coordFrame_coordMatrice(aX+vX,aY)  # coord du mouvement d'arrivée dans la matrice
			if try_move in possible_move:
				aX+=vX
				bX+=vX
			elif possible_move:
				# prend le min ou le max des moves possibles comme collision
				aX=BOARD+CASE*(max(possible_move)[1]+1 if vX>0 else min(possible_move)[1])
				bX=aX+CASE*vehicule.lg
		#determine les coordonnées de la matrice pour lesquelles l'arriere du Vehicule est le plus proche
		self.selectedCoord=( (aY-BOARD)//CASE + int((aY-BOARD)%CASE>CASE//2),(aX-BOARD)//CASE+int((aX-BOARD)%CASE>CASE//2))
		
		return ((aX,aY),(bX,bY))
	

		
	def drawFleche(self,cnv):
		cnv.create_line((6*CASE+CASE//4,3*CASE+CASE//2),(7*CASE-CASE//4,3*CASE+CASE//2),width=CASE//5,arrow='last',fill="green")


	def drawVehicules(self,cnv):
		''' dessine les rectangles representant les véhicules '''
		for vehicule in self.vehicules.values():
			if vehicule.id!=self.selected:
				a,b= self.vehiculeIntoRect(vehicule)
				cnv.create_rectangle(a,b,fill=COLORS[vehicule.id],outline="black" )
			else:
				# si on ne veut pas deplacer le vehicule on appelle pas selectedIntoRect mais on change la couleur
				a,b=self.selectedIntoRect() if self.vector_deplacement!=(0,0) else self.vehiculeIntoRect(vehicule)
				cnv.create_rectangle(a,b,fill="black",outline="black" )


	
	

	def drawGrille(self,cnv):
		#return sup gauche et in droit d'une case		
		def coordIntoRect(i,j):
			'''retourne le coin sup gauche et inf droit d'une case de coordonnée (i,j) de la matrice'''
			A=(aX,aY)=(BOARD+j*CASE,BOARD+i*CASE)
			B=(aX+CASE,aY+CASE)
			return (A,B)
		rects= [ (coordIntoRect(i,j),str(self.matrice[i][j])) for i in range(6) for j in range(6)]
		for (a,b),c in rects:
			cnv.create_rectangle(a,b)
			cnv.create_text(a[0]+CASE//2,a[1]+CASE//2,text=c,font=('arial',CASE//3,'bold'),fill="black" if int(c)!=self.selected or int(c)==0  else "white")
			
	def drawMove(self,cnv):
		cnv.create_text(6*CASE+CASE//2,CASE,text="Moves",font=('arial',CASE//6,'bold'),fill="black")
		cnv.create_text(6*CASE+CASE//2,CASE+CASE//3,text=str(self.moves),font=('arial',CASE//3,'bold'),fill="black")

	def drawChrono(self,cnv):
		cnv.create_text(6*CASE+CASE//2,2*CASE,text="Time",font=('arial',CASE//5,'bold'),fill="black" )
		cnv.create_text(6*CASE+CASE//2,2*CASE+CASE//3,text="00:00",font=('arial',CASE//8,'bold'),fill="black" )

	def drawVictory(self,cnv):
		cnv.create_text(6*CASE+CASE//2,5*CASE,text="Victory",font=('arial',CASE//8,'bold'),fill="black")
		cnv.create_text(6*CASE+CASE//2,5*CASE+CASE//3,text=str(self.estGagnee()),font=('arial',CASE//8,'bold'),fill="black" )
	

	def draw(self,cnv):
		cnv.delete("all")
		self.drawVehicules(cnv)
		self.drawGrille(cnv)
		self.drawFleche(cnv)
		self.drawMove(cnv)
		self.drawVictory(cnv)
		self.drawChrono(cnv)

	
	def show(self):
		''' utilitée principale du module_fenetre_partie avec gestion d'events'''

		def selection(event):
			''' si le click est dans la grille on met a jour l'id selected
				on met a jour origin_click
				et on redessin car la couleur du vehicule selected change '''
			self.origin_click=(event.x,event.y)
			self.vector_deplacement=(0,0)
			(i,j)=self.coordFrame_coordMatrice(event.x,event.y)
			if 0<=i<=5 and 0<=j<=5 and self.matrice[i][j]!=0:
				self.selected= self.matrice[i][j]
				self.draw(cnv)
			
			
				
			

		def updateMove(event):
			''' lorsque la souris bouge avec le click  gauche activé :
				on met a jour le vector_deplacement
				et on redessine'''
			self.vector_deplacement=(event.x-self.origin_click[0],event.y-self.origin_click[1])

			self.draw(cnv)
			

		def unselect(event):
			'''lorsqu'on lache le click gauche de la souris :
					-on remet les attributs par defauts:
					vector_deplacement,selected

					-on met a jour la matrice selon le mouvement effectué

					-on incrémente move
			'''
			if self.selected and self.selectedCoord!=self.vehicules[self.selected].coord :
				self.addMove()
				self.updateMatrice(self.vehicules[self.selected],self.selectedCoord)
				
			self.vector_deplacement=(0,0)
			self.selected=None
			self.draw(cnv)
			
		

		root=Tk()
		cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
		cnv.pack(side="left",padx=0,pady=0)
		root.bind('<Button-1>',selection)
		root.bind('<B1-Motion>',updateMove)
		root.bind('<ButtonRelease-1>',unselect)
		root.title("Partie")
		self.draw(cnv)
		root.mainloop()



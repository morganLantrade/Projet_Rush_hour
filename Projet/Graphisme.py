from tkinter import *
from Grille import*
from Vehicule import*


WIDTH=705
HEIGHT=605
CASE=100
BOARD=5
COLORS=["white",'red',"yellow","blue","green","orange",
"purple","grey","light green","salmon","brown","pink","dark green"]



#return sup gauche et in droit d'une case
def coordIntoRect(i,j):
	A=(a1,a2)=(5+i*CASE,5+j*CASE)
	B=(a1+CASE,a2+CASE)
	return (A,B)

#return le coin sup gauche,inf droit et couleur du rectangle representant la voiture
def vehiculeIntoRect(Grille,vehicule):
	(i,j)=vehicule.coord
	(iD,jD)=vehicule.direction
	(a1,a2)=5+j*CASE,5+i*CASE
	a1-=(vehicule.lg-1)*CASE if iD==-1 else 0 #gauche
	a2-=(vehicule.lg-1)*CASE if jD==-1 else 0 #haut
	if (jD==0):
		B=b1,b2=(a1+CASE*vehicule.lg,a2+CASE) #mouvement lateral
	else:
		B=b1,b2=(a1+CASE,a2+CASE*vehicule.lg) #mouvement horizontal
	C=COLORS[vehicule.id] if vehicule!=Grille.selected else "black"
	return ((a1,a2),B,C)

def drawFleche(canvas):
	canvas.create_line((625,350),(675,350),width=20,arrow='last',fill="green")

def drawVehicules(cnv,Grille):
	for vehicule in Grille.vehicules:
		a,b,c= vehiculeIntoRect(Grille,vehicule)
		cnv.create_rectangle(a,b,fill=c)
def drawGrille(cnv,Grille):
	rects= [ (coordIntoRect(i,j),str(Grille.laGrille[j][i])) for (i,j) in Grille.coords]
	for (a,b),c in rects:
		cnv.create_rectangle(a,b)
		cnv.create_text(a[0]+CASE//2,a[1]+CASE//2,text=c,font=('arial',CASE//3,'bold'))

def selection(Grille,event):
	x=event.x
	y=event.y
	print(x,y)

def show(Grille):
	root=Tk()
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
	cnv.pack(side="left",padx=0,pady=0)
	drawVehicules(cnv,Grille)
	drawFleche(cnv)
	drawGrille(cnv,Grille)
	root.bind('Button-1',selection)
	root.title("ebauche")
	root.mainloop()


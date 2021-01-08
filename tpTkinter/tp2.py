from random import sample
from tkinter import Tk, Canvas

UNIT=15
COLORS=["ivory","lime green"]

class Forest:
	def __init__(self,size,density):
		forest= [ (col,row) for row in range(size) for col in range(size)] 
		nb_trees=int(size**2*density)
		trees=sample(forest,nb_trees)
		self.size=size
		self.unit=UNIT
		self.grid= [[0]*size for _ in range(size)]
		for xTree,yTree in trees:
			self.grid[yTree][xTree]=1
		
	

def drawForest(canvas,foret):
	def coordIntoRect(i,j):
		A=(a1,a2)=((i+1)*UNIT,(1+j)*UNIT)
		B=(a1+UNIT,a2+UNIT)
		C= COLORS[foret.grid[i][j]]
		return (A,B,C)
	n=foret.size
				#coin sup gauche     coin inf droit         couleur
	rects = [ coordIntoRect(i,j) for i in range(n) for j in range(n) ]
	for a,b,c in rects:
		canvas.create_rectangle(a,b,fill=c)


	
def show(size,density):
	root=Tk()
	cvn=Canvas(root,width=size*UNIT+UNIT*2,height=size*UNIT+UNIT*2, background="ivory")
	cvn.pack()
	drawForest(cvn,Forest(size,density))
	root.title(f'Foret de taille {size}x{size} et de densité {density}')
	root.mainloop()

show(50,0.45)

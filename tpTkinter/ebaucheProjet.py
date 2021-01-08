from tkinter import *

WIDTH=705
HEIGHT=605
CASE=100
BOARD=5
COLORS=["white",'red',"yellow","blue","green","orange","purple","grey"]

Grid= [ [0,0,2,0,0,0],[3,0,2,0,3,3],[3,0,2,0,0,0],[0,1,1,0,4,5],[6,6,0,0,4,5],[3,3,3,0,7,7] ]

class vehicule:
	def __init__(self,listeCoord,color):
		self.coords=listeCoord
		self.color=color
		self.direction=(1,0) if listeCoord[0][0]==listeCoord[1][0] else  (0,1)
		self.lg=len(listeCoord)
		if self.direction=(1,0):
			if self.coords[0][1]>0:
				A=(listeCoord[0][1]-1,listeCoord[0][0]) else (-1,-1)
			if self.coords[self.lg-1][1]<5:
				B=(listeCoord[self.lg-1][1]+1,listeCoord[self.lg-1])
			self.casePossibles=[]
			if (Grid[A[0]][A[1]]==0) self.casePossibles.append(A)
			if (Grid[B[0]][B[1]]==0) self.casePossibles.append(B)

def updateGrid(vehicule):
	for (x,y) in vehicule.listeCoord:
		if Grid[x][y]!=0 : return;
	for (x,y) in vehicule.listeCoord:
		Grid[x][y] = COLORS.indexOf(vehicule.color)

def coordIntoRect(i,j):
	A=(a1,a2)=(5+j*CASE,5+i*CASE)
	B=(a1+CASE,a2+CASE)
	C=COLORS[Grid[i][j]]
	return (A,B,C)

def drawFleche(canvas):
	canvas.create_line((625,350),(675,350),width=20,arrow='last',fill="green")

def show():
	root=Tk()
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
	cnv.pack(side="left",padx=0,pady=0)
	rects= [ coordIntoRect(i,j) for i in range (6) for j in range(6)]
	for a,b,c in rects:
		cnv.create_rectangle(a,b,fill=c)
	drawFleche(cnv)
	root.title("basique")
	root.mainloop()

show()
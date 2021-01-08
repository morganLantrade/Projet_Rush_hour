from tkinter import*
import random

##CONSTANTES
SIZE=900 #modifiable


WIDTH=SIZE
BOARD2=WIDTH/9
BOARD=BOARD2/3
HEIGHT=(WIDTH-BOARD2*2)*6/7+(BOARD)*2
COLORS=["white","red","yellow","blue"]



def remplirGrid(col,player):
	i=5
	while grid[i][col]!=0 and i>=0:
		i-=1
	if (i!=-1):
		grid[i][col]=player

def coordGrid(coinSup,coinInf):
	def coordIntoOval(i,j):
		A=(a1,a2) =(coinSup[0]+space//2+j*(diam+space),coinSup[1]+space//2+i*(diam+space)) #coin sup
		B=(a1+diam,a2+diam) #coin inf
		C=COLORS[grid[i][j]] # couleur
		return (A,B,C)
	
	spaceTotal=(coinInf[0]-coinSup[0])//7
	space=spaceTotal/10 #10%
	diam=spaceTotal-space
	return [ coordIntoOval(i,j) for i in range(6) for j in range(7)]
	
def drawGrid(cnv):
	A=(x1,y1)=(0,HEIGHT-BOARD)
	B=(x2,y2)=(WIDTH,HEIGHT)
	cnv.create_rectangle(A,B,fill="blue", outline='') # base
	C=(x3,y3)=(BOARD2,BOARD)
	D=(x4,y4)=(WIDTH-BOARD2,HEIGHT-BOARD)
	cnv.create_rectangle(C,D,fill="blue", outline='') # grid
	#jetons
	for a,b,c in coordGrid(C,D):
		cnv.create_oval(a,b,fill=c) 

def show():
	root=Tk()
	root.title("Puissance 4")
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
	cnv.pack()
	drawGrid(cnv)
	root.mainloop()

grid=[[0]*7 for _ in range(6)]
remplirGrid(4,1)
remplirGrid(4,2)
remplirGrid(4,1)
remplirGrid(5,2)
show()
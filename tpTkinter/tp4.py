from tkinter import *

SIZE=(HEIGHT,WIDTH)=(500,500)
CENTER=(WIDTH//2,HEIGHT//2)
BOARD=WIDTH//16
DIAM=WIDTH-BOARD*2
COLORS=["light grey","DarkOrange4","black"]
DIAM2=BOARD

def filter(i,j):
	return (i<3 and 4>=j>=2) or (2<=i<=4 and j<3) or (i>3 and 4>=j>=2) or (2<=i<=4 and j>3)
def grid():
	coord=[ (i,j) for i in range(7) for j in range(7) if filter(i,j)]
	spaceTotal=(CENTER[0]+DIAM2//2-BOARD)//4
	spaceBetween=spaceTotal-DIAM2
	return [ (BOARD+spaceBetween+(i*spaceTotal),(BOARD+spaceBetween+(j*spaceTotal))) for (i,j) in coord]
	

def drawGrid(canvas):
	circles= [ ((a,b),(a+DIAM2,b+DIAM2),COLORS[2]) for (a,b) in grid()]
	for a,b,c in circles:
		canvas.create_oval(a,b,fill=c ,outline=c)

def drawPlateau(canvas):
	A=(x,y)=(BOARD,BOARD)
	B=(x+DIAM,y+DIAM)
	canvas.create_oval(A,B,fill=COLORS[1],outline=COLORS[1])

def drawCenter(canvas):
	(x,y)=CENTER
	A=(a,b)=(x-DIAM2/2,y-DIAM2/2)
	B=(a+DIAM2,b+DIAM2)
	canvas.create_oval(A,B,fill=COLORS[0],outline=COLORS[0])

def show():
	root=Tk()
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
	cnv.pack(side="left",padx=0,pady=0)
	root.title("Jeu du solitaire")
	drawPlateau(cnv)
	drawCenter(cnv)
	drawGrid(cnv)
	root.mainloop()

show()
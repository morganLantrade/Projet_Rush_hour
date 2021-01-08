from tkinter import *
from math import cos,sin,pi

SIZE=WIDTH=HEIGHT=500

O=(Ox,Oy)=(WIDTH/2,HEIGHT/2)
BOARD=SIZE/10
D=SIZE-2*BOARD
R=D/2


def showCircleN(canvas,n,table):
	points ={ k : ( Ox+R*cos((2*pi*k)/n),Oy+R*sin((2*pi*k)/n)) for k in range(n) }
	for key,(x,y) in points.items():
		canvas.create_oval((x-1,y-1),(x+1,y+1),fill='black', outline='black')
		canvas.create_line((x,y),points[key*table%n])





def show(n,table):
	root=Tk()
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
	cnv.pack()
	showCircleN(cnv,n,table)
	root.title(f'Table Micmaths table de {table} avec {n} sommets')
	root.geometry('900x500')
	root.mainloop()

show(200,4)
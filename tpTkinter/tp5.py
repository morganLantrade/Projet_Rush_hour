from tkinter import *

WIDTH=500
HEIGHT=500
LONGUEUR=35
LesPoints=[ (10,50),(436,235),(245,45),(324,324),(86,487)]


Origin=(250,250)

def distance(A,B):
	return ((A[0]-B[0])**2+(A[1]-B[1])**2)**0.5


def origin(B,C,L):
	(Bx,By) = B
	(Cx,Cy) = C
	vecteur= (vx,vy)= (Bx-Cx,By-Cy)
	return (Bx+vx/(distance(B,C)/L),By+vy/(distance(B,C)/L))
		
def shot(B,C,L):
	(Bx,By) = B
	(Cx,Cy) = C
	cnv.create_line(B,C,width=1,fill="green2",dash=(4,4))
	cnv.create_line(B,origin(B,C,L),fill="green2",width=7,arrow='first')

def motion(event):
	x,y=event.x,event.y
	Origin=(x,y)
	cnv.delete('all')
	for B in LesPoints:
		shot(B,Origin,LONGUEUR)




root=Tk()
cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="grey")
cnv.pack(side="left",padx=0,pady=0)
root.title("animation")
root.bind('<Motion>',motion)
root.mainloop()


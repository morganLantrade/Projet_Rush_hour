from tkinter import *

n=120 #taille case

def fillGrid(canvas,nb):
	def coordIntoCase(i,j):
		A=(a1,a2)= (j*n,i*n)
		B=(a1+n,a2+n)
		C=(i*nb)+j+1
		return (A,B,C)
	rects= [ coordIntoCase(i,j) for i in range(nb) for j in range(nb)]
	
	for a,b,c in rects:
		canvas.create_rectangle(a,b,fill="light grey" if c!=nb**2 else "ivory") 
		if c!=nb**2:
			canvas.create_text(a[0]+n//2,a[1]+n//2,text=str(c),font=('arial',n//3,'bold'))




def show(nb):
	root=Tk()
	cnv=Canvas(root,width=n*nb,height=n*nb,background="ivory")
	cnv.pack()
	fillGrid(cnv,nb)
	root.mainloop()

show(6)
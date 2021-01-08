from tkinter import *

WIDTH=500
HEIGHT=500
BOARD=5
COLORS=[]









def show():
	root=Tk()
	cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory",
		highlightbackground="green",
		highlightthickness=BOARD)

	cnv.pack(side="left",padx=0,pady=0)
	root.title("basique")
	root.mainloop()

show()
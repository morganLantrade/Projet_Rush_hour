from tkinter import * 
from PIL import Image, ImageTk


def show_frame(frame):
    frame.tkraise()
    
fenetre = Tk()
fenetre.state('zoomed')
fenetre.title("CANDY RUSH HOUR")

image = Image.open(r"C:\Users\Utilisateur\Desktop\PROJET PYTHON 2021\oui.jpg")
photo = ImageTk.PhotoImage(image.resize((196, 196), Image.ANTIALIAS))

fenetre.rowconfigure(0, weight=1)
fenetre.columnconfigure(0, weight=1)

frame1 = Frame(fenetre)
frame2 = Frame(fenetre)

for frame in (frame1, frame2):
    frame.grid(row=0,column=0,sticky='nsew')
#==================Menu 1 : Acceuil
frame1_title=  Label(frame1, text='CANDY RUSH HOUR', font='times 35', bg='#8c7b98')
frame1_title.pack(fill='both', expand=True)

frame1_btn = Button(frame1, text='Enter',command=lambda:show_frame(frame2))
frame1_btn.pack(fill='x', ipady=16)

#==================Menu 2 : Les règles 
#frame2_title=  Label(frame2, image=test, bg='yellow')
# #frame2_title.pack(fill='both',expand=True)

label = Label(frame2, image=photo, bg='yellow')
label.image = photo
label.pack(anchor='n')

frame2_btn = Button(frame2, text='Enter',command=lambda:show_frame(frame1))
frame2_btn.pack(fill='x',ipady=20)


fenetre.mainloop()
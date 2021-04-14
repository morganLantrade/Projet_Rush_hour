from tkinter import * 
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()
pygame.mixer.music.load("musique.mp3") 

def lancer_musique():
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1)

def arret_son():
	pygame.mixer.music.stop()

def quitter():
	pygame.quit()
	fenetre.destroy()

def show_frame(frame):
    frame.tkraise()
    
fenetre = Tk()


fenetre.geometry("800x600")
fenetre.title("CANDY RUSH HOUR")

fenetre.protocol("WM_DELETE_WINDOW",quitter)

#Ouverture d'image pour la 
image = Image.open(r"oui.jpg")
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

son1 = Image.open(r"son_on.jpg")
image_son1 = ImageTk.PhotoImage(son1.resize((65, 65), Image.ANTIALIAS))

Button(frame1,image=image_son1,command=lancer_musique,bg="white").pack(pady=10)

Button(frame1,text="Couper",command=arret_son,width=40).pack(pady=10)

#==================Menu 2 : Les règles 
#frame2_title=  Label(frame2, image=test, bg='yellow')
# #frame2_title.pack(fill='both',expand=True)

label = Label(frame2, image=photo, bg='yellow')
label.image = photo
label.pack(anchor='w')

frame2_btn = Button(frame2, text='Enter',command=lambda:show_frame(frame1))
frame2_btn.pack(fill='x',ipady=20)


fenetre.mainloop()
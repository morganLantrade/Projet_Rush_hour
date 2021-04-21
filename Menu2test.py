from tkinter import * 
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()
pygame.mixer.music.load("musique.mp3") 

def lancer_musique():
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play(-1)


etatmusique=0
def Junk_box():
	global etatmusique 
	if etatmusique == 0: 
		pygame.mixer.music.pause()
		b_musique['image'] = image_son1
	else: 
		pygame.mixer.music.unpause()
		b_musique['image'] = image_son2
	etatmusique = 2-etatmusique

"""def change_i():
    if b_musique['image'] == image_son1:
        #start_recording()

        b_musique.config(image=image_son2)
        b_musique['image'] = image_son2
    else:
        #stop_recording()

        b_musique.config(image=image_son1)
        b_musique['image'] = image_son1
"""

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
frame3= Frame(fenetre)

for frame in (frame1,frame2,frame3):
    frame.grid(row=0,column=0,sticky='nsew')



#==================Menu 1 : Acceuil

#frame1.configure(background='systemTransparent')

frame1_title=  Label(frame1, text='VROUM, THE GAME', font='times 35')
frame1_title.pack(fill='both', expand=False)


#Bouton Règles (Frame 2)->
REGLES = Image.open(r"REGLES.png")
image_REGLES = ImageTk.PhotoImage(REGLES, Image.ANTIALIAS)

frame1_btn = Button(frame1, image=image_REGLES,command=lambda:show_frame(frame2),borderwidth=0)
frame1_btn.pack(pady=14)

#Bouton de la gestion du son ->
son_ON = Image.open(r"SON ON.png")
image_son1 = ImageTk.PhotoImage(son_ON.resize((40,40), Image.ANTIALIAS))

son_OFF = Image.open(r"SON OFF.png")
image_son2 = ImageTk.PhotoImage(son_OFF.resize((40, 40), Image.ANTIALIAS))

b_musique=Button(frame1,image=image_son2,command=Junk_box,borderwidth=0)
b_musique.place(x=750,y=5)

#Bouton pour accéder au choix de difficulté (Frame 3)-> 
JOUER = Image.open(r"JOUER.png")
image_JOUER = ImageTk.PhotoImage(JOUER, Image.ANTIALIAS)

To_Level = Button(frame1, image=image_JOUER,command=lambda:show_frame(frame3),borderwidth=0)
To_Level.pack(pady=7)

#Bouton pour quitter le jeu :
QUITTER_ = Image.open(r"QUITTER.png")
image_quitter = ImageTk.PhotoImage(QUITTER_, Image.ANTIALIAS)

B_Quitter= Button(frame1, image=image_quitter, command=quitter, borderwidth=0)
B_Quitter.place(x=580,y=540)



#==================Menu 2 : Les règles 
#frame2_title=  Label(frame2, image=test, bg='yellow')
# #frame2_title.pack(fill='both',expand=True)

label = Label(frame2,text="REGLES DU JEU", bg='yellow')
label.pack(anchor='w')

frame2_btn = Button(frame2, text='Retour',command=lambda:show_frame(frame1))
frame2_btn.pack(fill='x',ipady=20)

#==================Menu 3 : Les levels (par difficulté) 
label = Label(frame3,text="Stages par niveau", bg='green')
frame3_btn = Button(frame3, text='Retour au Menu',command=lambda:show_frame(frame1))
frame3_btn.pack(fill='x',ipady=20)



show_frame(frame1)
lancer_musique()
fenetre.mainloop()
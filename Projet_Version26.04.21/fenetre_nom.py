from tkinter import * 
import pygame
from PIL import Image, ImageTk

#fenetre=Tk()

class FenetreNom():

	def __init__(fenetre): # on peut mettre couleur , theme , taille , ou meme nom des boutons en paramaetre
		self.fenetre=fenetre
		self.fenetre.geometry("800x600")
		self.fenetre.title("CANDY RUSH HOUR")

		
		# ICI tu créer tes boutons , label,frame, canvas ( ne pas oublier les selfs)
		self.frame1=Frame(self.fenetre)
		self.frame1_title=Label(self.root, text='VROUM, THE GAME', font='times 35')
		self.frame1_title.pack(fill='both', expand=False)
		

		self.bouton_test= None #
		#Button(self.frame1,command= self.test_bouton) Ici tu as besoin d'une image par exemple





		#DICTIONNAIRES IMAGES QUE TU INITIALISERA AVEC LOARD_IMAGES
		self.images={}
		
		# pour les events
		self.fenetre.bind('<Button-1>',self.selection)

     
#############################################################################################################################
#############################################################################################################################
#####                    EVENT HANDLERS                                                                                   ###
#############################################################################################################################
#############################################################################################################################

	def selection(self,event): # si c'est un bind il faut event en plus
		print("tu clic")


	def test_bouton(self):
		pass


	
#############################################################################################################################
#############################################################################################################################
#####                    METHODES LIEES AUX DATA                                                                          ###
#############################################################################################################################
#############################################################################################################################


	def loard_images(self): 
		self.images["nom de l'image que tu veux en clé"] = img
		pass

#############################################################################################################################
#############################################################################################################################
#####                    METHODES DE DRAW                                                                                 ###
#############################################################################################################################
#############################################################################################################################

	def draw(self):
		self.drawBouton_test()

	def drawButon_test(self):
		img=self.images["imageB1"]
		# tu modifie ce que tu veux
		self.bouton1=Boutton(self.fenetre,image=img, command=self.bouton_test )
		self.bouton1.pack()
   
    
#############################################################################################################################
#############################################################################################################################
#####                    METHODES PRINCIPALE DE LA FENETRE                                                                ###
#############################################################################################################################
#############################################################################################################################
        
    '''mainloop de la fenetre Tkinter'''
    def afficher(self):
        self.load_images()
        self.draw()
        self.fenetre.mainloop()
    
    def quitter(self):
        self.fenetre.destroy()
        



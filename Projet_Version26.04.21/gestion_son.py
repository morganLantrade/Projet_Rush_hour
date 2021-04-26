import pygame
import threading

 
class Musique:
    etat_musique=0
    musique=None
    bouton=None
    victoire=None
   
    def __init__(self):
        #  mixer.pre_init( requence , size , channels, buffer) pour eviter du delay dans le programme 
        pygame.mixer.pre_init(44100, -16, 2, 2048)  
        pygame.mixer.init()
        pygame.init()
        Musique.musique=pygame.mixer.Sound("assets/sons/musique.ogg") 
        Musique.bouton=pygame.mixer.Sound("assets/sons/son_bouton.ogg") 
        Musique.victoire=pygame.mixer.Sound("assets/sons/son_victoire.ogg") 
        Musique.victoire.set_volume(0.05)
        Musique.musique.set_volume(0.05)
        Musique.bouton.set_volume(0.05)
        Musique.musique.play(-1,0,8000)

 


    @staticmethod
    def pause():
        pygame.mixer.pause()
        Musique.etat_musique=2

    @staticmethod
    def unpause():
        pygame.mixer.unpause()
        Musique.etat_musique=0

    @staticmethod
    def playBruitage():
         Musique.bouton.play(0)
        

    @staticmethod
    def playVictoire():
        Musique.victoire.play(0)
        
    @staticmethod
    def stop():
        pygame.quit()




import tkinter as tk
from PIL import Image, ImageTk
from gestion_son import Musique
import tkinter.font as tkFont

from partie import Partie 
from vehicule import Vehicule
from fenetre_partie import FenetrePartie



class FenetreMenuPrincipale:
    def __init__(self, root=None,size=(800,600)):
        self.root = root
        self.canvas=tk.Canvas(root,width=800,height=600,borderwidth=0,bg="#f1f2ee")
        self.bg=None
        #Boolean : souris sur tag : indicateur pour modifier la couleur de certains widgets sur le canevas. 
        self.souris_sur_tag=None 

        self.root.title("Rush Before 19 Hour")

        ### CENTRER LA FENETRE AU MILIEU DE L'ECRAN ###
        self.width=800
        self.height=600

        screen_width=root.winfo_screenwidth()
        screen_height=root.winfo_screenheight()
        x= (screen_width/2)-(self.width/2)
        y=(screen_height/2)-(self.height/2)
        self.root.geometry(f'{self.width}x{self.height}+{int(x)}+{int(y)}')
        self.root.minsize(800,600)


        ### GESTION DU SON SUR LA FENETRE : ### 

        #Lancement de la musique au lancement du jeu: 
        Musique()

        son_n_u = Image.open(r"assets/icon son/son0.png")
        son_s_u = Image.open(r"assets/icon son/son0_S.png")
        son_n_p = Image.open(r"assets/icon son/son2.png")
        son_s_p = Image.open(r"assets/icon son/son2_S.png")

        self.son_normal_unpause=ImageTk.PhotoImage(son_n_u.resize((40,40)), Image.ANTIALIAS )
        self.son_selec_unpause=ImageTk.PhotoImage(son_s_u.resize((40,40)), Image.ANTIALIAS )

        self.son_normal_pause=ImageTk.PhotoImage(son_n_p.resize((40,40)), Image.ANTIALIAS )
        self.son_selec_pause=ImageTk.PhotoImage(son_s_p.resize((40,40)), Image.ANTIALIAS )


        def bouton_son(event=None):
            if Musique.etat_musique ==0:
                Musique.pause()
                self.canvas.itemconfig(self.boutton_son,image=self.son_normal_unpause)
            else: 
                Musique.unpause()
                self.canvas.itemconfig(self.boutton_son,image=self.son_normal_pause)

        def bouton_son_focus(event=None):
            if Musique.etat_musique ==0:
                self.canvas.itemconfig(self.boutton_son,image=self.son_selec_pause)
            else:
                self.canvas.itemconfig(self.boutton_son,image=self.son_selec_unpause)



        #### BOUTON "ACCEDER AU NIVEAUX DES NIVEAUX ET DIFFICULTE : Jouer" ##### 
        self.boutton_niveaux=None
        self.image_jouer=None

        JOUER_I = Image.open(r"assets/menu/JOUER.png")
        self.image_jouer = ImageTk.PhotoImage(JOUER_I, Image.ANTIALIAS)

        self.boutton_niveaux=tk.Button(self.canvas, image=self.image_jouer,borderwidth=0, bg="#f1f2ee",command=self.ouvrir_choix_niv)


        #### BOUTON "COMMENT JOUER" ##### 
        self.boutton_regles=None
        self.image_regles=None

        REGLES = Image.open(r"assets/menu/REGLES.png")
        self.image_regles = ImageTk.PhotoImage(REGLES, Image.ANTIALIAS)

        self.boutton_regles=tk.Button(self.canvas, image=self.image_regles,borderwidth=0,bg="#f1f2ee",
                  command=self.ouvrir_regles,cursor="question_arrow")


        ### BOUTON QUITTER LE JEU ###

        self.boutton_quitter=None
        self.root.protocol("WM_DELETE_WINDOW",self.quitter)

        QUITTER_I = Image.open(r"assets/menu/QUITTER.png")
        self.image_quitter = ImageTk.PhotoImage(QUITTER_I, Image.ANTIALIAS)

        self.boutton_quitter=tk.Button(self.canvas, image=self.image_quitter,borderwidth=0,bg="#f1f2ee",activebackground="#f1f2ee", #a2cce7
            command=self.quitter,cursor="X_cursor",state="disable")
        
        #Mise en place du fond sur la fenêtre : 
        self.ouvrir_fond()
        #Creation des boutons sur la fenêtre : 


        self.canvas.create_window(400,300,window=self.boutton_niveaux,anchor="center")
        self.canvas.create_window(400,380,window=self.boutton_regles,anchor="center")
        self.canvas.create_window(400,460,window=self.boutton_quitter,anchor="center")

        #Creation du bouton son interactif :
        self.boutton_son = self.canvas.create_image(760,30,image=self.son_normal_pause,anchor="center")
        self.canvas.tag_bind(self.boutton_son,'<1>', bouton_son)
        self.canvas.tag_bind(self.boutton_son,'<Motion>', bouton_son_focus)

        self.canvas.pack()
        
        #Initialisation de l'icon du jeu sur la fenêtre : (A mettre après la musique et placement de la fenêtre sinon lag)
        self.root.iconphoto(False, tk.PhotoImage(file='assets/icon fenetre/ICON V2_essai.png'))

    def ouvrir_fond(self):
        lien = r"assets/menu bg/menu_principal.png"
        self.bg = ImageTk.PhotoImage(Image.open(lien).resize((800,600),Image.ANTIALIAS))
        self.canvas.create_image(0,0,image=self.bg,anchor="nw")
        

    def aff_menu_principale(self):
        self.canvas.pack()

    def ouvrir_regles(self):
        self.menu_regles = MenuRegles(master=self.root, app=self)
        self.canvas.pack_forget()
        self.menu_regles.lancer_regles()

    def ouvrir_choix_niv(self):
        self.menu_niveaux = MenuNiveaux(master=self.root, app=self)
        self.canvas.pack_forget()
        self.menu_niveaux.lancer_niv()

    def quitter(self):
        self.root.destroy()


###############################################################################################################
#                   CLASSE DE LA PAGE GUIDANT LE JOUEUR SUR LES REGLES ET LES COMMANDES                     #
##############################################################################################################
class MenuRegles:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.canva = tk.Canvas(self.master,borderwidth=0,width=800,height=600)
        self.bg=None



        #### BOUTON RETOUR AU MENU PRINCIPAL ###

        self.boutton_retour=None 
        self.image_retour=None 

        RETOUR= Image.open(r"assets/menu/RETOUR.png")
        self.image_retour= ImageTk.PhotoImage(RETOUR, Image.ANTIALIAS)
        self.boutton_retour=tk.Button(self.master, image=self.image_retour, borderwidth=0, command=self.retour_menu,activebackground="#f1f2ee")


        self.ReglesTxt=tk.Label(self.master, text="Ici il y a des règles, blabla sortez la voiture jaune du parking",bg="#f1f2e2")
        self.canva.create_window(350,400,window=self.ReglesTxt,anchor="center")


        self.background()

        self.canva.create_window(400,500,window=self.boutton_retour,anchor="center")
        self.canva.pack()


    def background(self):
        lien = r"assets/menu bg/bg_regles.png"
        self.bg = ImageTk.PhotoImage(Image.open(lien).resize((800,600),Image.ANTIALIAS))
        self.canva.create_image(0,0,image=self.bg,anchor="nw")


    def lancer_regles(self):
        self.canva.pack()

    def retour_menu(self):
        self.canva.pack_forget()
        self.app.aff_menu_principale()



###############################################################################################################
#                   CLASSE DE LA PAGE DE CHOIX DES NIVEAUX ET DIFFICULTE DU JEU                             #
##############################################################################################################
class MenuNiveaux:
    def __init__(self, master=None, app=None):
        self.master = master
        self.app = app
        self.canva = tk.Canvas(self.master,borderwidth=0,width=800,height=600)
        self.bg=None

        ## Importation des images de flèches de sélections de niveaux : ### 
        fleche_gaucheN=Image.open(r"assets/icon fleche/fleche0.png")
        fleche_gaucheS=Image.open(r"assets/icon fleche/fleche0_S.png")
        fleche_gaucheD=Image.open(r"assets/icon fleche/fleche0_D.png")

        fleche_droiteN=Image.open(r"assets/icon fleche/fleche2.png")
        fleche_droiteS=Image.open(r"assets/icon fleche/fleche2_S.png")
        fleche_droiteD=Image.open(r"assets/icon fleche/fleche2_D.png")

        self.image_gaucheN=ImageTk.PhotoImage(fleche_gaucheN.resize((40,40)),Image.ANTIALIAS)
        self.image_gaucheS=ImageTk.PhotoImage(fleche_gaucheD.resize((40,40)),Image.ANTIALIAS)
        self.image_gaucheD=ImageTk.PhotoImage(fleche_gaucheD.resize((40,40)),Image.ANTIALIAS)

        self.image_droiteN=ImageTk.PhotoImage(fleche_droiteN.resize((40,40)),Image.ANTIALIAS)
        self.image_droiteS=ImageTk.PhotoImage(fleche_droiteD.resize((40,40)),Image.ANTIALIAS)
        self.image_droiteD=ImageTk.PhotoImage(fleche_droiteD.resize((40,40)),Image.ANTIALIAS)



        ### BOUTON DE CHOIX DE DIFFICULTE ###

        self.aff_difficulte=tk.Label(self.master,text="Facile",bg="#f1f2ee")
    

        def bouton_diff_av(event=None):
            if(self.aff_difficulte['text']=="Normal"):
                self.aff_difficulte['text']="Facile"

            elif(self.aff_difficulte['text']=="Difficile"):
                self.aff_difficulte['text']="Normal"



        def bouton_diff_arr(event=None):
            if(self.aff_difficulte['text']=="Normal"):
                self.aff_difficulte['text']="Difficile"

            elif(self.aff_difficulte['text']=="Facile"):
                self.aff_difficulte['text']="Normal"

        #Faire les versions selectionnées : 


        ### BOUTONS DE SELECTION DE NIVEAUX ###
        """
        Niveaux=[1,2,3,4,5,6,7,8,9]
        cpt=0
        row1=0
        row2=0
        row3=0

        for niveau in Niveaux: 
            if cpt<3:
                 boutton=tk.Button(self.master,text=niveau,width=3,height=2, bg="#A2CCE7",activebackground="#A2CFFF",bd=1)
                 boutton.config(command= lambda: self.load_niveau(niveau))
                 #self.canva.create_window(345+row1*50,330,window=boutton,anchor="center")
                 row1+=1
            elif cpt >= 3 and cpt < 6:
                 boutton=tk.Button(self.master,text=niveau,width=3,height=2, bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(niveau)) 
                 #self.canva.create_window(345+row2*50,400,window=boutton,anchor="center")
                 row2+=1
            else:
                 boutton=tk.Button(self.master,text=niveau,width=3,height=2, bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(niveau))
                 #self.canva.create_window(345+row3*50,470,window=boutton,anchor="center")
                 row3+=1
            cpt+=1

        """

        niveau_un=tk.Button(self.master,text="1",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(1))
        self.canva.create_window(345,330,window=niveau_un,anchor="center")

        niveau_deux=tk.Button(self.master,text="2",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(2))
        self.canva.create_window(395,330,window=niveau_deux,anchor="center")

        niveau_trois=tk.Button(self.master,text="3",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(3))
        self.canva.create_window(445,330,window=niveau_trois,anchor="center")

        niveau_quatre=tk.Button(self.master,text="4",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(4))
        self.canva.create_window(345,400,window=niveau_quatre,anchor="center")

        niveau_cinq=tk.Button(self.master,text="5",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(5))
        self.canva.create_window(395,400,window=niveau_cinq,anchor="center")

        niveau_six=tk.Button(self.master,text="6",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(6))
        self.canva.create_window(445,400,window=niveau_six,anchor="center")

        niveau_sept=tk.Button(self.master,text="7",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(7))
        self.canva.create_window(345,470,window=niveau_sept,anchor="center")

        niveau_huit=tk.Button(self.master,text="8",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(8))
        self.canva.create_window(395,470,window=niveau_huit,anchor="center") 

        niveau_neuf=tk.Button(self.master,text="9",widt=3, height=2,  bg="#A2CCE7",activebackground="#A2CFFF",bd=1,command= lambda: self.load_niveau(9))
        self.canva.create_window(445,470,window=niveau_neuf,anchor="center")   


        #### BOUTON RETOUR AU MENU PRINCIPAL ###

        self.boutton_retour=None 
        self.image_retour=None 

        RETOUR= Image.open(r"assets/menu/RETOUR.png")
        self.image_retour= ImageTk.PhotoImage(RETOUR, Image.ANTIALIAS)
        self.boutton_retour=tk.Button(self.master, image=self.image_retour, borderwidth=0, command=self.retour_menu,activebackground="#A2CCE7",bg="#A2CCE7")


        self.background()

        #Creation des boutons interactifs # 

        self.canva.create_window(670,550,window=self.boutton_retour,anchor="center")

        self.canva.create_window(395,250,window=self.aff_difficulte,anchor="center")

        self.boutton_avant = self.canva.create_image(320,250,image=self.image_gaucheN,anchor="center")
        self.canva.tag_bind(self.boutton_avant,'<1>', bouton_diff_av)
        #self.canvas.tag_bind(self.boutton_avant,'<Motion>', bouton_son_focus)

        self.boutton_arr = self.canva.create_image(470,250,image=self.image_droiteN,anchor="center")
        self.canva.tag_bind(self.boutton_arr,'<1>', bouton_diff_arr)
        #self.canvas.tag_bind(self.boutton_avant,'<Motion>', bouton_son_focus)



        self.canva.pack()

    def load_niveau(self,niveau):
        if(self.aff_difficulte['text']=="Normal"):
            level=8+niveau
        elif(self.aff_difficulte['text']=="Difficile"):
            level=17+niveau 
        else: 
            level=niveau-1

        self.canva.pack_forget()
        premierePartie=FenetrePartie(level,self.master)
        premierePartie.afficher()

        #laPremierePartie=FenetrePartie(niveau,self.master)
        #laPremierePartie.afficher()


    def background(self):
        lien = r"assets/menu bg/choix_diff.png"
        self.bcg = ImageTk.PhotoImage(Image.open(lien).resize((800,600),Image.ANTIALIAS))
        self.canva.create_image(0,0,image=self.bcg,anchor="nw")


    def lancer_niv(self):
        self.canva.pack()

    def retour_menu(self):
        self.canva.pack_forget()
        self.app.aff_menu_principale()




if __name__ == '__main__':
    root = tk.Tk()
    app = FenetreMenuPrincipale(root)
    root.mainloop()
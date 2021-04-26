from tkinter import *
from module_partie import Partie,Deplacement
from module_vehicule import Vehicule
from PIL import Image,ImageTk
from timeit import default_timer
from gestion_son import Musique
import tkinter.font as font



couleur1='172a78'








class FenetrePartie(Partie):
    ''' La classe FenetrePartie  hérite de la classe Partie et représente
    graphiquement le plateau de jeu en lancant une fenetre Tkinter 
    Elle sera capable de gérer les évènements.

        Nouveaux attributs :

        List(Vehicule) ou int[6][6]  copie : permet de recommencer une partie
        int selected : représente l'id du véhicule selectionné ( par la souris ) 
        (int,int) vecteur_deplacement 
        (int,int) clic_origine 
        (int,int) coord_selected 
        { vehicule.id : Image } images des véhicules
        boolean souris_sur_tag : permet de modifier la couleur de certain widgets du canevas
        boolean pause
        boolean redimensionnee
        float : chrono = timer actuel
        float : debut = timer début partie
        float : timer_pause= timer mémorisation de la pause
        int nb_voiture : permet de choisir parmis les différentes voitures proposées dans le fichier
        int nb_camion : permet de choisir parmis les différents camions proposés dans le fichier
        int : width :largeur canevas
        int : height :height hauteur canevas
        int : bord_x :taille du bord en largeur
        int : bord_y :taille du bord en hauteur
        int : case :taille d'une case


    '''
    
        
    def __init__(self,vehicules,master,size=(800,600)):
        super().__init__(vehicules)
        self.vecteur_deplacement=(0,0)
        self.clic_origine=(0,0)
        self.coord_selected=(0,0)
        self.selected=None
        self.souris_sur_tag=None
        
        self.pause=True
        #DICTIONNAIRES D'IMAGES,DE SONS et de BOUTONS(fonctions)
        self.images={}
        self.boutons= { 'bouton_son' : self.bouton_son , 'bouton_reglage' : self.bouton_reglage ,
                      'bouton_recommencer' : self.bouton_recommencer, 'bouton_indice':self.bouton_indice,
                      'bouton_fleche_av': self.bouton_fleche_av , 'bouton_fleche_ar' : self.bouton_fleche_ar,
                      'bouton_aled' : self.bouton_aled}
        self.nb_voitures=4
        self.nb_camions=3
        
        # TIMER
        self.chrono=0
        self.debut=default_timer()
        self.timer_pause=0 
                
        ## DIMENSIONS FENETRE
        self.width=size[0]
        self.height=size[1]
        self.bord_x=self.width//20
        self.bord_y=self.height//40
        self.case=int(self.width//8.4)       
        self.redimensionnee=False
        
        #LANCER FENETRE ET LIER SES EVENTS
        self.root=master
        self.canvas=Canvas(self.root,width=self.width,height=self.height,bg="#f3dac3")
        self.canvas.pack(side="top",padx=0,pady=0)
        self.root.bind('<Button-1>',self.selection)
        self.root.bind('<B1-Motion>',self.updateDeplacement)
        self.root.bind('<ButtonRelease-1>',self.unselect)
        self.root.bind('<Motion>' , self.souris_sur )
        self.root.bind('<Configure>',self.resize)
        self.root.bind('<Key>',self.pressed)
        self.root.title("Rush Hour")
        self.root.geometry(f'{self.width}x{self.height}+{self.root.winfo_screenwidth()//2-self.width//2}+{self.root.winfo_screenheight()//2-self.height//2}')
        self.root.minsize(400,300)


        
        self.les_fonts=list(font.families())
        self.font_num=self.les_fonts.index('Segoe UI Light')
        self.la_font=self.les_fonts[self.font_num]

        
        
     
        
        
        


   

        
    #############################################################################################################################
    #############################################################################################################################
    #####                    EVENT HANDLERS                                                                                   ###
    #############################################################################################################################
    #############################################################################################################################
   

    def bouton_son(self):
        if  Musique.etat_musique == 0: 
            Musique.pause()
        else: 
            Musique.unpause()



    def bouton_indice(self):
        print("Indice")
        
    def bouton_aled(self):
        print("A l'aide !")
    
    def bouton_recommencer(self):
        self.recommencer()
        self.debut+=self.timer_pause
        self.timer_pause=self.chrono
        self.chrono=0
        

    
    def bouton_reglage(self):
        print("Reglage")
    
    def bouton_fleche_av(self):
        if len(self.pile_deplacements_retour)>0:
            self.retour_avant()
            self.draw()
    def bouton_fleche_ar(self):
        if len(self.pile_deplacements)>0:
            self.retour_arriere()
            self.draw()
        
        
    
        



    def selection(self,event):
        ''' si le click est dans la grille on met a jour l'id selected
        on met a jour clic_origine
        et on redessin car la couleur du vehicule selected change '''
        tag=self.canvas.find_closest(event.x,event.y)
        leTag=self.lireTag(tag)
        if len(leTag)>0:
            #Cas d'un vehicule selectionné
            if leTag[0]=="V" and not self.pause and not self.est_gagnee:
                self.clic_origine=(event.x,event.y)
                self.vecteur_deplacement=(0,0)
                v=self.vehicules[int(leTag[1:])]
                self.selected=v.id
                self.coord_selected=v.coord
            if leTag in self.boutons:
                if (leTag!='bouton_fleche_ar' and leTag!='bouton_fleche_av'):
                    Musique.playBruitage() 
                    self.boutons[leTag]()
                elif not(self.pause) and (leTag=="bouton_fleche_ar" and self.pile_deplacements or leTag=="bouton_fleche_av" and self.pile_deplacements_retour ):
                    Musique.playBruitage() 
                    self.boutons[leTag]()

            ##on appelle la fonction selectionnee
            self.draw()

    
    def updateDeplacement(self,event):
        ''' lorsque la souris bouge avec le click  gauche activé :
            on met a jour le vecteur_deplacement
            et on redessine'''
        
        self.vecteur_deplacement=(event.x-self.clic_origine[0],event.y-self.clic_origine[1])
        self.draw()
        

    def unselect(self,event):
        '''lorsqu'on lache le click gauche de la souris :
                -on remet les attributs par defauts:
                vecteur_deplacement,selected
 
                -on met a jour la matrice selon le mouvement effectué

                -on incrémente Deplacement
        '''
        if self.selected and self.coord_selected!=self.vehicules[self.selected].coord :
            self.updatePartie(self.vehicules[self.selected],self.coord_selected)
            self.est_gagnee=self.estGagnee()
            if self.est_gagnee:
                Musique.playVictoire()
            self.pile_deplacements_retour=[]
            
        self.vecteur_deplacement=(0,0)
        self.selected=None
        self.draw()



    
    
    def resize(self,event):
        '''redimensionne le canvas par rapport a la fenetre met en mode pause'''
        #On passe on en mode pause mais on redimensionne exepté pour le début de la partie.
        if event.width!=self.width :
            self.pause=True
            self.redimensionnee=True
            W=self.root.winfo_width()
            H=self.root.winfo_height()
            self.width=W
            self.height=int(W*3/4)
            if self.height>H:
                self.height=H
                self.width=int(self.height*4/3)
            # on redimensionne
            self.canvas.config(width=self.width,height=self.height)
            self.bord_x=self.width//20
            self.bord_y=self.height//40
            self.case=int(self.width//8.4)
            self.draw()



    
    def souris_sur(self,event):
        '''modifie les couleurs des widgets selon la position de la souris'''
        if self.redimensionnee:
            self.redimensionner()
        tag=self.canvas.find_closest(event.x,event.y)
        leTag=self.lireTag(tag)
        if len(leTag)>0:
            self.souris_sur_tag=leTag
        else:
            self.souris_sur_tag=None
        self.draw()

    def pressed(self,event):
        '''modifie la variable self.pause si on appuie sur la touche espace'''
        if event.char == ' 'and not self.redimensionnee and not self.est_gagnee:
            self.pause=not self.pause
            self.draw()
            self.root.after(100) # anti spam

        if event.char=='a':
            self.font_num+=1 if self.font_num < len(self.les_fonts) else 0
            self.la_font=self.les_fonts[self.font_num]
            print(self.la_font)
        if event.char=='e':
            self.font_num-=1 if self.font_num >0 else 0
            self.la_font=self.les_fonts[self.font_num]
            print(self.la_font)

        
    
   
    def update_chrono(self):
        '''timer calculé en fonction du début de la partie et des pauses et eventuels reset''' 
        
        if not self.est_gagnee and not(self.pause):
            now=self.chrono=default_timer()-self.timer_pause-self.debut
        else:
            self.timer_pause=default_timer()-self.chrono-self.debut
        self.draw()
        self.root.after(10,self.update_chrono)

    
    def redimensionner(self):
        '''redimensionne la fenetre et toutes ses dimensions et recharge les images '''
        self.redimensionnee=False
        
        self.update_chrono()
        W=self.root.winfo_width()
        H=self.root.winfo_height()
        self.width=W
        self.height=int(W*3/4)
        if self.height>H:
            self.height=H
            self.width=int(self.height*4/3)
        # on redimensionne
        self.canvas.config(width=self.width,height=self.height)
        self.bord_x=self.width//20
        self.bord_y=self.height//40
        self.case=int(self.width/8.4)
        self.load_images_Vehicules()
        self.load_images_Menu()
        
        self.draw()
    
    def lireTag(self,id_tag):
        '''retourne le tag de l' id_tag_ sur le canvas'''
        return self.canvas.itemconfig(id_tag)['tags'][-1][:-8]


    #############################################################################################################################
    #############################################################################################################################
    #####                    METHODES LIEES AUX COORDONNEES VEHICULE ET PLATEAU                                               ###
    #############################################################################################################################
    #############################################################################################################################
    
    def coordFrame_coordMatrice(self,x,y):
        ''' retourne les coordonnées (i,j) de la matrice selon les coordonnées
        (x,y) de la fenetre  '''
        (i,j)=((y-self.bord_y)//self.case,(x-self.bord_x)//self.case)
        return (i,j)

        
        
    #return le coin sup gauche,inf droit et couleur du rectangle representant la voiture
    def vehiculeIntoRect(self,vehicule):
        ''' Retourne selon les coordonnées du vehicule dans la matrice et la taille self.case:
        A : les coordonnées du coin sup gauche dans la fenetre
        B : les coordonnées du in droit dans la fenetre  
                
        Pour ensuite créer le rectangle dans le canvas '''      
        (y,x)=vehicule.coord
        (xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
        (x,y)=(self.bord_x+x*self.case,self.bord_y+y*self.case)   
        return (x,y)
    
    #########################
    #TO DO 
    #Deplacer les rectangles au lieu de clear canvas et redessiner par desssus
    #########################
    def selectedIntoRect(self):
        ''' Retourne les nouvelles coordonnées du véhicule selectionné selon le mouvement de la souris
        et gère les collisions '''
        vehicule=self.vehicules[self.selected]
        (aX,aY)= self.vehiculeIntoRect(vehicule)
        vX,vY=self.vecteur_deplacement
        possible_deplacement=self.vehiculePossibleDeplacement(vehicule)
        if vehicule.orientation=="V":
            try_deplacement=self.coordFrame_coordMatrice(aX,aY+vY)  # coord du mouvement d'arrivée dans la matrice
            if try_deplacement in possible_deplacement :
                aY+=vY
            elif possible_deplacement: 
                
                # prend le min ou le max des Deplacements possibles comme collision
                aY=self.bord_y+self.case*(max(possible_deplacement)[0]+1 if vY>=0 else min(possible_deplacement)[0]) 
                
        else:
            try_deplacement=self.coordFrame_coordMatrice(aX+vX,aY)  # coord du mouvement d'arrivée dans la matrice
            if try_deplacement in possible_deplacement:
                aX+=vX
            elif possible_deplacement:
                # prend le min ou le max des Deplacements possibles comme collision
                aX=self.bord_x+self.case*(max(possible_deplacement)[1]+1 if vX>=0 else min(possible_deplacement)[1])
                
        #determine les coordonnées de la matrice pour lesquelles l'arriere du Vehicule est le plus proche
        self.coord_selected=( (aY-self.bord_y)//self.case + int((aY-self.bord_y)%self.case>self.case/2),(aX-self.bord_x)//self.case+int((aX-self.bord_x)%self.case>self.case/2))
        
        return (aX,aY)


    #############################################################################################################################
    #############################################################################################################################
    #####                    METHODES LIEES AUX DATA                                                                          ###
    #############################################################################################################################
    #############################################################################################################################
    
    

    
    def load_images_Vehicules(self):
        '''Met a jour le dictionnaire d'images'''
        version_voiture=0
        version_camion=0
        for id in self.vehicules.keys():
            v=self.vehicules[id]
            width= self.case if v.orientation=="V" else self.case*v.lg
            height=self.case if v.orientation=="H" else self.case*v.lg
            
            if id!=1:
                #Image selon la type de vehicule
                img=Image.open(f'assets/vehicules/{v.orientation}{v.lg} N{1+(version_voiture if v.lg==2 else version_camion)}.png')
                img=img.resize((width,height))
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                self.images[str(id)]=img
                #sa version selectionnée
                img=Image.open(f'assets/vehicules/{v.orientation}{v.lg}S N{1+(version_voiture if v.lg==2 else version_camion)}.png')
                img=img.resize((width,height))
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                self.images[str(id)+"S"]=img
                version_voiture=(version_voiture+int(v.lg==2))%self.nb_voitures
                version_camion=(version_camion+int(v.lg==3))%self.nb_camions
                
            elif id==1 :
                #Image vehicule principal
                img=Image.open(f'assets/vehicules/P2.png')
                img=img.resize((width,height))
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                self.images[str(id)]=img
                 #sa version selectionnée
                img=Image.open(f'assets/vehicules/P2S.png')
                img=img.resize((self.case*2,self.case))
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                self.images[str(id)+"S"]=img
        
    '''met a jour le dictionnaire d'images'''
    def load_images_Menu(self):
        def load_image(file,size):
            img=Image.open(file)
            img=img.resize((size[0],size[1]))
            img=ImageTk.PhotoImage(img.convert("RGBA"),Image.ANTIALIAS)
            nom_image=file.split('/')[-1][:-4]
            self.images[nom_image]=img

            img=Image.open(file[:-4]+'_S'+file[-4:])
            img=img.resize((int(size[0]*1.03),int(size[1]*1.03)))
            img=ImageTk.PhotoImage(img.convert("RGBA"),Image.ANTIALIAS)
            self.images[nom_image+'_S']=img

        taille_icone=(self.width//15,self.height//12)
        taille_bouton=(self.width//6,self.height//11)
        
        load_image('assets/icon son/son0.png',taille_icone)
        load_image('assets/icon son/son2.png',taille_icone)
        load_image('assets/icon reglage/reg.png',taille_icone)
        load_image('assets/icon fleche/fleche0.png',taille_icone)
        load_image('assets/icon fleche/fleche2.png',taille_icone)
        load_image('assets/menu/recommencer.png',taille_bouton)
        load_image('assets/menu/indice.png',taille_bouton)
        load_image('assets/menu/aled.png',taille_bouton)


        img=Image.open('assets/icon fleche/fleche0_D.png')
        img=img.resize(taille_icone)
        img=ImageTk.PhotoImage(img.convert("RGBA"),Image.ANTIALIAS)
        self.images['fleche0_D']=img

        img=Image.open('assets/icon fleche/fleche2_D.png')
        img=img.resize(taille_icone)
        img=ImageTk.PhotoImage(img.convert("RGBA"),Image.ANTIALIAS)
        self.images['fleche2_D']=img
    


    #############################################################################################################################
    #############################################################################################################################
    #####                    METHODES DE DRAW                                                                                 ###
    #############################################################################################################################
    #############################################################################################################################
    

    def draw(self):
        self.canvas.delete("all")
        self.drawGrille()
        self.drawInfo()
        if not(self.redimensionnee):
            
            self.drawVehicules()
            self.drawMenu()
            
    def drawVehicules(self):
        '''recupere les positions des images et  les affiche'''
        
        for vehicule in self.vehicules.values():
            if self.selected and vehicule.id==self.selected and self.vecteur_deplacement!=(0,0) :
                (x,y)=self.selectedIntoRect()
            else:
                (x,y)= self.vehiculeIntoRect(vehicule) 
            
            self.canvas.create_image(x,y,image=self.images[str(vehicule.id)+("S" if self.selected and vehicule.id==self.selected else "")],anchor="nw",tags=f'V{vehicule.id}')
    

    def drawGrille(self):
        def coordIntoRect(i,j):
            '''retourne le coin sup gauche et inf droit d'une self.case de coordonnée (i,j) de la matrice'''
            (x,y)=(self.bord_x+j*self.case,self.bord_y+i*self.case)
            if self.pause:
                 color="grey26" if (i+j)%2==0 else "gray20"
            else:
                 color="mint cream" if (i+j)%2==0 else "azure3"
            return ((x,y),(x+self.case,y+self.case),color)
        rects=(coordIntoRect(i,j) for i in range(6) for j in range(6))
        
        for (A,B,C) in rects:
            self.canvas.create_rectangle(A,B,fill=C,outline=C)
         

    

    def drawMenu(self):
              
        def drawSon(x,y):
            surligner= self.souris_sur_tag and self.souris_sur_tag=='bouton_son'
            self.canvas.create_image(x,y,image=self.images[f'son{Musique.etat_musique}'+('' if not(surligner) else '_S')],anchor="nw",tags=f'bouton_son')
            
        def drawReglage(x,y):
            surligner= self.souris_sur_tag and self.souris_sur_tag=='bouton_reglage'
            self.canvas.create_image(x,y,image=self.images[('reg' if not surligner else 'reg_S')],anchor="nw",tags=f'bouton_reglage')
       
        def drawFlecheAvant(x,y):
            surligner= self.souris_sur_tag and self.souris_sur_tag=='bouton_fleche_av'
            disabled= len(self.pile_deplacements_retour)==0 or self.pause
            nom_image= 'fleche2'+('' if not(surligner or disabled) else ('_S' if not(disabled) else '_D'))
            self.canvas.create_image(x,y,image=self.images[nom_image],anchor="nw",tags='bouton_fleche_av')

        def drawFlecheArriere(x,y):
            surligner= self.souris_sur_tag and self.souris_sur_tag=='bouton_fleche_ar'
            disabled= len(self.pile_deplacements)==0 or self.pause
            nom_image= 'fleche0'+('' if not(surligner or disabled) else ('_S' if not(disabled) else '_D'))
            self.canvas.create_image(x,y,image=self.images[nom_image],anchor="nw",tags='bouton_fleche_ar')


        #dimensions locales
        width_menu=1.3*self.case
        height_menu=3*self.case
        bord_x_menu=width_menu/9
        bord_y_menu=height_menu/20
        height_bouton=int(self.case/1.54)-bord_y_menu/2
        x=6*self.case+1.7*self.bord_x+bord_x_menu/2.4
        y=self.bord_y+bord_y_menu/1.3
        #contour    
        self.canvas.create_rectangle(6*self.case+1.7*self.bord_x,self.bord_y,7.5*self.case+1.7*self.bord_x,self.bord_y+3*self.case,fill='#9daab0',outline='#071860'  ,width=self.width//250)
        
        #Objets crées
        recommencer_tag=self.souris_sur_tag and self.souris_sur_tag=='bouton_recommencer'
        self.canvas.create_image(int(x-(0.02*(width_menu-bord_x_menu) if recommencer_tag else 0)),y,image=self.images['recommencer'+('_S' if recommencer_tag else '')],anchor="nw",tags='bouton_recommencer')
        indice_tag=self.souris_sur_tag and self.souris_sur_tag=='bouton_indice'
        self.canvas.create_image(int(x-(0.02*(width_menu-bord_x_menu) if indice_tag else 0)),y+(height_bouton),image=self.images['indice'+('_S' if indice_tag else '')],anchor="nw",tags='bouton_indice')
        aled_tag=self.souris_sur_tag and self.souris_sur_tag=='bouton_aled'
        self.canvas.create_image(int(x-(0.02*(width_menu-bord_x_menu) if aled_tag else 0)),y+2*(height_bouton),image=self.images['aled'+('_S' if aled_tag else '')],anchor="nw",tags='bouton_aled')
        drawSon(x+0.8*bord_x_menu,y+3.1*(height_bouton+bord_y_menu))  #ajustement lié au zones transparentes des images
        drawReglage(x+4.9*bord_x_menu,y+3.05*(height_bouton+bord_y_menu)) # ajustement lié au zones transparentes des images
        drawFlecheAvant(x+5*bord_x_menu,y+3*height_bouton)
        drawFlecheArriere(x+0.9*bord_x_menu,y+3*height_bouton)

        


    def drawInfo(self):
        '''permet d'afficher les 4 éléments et le cadre des info de la partie  '''

        def drawLevel(x,y):
            self.canvas.create_text(x,y,text="Difficulté",font=(self.la_font,self.case//6,'bold'),fill="black")
            self.canvas.create_text(x,y+ecart_texte,text="***",font=(self.la_font,self.case//8,'bold'),fill="black")

        def drawStage(x,y):
            self.canvas.create_text(x,y,text="Niveau",font=(self.la_font,self.case//6,'bold'),fill="black")
            self.canvas.create_text(x,y+ecart_texte,text=str(17),font=(self.la_font,self.case//8,'bold'),fill="black")

        def drawDeplacement(x,y):
            self.canvas.create_text(x,y,text="Déplacements",font=(self.la_font,int(self.case/6.5),'bold'),fill="black")
            self.canvas.create_text(x,y+ecart_texte,text=str(len(self.pile_deplacements)),font=(self.la_font,self.case//8,'bold'),fill="black")

        def drawChrono(x,y):
            self.canvas.create_text(x,y,text="Temps",font=(self.la_font,self.case//6,'bold'),fill="black" )
            self.canvas.create_text(x,y+ecart_texte,text=f'{int(self.chrono//60)} mn {int(self.chrono%60)} s',font=(self.la_font,self.case//8,'bold'),fill="black" )
            
        #dimensions locales
        x=7.45*self.case
        y=self.bord_y+4.18*self.case
        ecart_texte=self.case/4
        ecart_info=self.case/2.1
        #contour
        self.canvas.create_rectangle(6*self.case+1.7*self.bord_x,self.bord_y+4*self.case,7.5*self.case+1.7*self.bord_x,
            self.bord_y+6*self.case,fill="#ffe27d"if not self.estGagnee() else "#63d988",outline='#d49406' ,width=self.width//250)
        #Objets crées
        drawStage(x,y)
        drawLevel(x,y+ecart_info)
        drawDeplacement(x,y+2*ecart_info)
        drawChrono(x,y+3*ecart_info)


    





   
    
#############################################################################################################################
#############################################################################################################################
#####                    METHODES PRINCIPALE DE LA FENETRE                                                                ###
#############################################################################################################################
#############################################################################################################################
        
    '''mainloop de la fenetre Tkinter'''
    def afficher(self):
        self.load_images_Vehicules()
        self.load_images_Menu()
        self.draw()
        self.update_chrono()
        self.root.mainloop()

    

    

from tkinter import *
from module_partie import Partie
from module_vehicule import Vehicule
from PIL import Image,ImageTk

WIDTH=800
HEIGHT=600
BOARD_X=50
BOARD_Y=15
CASE=95





COLORS=["white",'red',"yellow","blue","green","orange",
"purple","grey","light green","salmon","brown","pink","dark green"]



class FenetrePartie(Partie):
    ''' La classe FenetrePartie est hérite de la classe Partie et représente
    graphiquement le plateau de jeu et les différents attributs de la Partie.
    Elle sera capable de gérer les évènements.

    
        Nouveaux attributs :
        int selected : représente l'id du véhicule selectionné ( par la souris ) 
        (int,int) vector_deplacement
        (int,int) origin_click
        (int,int) selected_coord


    '''
    
    def __init__(self,vehicules):
        super().__init__(vehicules)
        self.vector_deplacement=(0,0)
        self.origin_click=(0,0)
        self.selectedCoord=(0,0)
        self.selected=None
        self.bg=None
        
        
        

    
    def coordFrame_coordMatrice(self,x,y):
        ''' retourne les coordonnées (i,j) de la matrice selon les coordonnées
        (x,y) de la fenetre  '''
        (i,j)=((y-BOARD_Y)//CASE,(x-BOARD_X)//CASE)
        return (i,j)

        
        
    #return le coin sup gauche,inf droit et couleur du rectangle representant la voiture
    def vehiculeIntoRect(self,vehicule):
        ''' Retourne selon les coordonnées du vehicule dans la matrice et la taille CASE:
        A : les coordonnées du coin sup gauche dans la fenetre
        B : les coordonnées du in droit dans la fenetre  
                
        Pour ensuite créer le rectangle dans le canvas '''      
        (y,x)=vehicule.coord
        (xD,yD)=Vehicule.DIRECTIONS["Bas" if vehicule.orientation=="V" else "Droite"]
        (x,y)=(BOARD_X+x*CASE,BOARD_Y+y*CASE)   
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
        vX,vY=self.vector_deplacement
        possible_move=self.vehiculePossibleMove(vehicule)
        if vehicule.orientation=="V":
            try_move=self.coordFrame_coordMatrice(aX,aY+vY)  # coord du mouvement d'arrivée dans la matrice
            if try_move in possible_move :
                aY+=vY
            elif possible_move: 
                
                # prend le min ou le max des moves possibles comme collision
                aY=BOARD_Y+CASE*(max(possible_move)[0]+1 if vY>0 else min(possible_move)[0]) 
                
        else:
            try_move=self.coordFrame_coordMatrice(aX+vX,aY)  # coord du mouvement d'arrivée dans la matrice
            if try_move in possible_move:
                aX+=vX
            elif possible_move:
                # prend le min ou le max des moves possibles comme collision
                aX=BOARD_X+CASE*(max(possible_move)[1]+1 if vX>0 else min(possible_move)[1])
                
        #determine les coordonnées de la matrice pour lesquelles l'arriere du Vehicule est le plus proche
        self.selectedCoord=( (aY-BOARD_Y)//CASE + int((aY-BOARD_Y)%CASE>CASE//2),(aX-BOARD_X)//CASE+int((aX-BOARD_X)%CASE>CASE//2))
        
        return (aX,aY)
    

        
    



    def drawVehicules(self,cnv):
        ''' dessine les rectangles representant les véhicules '''
        for v in self.vehicules.values():
            if v.id!=self.selected and v.id!=1:
                img=Image.open(f'assets/litBleu{v.orientation}{v.lg}.png')
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                v.img=img
            elif v.id==1:
                img=Image.open(f'assets/litRouge2.png')
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                v.img=img
            elif self.selected==v.id:
                img=Image.open(f'assets/litVert{v.orientation}{v.lg}.png')
                img =ImageTk.PhotoImage(img.convert("RGBA"))
                v.img=img

        for vehicule in self.vehicules.values():
            if vehicule.id!=self.selected:
                (x,y)= self.vehiculeIntoRect(vehicule)
                cnv.create_image(x,y,image=vehicule.img,anchor="nw")
            else:
                # si on ne veut pas deplacer le vehicule on appelle pas selectedIntoRect mais on change la couleur
                (x,y)=self.selectedIntoRect() if self.vector_deplacement!=(0,0) else self.vehiculeIntoRect(vehicule)
                cnv.create_image(x,y,image=vehicule.img ,anchor="nw")


    
    

    def drawGrille(self,cnv):
        #return sup gauche et in droit d'une case       
        def coordIntoRect(i,j):
            '''retourne le coin sup gauche et inf droit d'une case de coordonnée (i,j) de la matrice'''
            return (BOARD_X+j*CASE,BOARD_Y+i*CASE)
            
        rects= [ (coordIntoRect(i,j),str(self.matrice[i][j])) for i in range(6) for j in range(6)]
        
        for (x,y),c in rects:
            cnv.create_image(BOARD_X,BOARD_Y,image=self.bg,anchor="nw")

    def drawFleche(self,cnv):
        cnv.create_line((7*CASE+CASE//3,BOARD_Y+3*CASE+CASE//2),(8.5*CASE-CASE//2,BOARD_Y+3*CASE+CASE//2),width=CASE//5,arrow='last',fill="green" if self.estGagnee() else "red")

    def drawLevel(self,cnv):
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+4.55*CASE+CASE//6,text="Level",font=('arial',CASE//6,'bold'),fill="black")
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+4.55*CASE+3*CASE//7,text="***",font=('arial',CASE//8,'bold'),fill="black")

    def drawStage(self,cnv):
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+4*CASE+CASE//6,text="Stage",font=('arial',CASE//6,'bold'),fill="black")
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+4*CASE+3*CASE//7,text=str(17),font=('arial',CASE//8,'bold'),fill="black")

    def drawMove(self,cnv):
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+5*CASE+CASE//6,text="Moves",font=('arial',CASE//6,'bold'),fill="black")
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+5*CASE+3*CASE//8,text=str(self.moves),font=('arial',CASE//8,'bold'),fill="black")

    def drawChrono(self,cnv):
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+5.45*CASE+CASE//6,text="Time",font=('arial',CASE//6,'bold'),fill="black" )
        cnv.create_text(7*CASE+CASE//2,BOARD_Y+5.45*CASE+3*CASE//7,text="00:00",font=('arial',CASE//8,'bold'),fill="black" )

    def drawMenu(self,cnv):
        cnv.create_rectangle(6*CASE+1.5*BOARD_X,BOARD_Y,7.5*CASE+1.5*BOARD_X,BOARD_Y+3*CASE)
        width=1.5*CASE-20
        height=CASE//2.15
        x=6*CASE+1.7*BOARD_X
        y=BOARD_Y+10
        board=30
        buttons=[cnv.create_rectangle(x,y+i*height+board*i,x+width,y+(i+1)*height+board*i) for i in range(4)]
        return buttons


    def drawInfo(self,cnv):
        cnv.create_rectangle(6*CASE+1.5*BOARD_X,BOARD_Y+4*CASE,7.5*CASE+1.5*BOARD_X,BOARD_Y+6*CASE)
        self.drawLevel(cnv)
        self.drawStage(cnv)
        self.drawMove(cnv)
        self.drawChrono(cnv)

    def drawVictory(self,cnv):
        cnv.create_text(7*CASE+CASE//2,5*CASE,text="Victory",font=('arial',CASE//8,'bold'),fill="black")
        cnv.create_text(7*CASE+CASE//2,5*CASE+CASE//3,text=str(self.estGagnee()),font=('arial',CASE//8,'bold'),fill="black" )
    

    def drawParking(self,cnv):
        img=Image.open(f'assets/fond_parquet.png')
        img=ImageTk.PhotoImage(img.convert("RGBA"))
        self.bg=img
        cnv.create_image(BOARD_X,BOARD_Y,image=self.bg,anchor='nw')

    def draw(self,cnv):
        cnv.delete("all")
        
        self.drawGrille(cnv)
        self.drawFleche(cnv)
        self.drawInfo(cnv)
        self.drawMenu(cnv)
        self.drawParking(cnv)
        self.drawVehicules(cnv)

    
    def show(self):
        ''' utilitée principale du module_fenetre_partie avec gestion d'events'''

        def selection(event):
            ''' si le click est dans la grille on met a jour l'id selected
                on met a jour origin_click
                et on redessin car la couleur du vehicule selected change '''
            self.origin_click=(event.x,event.y)
            self.vector_deplacement=(0,0)
            (i,j)=self.coordFrame_coordMatrice(event.x,event.y)
            if 0<=i<=5 and 0<=j<=5 and self.matrice[i][j]!=0:
                self.selected= self.matrice[i][j]
                self.selectedCoord=self.vehicules[self.selected].coord
                self.draw(cnv)
            
            
                
            

        def updateMove(event):
            ''' lorsque la souris bouge avec le click  gauche activé :
                on met a jour le vector_deplacement
                et on redessine'''
            self.vector_deplacement=(event.x-self.origin_click[0],event.y-self.origin_click[1])

            self.draw(cnv)
            

        def unselect(event):
            '''lorsqu'on lache le click gauche de la souris :
                    -on remet les attributs par defauts:
                    vector_deplacement,selected

                    -on met a jour la matrice selon le mouvement effectué

                    -on incrémente move
            '''
            if self.selected and self.selectedCoord!=self.vehicules[self.selected].coord :
                self.addMove()
                self.updateMatrice(self.vehicules[self.selected],self.selectedCoord)
                

            self.vector_deplacement=(0,0)
            self.selected=None
            self.draw(cnv)
            
        

        root=Tk()
        cnv=Canvas(root,width=WIDTH,height=HEIGHT,bg="ivory")
        cnv.pack(side="left",padx=0,pady=0)
        root.bind('<Button-1>',selection)
        root.bind('<B1-Motion>',updateMove)
        root.bind('<ButtonRelease-1>',unselect)
        root.title("Partie")

        self.draw(cnv)
        
        
        
        root.mainloop()



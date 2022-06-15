from secrets import choice
from lib.gamezone import firstLevel, secondLevel
import tkinter as tk
from tkinter import PhotoImage, Label, messagebox
import copy,pygame
from random import choice

class GameWindow(tk.Tk):  #Clase que hereda tkinter    
    """ Clase principal para el manejo de Tkinter """

    def __init__(self): #constructor
        tk.Tk.__init__(self) #ejecucion del constructor
        self.__gameSetup = GameSetup()
        self.initComponents()
                
    def initComponents(self): #Se inician las funciones
        self.__setupMatrix()
        self.__setupWindow()
        self.__setupCanvas()
        self.__setupImageFiles()
        self.__setupImages()
        self.__setupMusic()
        self.__setupBindings()

    def __setupMusic(self): # configuracion de la musica            
        pygame.mixer.init()#Turn on pygame
        pygame.mixer.music.load("sound/level.mp3")#Import song
        pygame.mixer.music.play(loops=0) #Play the song once

    def __setupMatrix(self): #Se carga la matriz correspondiente al nivel deseado 
        self.__gameSetup.getMatrix().loadMatrix(copy.deepcopy(secondLevel)) #el copy se usa para crea un nuevo objeto, no modificar el mismo
        
    def __setupWindow(self): #Configuracion de la ventana principal
        self.geometry("772x608+300+60")
        self.resizable(False,False)
        self.title("Donkey")

    def __setupCanvas(self): # Configuracion de canvas principal
        self.__gameCanvas = tk.Canvas(self, width=770, height=608, bg="Black")
        self.__gameCanvas.place(x=0, y=0)

    def __setupBindings(self):# Configuracion de los movimientos mediante teclas
        self.bind('<d>', lambda event: self.__move(self.__gameSetup.getPlayer().walkRight))
        self.bind('<w>', lambda event: self.__move(self.__gameSetup.getPlayer().climbUp))
        self.bind('<s>', lambda event: self.__move(self.__gameSetup.getPlayer().climbDown))
        self.bind('<a>', lambda event: self.__move(self.__gameSetup.getPlayer().walkLeft))
        self.bind('<q>', lambda event: self.__jumpLeft())
        self.bind('<e>', lambda event: self.__jumpRight())

    def __move(self, pMoveFunction):#funcion que realiza el movimiento general del personaje
        x = self.__gameSetup.getPlayer().getCoordinates()[0]
        y = self.__gameSetup.getPlayer().getCoordinates()[1]
        if self.__gameSetup.getCheck().gameLose(x, y):
            messagebox.showerror("LOST", "YOU LOST!")
        else: 
            if not self.__gameSetup.getCheck().gameWin(x, y):
                isFalling = self.__gameSetup.getCheck().checkFalling(x, y)
                if isFalling:
                    while True:
                        movement = self.__gameSetup.getPlayer().fallingDown()
                        self.__updateVisualMatrix(movement[0], movement[1])
                        isFalling = self.__gameSetup.getCheck().checkFalling(self.__gameSetup.getPlayer().getCoordinates()[0], self.__gameSetup.getPlayer().getCoordinates()[1])
                        if not isFalling:
                            break
                else:
                    movement = pMoveFunction()
                    self.__updateVisualMatrix(movement[0], movement[1])
            else:
                messagebox.showinfo("WIN", "YOU WON!")

   
    def __jumpRight(self):#llamado a movimiento y actualizacion visual
        x = self.__gameSetup.getPlayer().getCoordinates()[0]
        y = self.__gameSetup.getPlayer().getCoordinates()[1]
        isFalling = self.__gameSetup.getCheck().checkFalling(x, y)    
        if isFalling:  
            while True:
                movement = self.__gameSetup.getPlayer().fallingDown()
                self.__updateVisualMatrix(movement[0], movement[1])
                isFalling = self.__gameSetup.getCheck().checkFalling(self.__gameSetup.getPlayer().getCoordinates()[0], self.__gameSetup.getPlayer().getCoordinates()[1])
                if not isFalling:
                    break
        else:
                movement = self.__gameSetup.getPlayer().fistPartOfJump()
                self.__updateVisualMatrix(movement[0], movement[1])

                movement = self.__gameSetup.getPlayer().jumpRigth()
                self.__updateVisualMatrix(movement[0], movement[1])  

                movement = self.__gameSetup.getPlayer().thirdPartOfJump(3)
                self.__updateVisualMatrix(movement[0], movement[1])  

    def __jumpLeft(self): # Llamado a movimiento y actualizacion visual
        x = self.__gameSetup.getPlayer().getCoordinates()[0]
        y = self.__gameSetup.getPlayer().getCoordinates()[1]
        isFalling = self.__gameSetup.getCheck().checkFalling(x, y)    
        if isFalling:  
            while True:
                movement = self.__gameSetup.getPlayer().fallingDown()
                self.__updateVisualMatrix(movement[0], movement[1])
                isFalling = self.__gameSetup.getCheck().checkFalling(self.__gameSetup.getPlayer().getCoordinates()[0], self.__gameSetup.getPlayer().getCoordinates()[1])
                if not isFalling:
                    break
        else:
            movement = self.__gameSetup.getPlayer().fistPartOfJump()
            self.__updateVisualMatrix(movement[0], movement[1])

            movement = self.__gameSetup.getPlayer().jumpLeft()
            self.__updateVisualMatrix(movement[0], movement[1])  

            movement = self.__gameSetup.getPlayer().thirdPartOfJump(-3)
            self.__updateVisualMatrix(movement[0], movement[1])   
        
    def __barrel(self): # Llamado a creacion de barril y actualizacion visual
        movement = self.__gameSetup.getBarrel().generateBarrel()
        self.__updateVisualMatrix(movement[0], movement[1])

    def __moveBarrel(self): # Llamado a movimiento de barril y actualizacion visual
        movement = self.__gameSetup.getBarrel().moveBarrel()
        self.__updateVisualMatrix(movement[0], movement[1])

    def __updateVisualMatrix(self, oldMovement, newMovement): # funcion que actualiza dos elementos de la matriz dados movimientos
        Label(self.__gameCanvas, image=self.__getImage(oldMovement[1]), bg="Black").place(x=oldMovement[0][1]*32,y=oldMovement[0][0]*32)
        Label(self.__gameCanvas, image=self.__getImage(newMovement[1]), bg="Black").place(x=newMovement[0][1]*32,y=newMovement[0][0]*32)

    def __setupImageFiles(self): # Creacion de las imagenes a usar y cargandolas en MEMORIA
        self.__floorImage = PhotoImage(file = "media/woodBlock.png")
        self.__ladderImage = PhotoImage(file = "media/ladder.png")
        self.__leftImage = PhotoImage(file = "media/marioLeft.png")
        self.__rightImage = PhotoImage(file = "media/marioRight.png")
        self.__climbImage = PhotoImage(file = "media/marioClimb.png")
        self.__blackImage = PhotoImage(file = "media/blackPiece.png")
        self.__dkLeftImage = PhotoImage(file ="media/dkLeft.png")
        self.__princessImage = PhotoImage(file ="media/princess.png")
        self.__barrel1 = PhotoImage(file="media/barrelSides.png")
        self.__barrelDown = PhotoImage(file="media/barrelDown.png")
        self.__blueBarrel = PhotoImage(file="media/blueBarrelSides.png")
        self.__blueBarrelDown = PhotoImage(file="media/blueBarrelDown.png")


    def __getImage(self, id): # funcion para obtener la imagen deseada dependiendo de su ID
        if id == -1 or id == 1:
            return self.__floorImage
        elif id == 2 or id == -2:
            return self.__ladderImage
        elif id == 3:
            return self.__rightImage
        elif id == -3:
            return self.__leftImage
        elif id == 3.1:
            return self.__climbImage
        elif id == 4:
            return self.__princessImage
        elif id == -5:
            return self.__dkLeftImage
        elif id == 7:
            return self.__blueBarrel
        elif id == 7.1:
            return self.__blueBarrelDown
        elif id == 6:
            return self.__barrel1
        elif id == 6.1:
            return self.__barrelDown
        else:
            return self.__blackImage
            
    def __setupImages(self): # Carga todas las imagenes visualmente
        
        matrix = self.__gameSetup.getMatrix().getMatrix()

        for i in range(0,len(matrix)):
            for j in range(0,len(matrix[0])):
                Label(self.__gameCanvas, image=self.__getImage(matrix[i][j]), bg="Black").place(x=j*32,y=i*32)

class Matrix(object):
    __instance = None

    def __new__(cls): #Haciendo uso de un singletone para tener una unica instancia de la matriz
        if cls.__instance is None:
            cls.__instance = super(Matrix, cls).__new__(cls)
            cls.__matrix = []
        return cls.__instance

    def loadMatrix(cls, pMatrix): # cargando la matriz 
        cls.__matrix = pMatrix

    def getMatrix(cls): # funcion que devulve la matriz
        return cls.__matrix

    def updatePosition(cls, pOld, pNew,oldID, newID): # funcion que actualiza la matriz a nivel logico
        cls.__matrix[pOld[0]][pOld[1]] = oldID 
        cls.__matrix[pNew[0]][pNew[1]] = newID 
        return (pOld, oldID), (pNew, newID)

class ToCheck: 
    def __init__(self):#constructor 

        self.__matrix = Matrix()

    def checkFloorRight(self, pX, pY): #funcion que verfica si hay un bloque de suelo en la posicion derecha
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x + 1][self.__y + 1] == 1 

    def checkLimitRight(self, pX, pY): # funcion que verifica si hay un limite del mapa a la derecha 
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y + 1] == -7

    def checkExtendedLimitRight(self, pX, pY): # funcion que verifica si hay un limite dos bloques a la derecha
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y + 2] == -7

    def checkWallRight(self, pX, pY): # funcion que verifica si hay un bloque a la derecha (pared)
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y + 1] == 1     
            
    def checkFloorLeft(self, pX, pY): #funcion que verfica si hay un bloque de suelo en la posicion izquierda
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x + 1][self.__y - 1] == 1

    def checkLimitLeft(self, pX, pY): # funcion que verifica si hay un limite del mapa a la izquierda 
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y - 1] == -7

    def checkExtendedLimitLeft(self, pX, pY): # funcion que verifica si hay un limite dos bloques a la izquierda
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y - 2] == -7
    def checkWallLeft(self, pX, pY):# funcion que verifica si hay un bloque a la izquierda (pared)
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x][self.__y - 1] == 1
            
    def gameWin(self, pX, pY): #funcion que determina si el juego esta ganado(si se llega a la plataforma de la princesa)
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x + 1][self.__y] == -1
    
    def gameLose(self, pX, pY):#funcion que determina si el juego esta perdido
        self.__x = pX
        self.__y = pY
        lose = self.__matrix.getMatrix()[self.__x][self.__y] in [6,7,6.1,7.1]
        return lose

    def checkFalling(self, pX, pY): #funcion que verifica si el personaje esta callendo
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x + 1][self.__y] == 0 or self.__matrix.getMatrix()[self.__x + 1][self.__y] == 9 #caso puntual que al saltar sobre el punto de destruccion del barril el jugador no bajaba

    def checkLadderUp(self, pX, pY):#funcion que verifica si hay una escaler arriba y si hay suelo a los lados del perosnaje
        self.__x = pX
        self.__y = pY
        self.__floorOnSides = self.__matrix.getMatrix()[self.__x][self.__y + 1] == 1 and self.__matrix.getMatrix()[self.__x][self.__y - 1] == 1
        self.__princessLadder = self.__matrix.getMatrix()[self.__x][self.__y + 1] == -1
        return self.__matrix.getMatrix()[self.__x - 1][self.__y] == 2 or self.__floorOnSides or self.__princessLadder

    def checkLadderDown(self, pX, pY):#funcion que verifica si hay una escaler abajo
        self.__x = pX
        self.__y = pY
        return self.__matrix.getMatrix()[self.__x + 1][self.__y] == 2
              
    def exist(self, pX, pY): #funcion que verifica si el barril existe, (el barril dejara de existir si a la derecha o a la izquierda suya hay un 9(esto en la matriz logica))
        self.__barrelX = pX
        self.__barrelY = pY
        self.__exist = True
        if self.__matrix.getMatrix()[self.__barrelX][self.__barrelY + 1] or self.__matrix.getMatrix()[self.__barrelX][self.__barrelY - 1] == 9:
            self.__exist = False
            return self.__exist
        return self.__exist
    
    def useLadder(self): #funcion que genera un numero aleatorio, en funcion de el numero generado el barril usara la escalera o no
        value = choice((1, 2))
        return value == 1

class Player:
    def __init__(self): #constructor
        self.__x = 17
        self.__y = 2
        self.__lives = 3
        self.__points = 0 
        self.__check = ToCheck() 
        self.__matrix = Matrix()

    def walkRight(self): #funcion que mueve al jugador a la derecha haciendo uso de las verificaciones del mapa.
        if self.__check.checkLadderUp(self.__x, self.__y):   
            self.__oldId = 2
        else:
            self.__oldId = 0
        self.__id = 3
        oldY = self.__y
        if not self.__check.checkFalling(self.__x, self.__y):
            if  not self.__check.checkLimitRight(self.__x, self.__y) and not self.__check.checkWallRight(self.__x, self.__y):
                self.__y += 1
                return self.__matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
            return self.__matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id)
        else:
            self.fallingDown()
    
    def walkLeft(self): #funcion que mueve al jugador a la izquierda haciendo uso de las verificaciones del mapa.
        if self.__check.checkLadderUp(self.__x, self.__y):   
            self.__oldId = 2
        else:
            self.__oldId = 0
        self.__id = -3 
        oldY = self.__y
        if not self.__check.checkFalling(self.__x, self.__y):       
            if not self.__check.checkLimitLeft(self.__x, self.__y) and not self.__check.checkWallLeft(self.__x, self.__y):
                self.__y -= 1
                return self.__matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
            return self.__matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id)
        else:
            self.fallingDown()    

    def climbUp(self): #funcion que sube escaleras haciendo uso de las verificaciones del mapa.
        self.__oldId = 2
        self.__id = 3.1
        oldX = self.__x
        if self.__check.checkLadderUp(self.__x, self.__y):  
            self.__x -= 1 
            return self.__matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)    
        return self.__matrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldId,  self.__id)
 
    def climbDown(self): #funcion que baja escaleras haciendo uso de las verificaciones del mapa.

        if self.__matrix.getMatrix()[self.__x + 1][self.__y + 1] == 1 and self.__matrix.getMatrix()[self.__x + 1][self.__y - 1] == 1:
             self.__oldId = 0
        else:
            self.__oldId = 2

        self.__id = 3.1
        oldX = self.__x
        if self.__check.checkLadderDown(self.__x, self.__y):
            self.__x += 1
            return self.__matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)
        return self.__matrix.updatePosition((oldX, self.__y), (oldX, self.__y),self.__oldId, self.__id)
    
    def fistPartOfJump(self):# Funcion que hace el jugador suba un bloque
        self.__oldId = 0
        self.__id = 3
        oldX = self.__x 
        self.__x -= 1
        if not self.__check.checkLimitRight(self.__x, self.__y) or not self.__check.checkLimitLeft(self.__x, self.__y):
            return self.__matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)    
        return self.__matrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldId, self.__id)
        
    def jumpRigth(self):#funcion que mueve al jugador un bloque a la derecha

        self.__oldId = 0

        self.__id = 3
        oldY = self.__y 
        if not self.__check.checkLimitRight(self.__x, self.__y):
            if self.__check.checkExtendedLimitRight(self.__x, self.__y):
                self.__y += 1
            else:
                self.__y += 2
            return self.__matrix.updatePosition((self.__x, oldY),(self.__x, self.__y),self.__oldId, self.__id)
        return self.__matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId, self.__id)

    def jumpLeft(self):#funcion que mueve al jugador un bloque a la izquierda
        self.__oldId = 0
        self.__id = -3
        oldY = self.__y
        if not self.__check.checkLimitLeft(self.__x, self.__y):
            if self.__check.checkExtendedLimitLeft(self.__x, self.__y):
                self.__y -= 1
            else:
                self.__y -= 2
            return self.__matrix.updatePosition((self.__x, oldY),(self.__x, self.__y),self.__oldId, self.__id)
        return self.__matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId, self.__id)       

    def thirdPartOfJump(self, id): #fucion que hace que el jugador baje un bloque si es necesario 
        if self.__matrix.getMatrix()[self.__x - 1][self.__y] == 2:
            self.__oldId = 2    
        else:
            self.__oldId = 0
        self.__id = id
        oldX = self.__x
        self.__floorOnSides = self.__matrix.getMatrix()[self.__x + 1][self.__y + 1] == 1 and self.__matrix.getMatrix()[self.__x + 1][self.__y - 1] == 1
        if self.__check.checkFalling(self.__x , self.__y) or self.__check.checkLadderDown(self.__x, self.__y) and not self.__floorOnSides: 
            self.__x += 1
            return self.__matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)
        return self.__matrix.updatePosition((oldX, self.__y), (oldX, self.__y), self.__oldId, self.__id)   

    def fallingDown(self): #funcion que hace que el jugador caiga cuando no hay bloques abajo.
        self.__oldId = 0
        self.__id = 3.1 
        oldX = self.__x

        while self.__check.checkFalling(self.__x, self.__y):
            self.__x += 1
            return self.__matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)

    def getCoordinates(self): #funcion que retorna las cooredenadas actuales del jugador 
        return self.__x, self.__y
            
class Barrel:
    def __init__(self): #constructor
        self.__direction = -1 #el -1 representa la izquierda, por lo tanto siempre va a ir hacia la izquierda, pero si toca con un limite o pared cambia de direccion 
        self.__x = 3
        self.__y = 20
        self.__matrix = Matrix()
        self.generateBarrel()
    
    def getRandomNumber(self): #genera un numero aleatorio el cual representara el tipo de barril
        random = choice((6,7))
        return random
    
    def generateBarrel(self): #funcion que genera un barril en el mapa
        self.__barrelType = self.getRandomNumber()
        #return self.__matrix.updatePosition((3,20),(3,20), 0, self.__barrelType)
    
    def moveBarrel(self): #Funcion que se encarga de mover el barril, de igual manera hace uso de la funciones de verificacion necesarias.
        if ToCheck.exist(self.__x, self.__y):
            if ToCheck.checkLadderDown(self.__x, self.__y):
                if ToCheck.useLadder():
                    if Matrix.getMatrix()[self.__x - 1, self.__y] == 0:
                        self.__oldId = 0                  
                    self.__oldId = 2
                        
                    if self.getRandomNumber() == 6: 
                        self.__id = 6.1
                    self.__id = 7.1
                                    
                    oldX = self.__x
                        
                    if ToCheck.checkLadderDown(self.__x, self.__y):
                        self.__x += 1
                        return Matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)
                    return Matrix.updatePosition((oldX, self.__y), (oldX, self.__y),self.__oldId, self.__id)

                else:
                    if ToCheck.checkFalling():

                        oldX = self.__x
                        if Matrix.getMatrix()[self.__x + 1, self.__y] == 0:
                            self.__x += 1
                            return Matrix.updatePosition((oldX, self.__y), (self.__x, self.__y), self.__oldId, self.__id)
                    
                    elif self.__direction == -1:
                        oldY = self.__y
                        if not ToCheck.checkLimitLeft(self.__x, self.__y) and not ToCheck.checkWallLeft(self.__x, self.__y):
                            self.__y -= 1
                            return Matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
                        return Matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id)

                    else:
                        oldY = self.__y
                        if not ToCheck.checkLimitLeft(self.__x, self.__y) and not ToCheck.checkWallLeft(self.__x, self.__y):
                            self.__y += 1
                            return Matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
                        return Matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id)
            else:
                if self.__direction == -1:
                    oldY = self.__y
                    if not ToCheck.checkLimitLeft(self.__x, self.__y) and not ToCheck.checkWallLeft(self.__x, self.__y):
                        self.__y -= 1
                        return Matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
                    return Matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id) 
                else:
                    oldY = self.__y
                    if not ToCheck.checkLimitLeft(self.__x, self.__y) and not ToCheck.checkWallLeft(self.__x, self.__y):
                        self.__y += 1
                        return Matrix.updatePosition((self.__x, oldY), (self.__x, self.__y), self.__oldId,  self.__id)
                    return Matrix.updatePosition((self.__x, oldY), (self.__x, oldY), self.__oldId,  self.__id)                       
        else: 
            return Matrix.updatePosition((self.__x, self.__y), (0, 0), 0, 0)

class GameSetup: #funcion que sirve de intermediario para no crear un conflicto de instancias(dependecia circular)
    def __init__(self): #constructor
        self.__matrix = Matrix()
        self.__player = Player()
        self.__barrel = Barrel()
        self.__check = ToCheck()
    
    def getMatrix(self): #funcion que sirve de medio para acceder a la clase Matrix()
        return self.__matrix

    def getPlayer(self):#funcion que sirve de medio para acceder a la clase Player()
        return self.__player

    def getBarrel(self):#funcion que sirve de medio para acceder a la clase Barrel()
        return self.__barrel
    
    def getCheck(self):#funcion que sirve de medio para acceder a la clase ToCheck()
        return self.__check 
        
class Main: #Clase que inicia el video juego 
    def __init__(self):#constructor
        self.__game = GameWindow()

    def run(self):#funcio que coloca la ventana del juego en el mainloop
        self.__game.mainloop()

game = Main()
game.run()

import threading
import tkinter as tk
from tkinter import *
from threading import Thread
import random
import time
import tkinter
import keyboard
from PIL import ImageTk, Image
from tkinter import Toplevel
import pygame
import sys
import natsort
from tkinter import font, PhotoImage
from natsort import natsorted
import tkinter as tk
from tkinter import messagebox
import math

#Variabes globales
window = None

#Constantes
filas = 40
columnas = 36
ventana_ancho = 540
ventana_alto = 700

#Definir colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
azul = (0, 0, 102)
amarillo = (255, 255, 0)
naranja = "#FF4500"
rosado = "#FF4501"
rojo = (255, 0, 0)
celeste = (255, 19, 0)
tamano_casilla = ventana_ancho // columnas

Partida = None
entryNombre= "" 
nombreJugadorActual = ""
pared = 0
alimento = 1
capsula = 2
alimentoComida = 3
vacio = 4

MoverFantasmas= True

ListaFantasmas = []


# Inicializar el score
score = 0

# Función para mostrar el score en la pantalla


running = True

button_width = 100
button_height = 40
button_x = ventana_ancho - button_width - 10  # Alineado a la derecha
button_y = ventana_alto - button_height - 10



class Juego:
    def __init__(self, tablero,  nivel, score, Jugador, Fantasmas ):
        self.tablero = tablero
        self.nivel = nivel
        self.score = score
        self.Jugador = Jugador
        self.Fantasmas = Fantasmas

    def iniciarJuego(self):
        self.score = 0

class PacMan:
    def __init__(self,velocidad,posicion_x,posicion_y):
        self.velocidad = velocidad
        self.x = 0 
        self.y = 0

class Fantasma:
    def __init__(self, color):
        self.estado = True  
        self.posicion_x = 18 
        self.posicion_y = 20 
        self.anterior = 4 
        self.color = color 

    def moverIzquierda(self,tablero,xJugador, yJugador):
        global MoverFantasmas
        next_x = self.posicion_x - 1
        if tablero[self.posicion_y][next_x] in (1, 2, 3, 4):
            self.posicion_x = next_x
        if((next_x == xJugador or self.posicion_x == xJugador) and self.posicion_y == yJugador ):
            MoverFantasmas =False
            
            

    def moverDerecha(self,tablero,xJugador, yJugador):
        global MoverFantasmas
        next_x = self.posicion_x + 1
        if tablero[self.posicion_y][next_x] in (1, 2, 3, 4):
            self.posicion_x = next_x
        if((next_x == xJugador or self.posicion_x == xJugador) and self.posicion_y == yJugador ):
            MoverFantasmas=False
            

    def moverArriba(self,tablero,xJugador, yJugador):
        global MoverFantasmas
        next_y = self.posicion_y - 1
        if tablero[next_y][self.posicion_x] in (1, 2, 3, 4):
           self.posicion_y = next_y
        if((next_y == xJugador or self.posicion_x == xJugador) and self.posicion_y == yJugador ):
            MoverFantasmas=False
            

    def moverAbajo(self,tablero,xJugador, yJugador):
        global MoverFantasmas
        next_y = self.posicion_y + 1
        if tablero[next_y][self.posicion_x] in (1, 2, 3,4):
           self.posicion_y = next_y
        if((next_y == xJugador or self.posicion_x == xJugador) and self.posicion_y == yJugador ):
            MoverFantasmas=False
            


#Inicializa Pygame y carga la música en la función play()
pygame.mixer.init()
def play():
    pygame.mixer.music.load("pacman-song.mp3")
    pygame.mixer.music.play(loops=0)

def stop_music():
    pygame.mixer.music.stop()

#Abre la ventana principal
def ventana_inicio():
    global window
    ventana1 = tk.Tk()
    ventana1.title("Diviértete")
    ventana1.minsize(height=480, width=800)
    ventana1.configure(background="black") #Color del tk
    
    #Fondo ventana_principal
    fondo = tk.PhotoImage(file="Fondo PAC-MAN.png")
    fondo_label = tk.Label(ventana1, image=fondo)
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
    ventana1.resizable(height=False, width=False)
    
    #Titulo Ventana Principal
    tituloPrincipal = tk.Label(ventana1, text="ROBOTS", font=("Courier New", 12, "bold"), background="grey", fg="white")
    tituloPrincipal.place(x=1400, y=25)
    def iniciar(vent):
        global entryNombre
        if (str(entryNombre.get())!=""):
            entryNombre =str(entryNombre.get())
            vent.destroy()
            Ventana_juego()
        else:
            messagebox.showinfo("Advertencia", "Debe ingresar un nombre valido")

    def ventana_nombre():
        global entryNombre
        ventana1.withdraw()
        nombre = Toplevel()
        nombre.title("Nombre jugador") #nombre de la ventana
        nombre.geometry("400x300") # dimensiones de la ventana
        nombre.configure(background="CadetBlue1") #color del fondo 
        #canvas
        canvasC3 = tkinter.Canvas(nombre, width=300, height=200, borderwidth=0, highlightthickness=0, background="pink")
        canvasC3.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        #titulo para identicar que tiene que hacer el jugador 
        titulo4= tkinter.Label(canvasC3, text="Ingrese su nombre:", font=("Verdana", 12), background="pink", fg="black")
        titulo4.place(x=50, y=60)
        # barra donde se escribe el nombre
        entryNombre= tkinter.Entry(nombre, width=40)
        entryNombre.pack()
        entryNombre.place(x=70, y=150)
        #boton aceptar para ir a la pantalla de juego
        Aceptar_Boton= tkinter.Button(nombre, text= "Aceptar", command=lambda:iniciar(nombre), fg=("white"), bg=("coral"))
        Aceptar_Boton.pack(pady=10)
        Aceptar_Boton.place(x=150, y=200)
    
    def agarrar_nombre():
        global nombreJugadorActual
        global score
        global Partida
        nombre = nombreJugadorActual
        print(nombre)
        try:
            with open('data.txt', 'a') as file:  # agrega al txt los datos

                file.write(f'{Partida.score}-{nombre},')
                file.close()
        except:
            with open('data.txt', 'w') as file:  # crea el txt de no existir
                file.write(f'{Partida.score}: {nombre},')


    #Ventana JUEGO
    def Ventana_juego():
        global ventana_alto
        global ventana_ancho
        pygame.init()
        ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
        pygame.display.set_caption("PacMan")
        font = pygame.font.Font(None, 36)
        clock = pygame.time.Clock()

        
        #Funcion para dibujar tablero de juego
        global Partida
        def show_score():
            
            pygame.draw.rect(ventana, negro, (0 , 600, 300, 100))
            score_text = font.render(f"Score: {Partida.score}", True, blanco)
            
            ventana.blit(score_text, (10, 600))
        
        
        def nombre():
            global nombreJugadorActual
            if(entryNombre != ""):
                NombreJugador = str(entryNombre)
                nombreJugadorActual = str(entryNombre)
            juganombre = font.render(f"Jugador@: {NombreJugador}", True, blanco)
            ventana.blit(juganombre, (10, 620))

       
       
        tableroJuego = [
                [4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [2, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],

                    ]
        

        Jugador = PacMan(0, 0, 0)
        ListaFantasmas = []
        for i in range (1):
            ListaFantasmas.append(Fantasma(rojo))
            ListaFantasmas.append(Fantasma(naranja))
            ListaFantasmas.append(Fantasma(rosado))
            ListaFantasmas.append(Fantasma(celeste))
        Partida = Juego(tableroJuego,1,0, Jugador, ListaFantasmas)

        def mover(fantasma,velocidad):
            global MoverFantasmas
            global Partida
            while MoverFantasmas:
                try:
                    time.sleep(velocidad)
                    direccion = random.choice(["izquierda", "derecha", "arriba", "abajo"])
                    
                    if direccion == "izquierda":
                        fantasma.moverIzquierda(Partida.tablero,Partida.Jugador.x, Partida.Jugador.y)
                    elif direccion == "derecha":
                        fantasma.moverDerecha(Partida.tablero, Partida.Jugador.x, Partida.Jugador.y)
                    elif direccion == "arriba":
                        fantasma.moverArriba(Partida.tablero, Partida.Jugador.x, Partida.Jugador.y)
                    elif direccion == "abajo":
                        fantasma.moverAbajo(Partida.tablero, Partida.Jugador.x, Partida.Jugador.y)
                except Exception as e:
                    # Maneja la excepción aquí, por ejemplo, imprime un mensaje de error
                    print(f"Error en el hilo: {e}")
            print("Se acabo el juego")

        for fantasma in Partida.Fantasmas:
            # Crea un objeto de hilo
            veloc= 0.5
            if fantasma.color==rojo:
                veloc=0.25
            hilo = threading.Thread(target=mover,args=(fantasma,veloc))

            # Inicia la ejecución del hilo
            hilo.start()

            

        jugador_imagen = pygame.image.load("jugador.png") 
        jugador_imagen = pygame.transform.scale(jugador_imagen, (tamano_casilla, tamano_casilla))

       # fantasma_rojo = pygame.image.load("rojo.png") 
        #fantasma_rojo = pygame.transform.scale(fantasma_rojo, (tamano_casilla, tamano_casilla))
            
        #Funcion para dibujar tablero de juego
        def dibujar_tablero():
            for fila in range(filas):
                for columna in range(columnas):
                    if Partida.tablero[fila][columna]==0:
                        pygame.draw.rect(ventana, azul, (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                    elif Partida.tablero[fila][columna]==1:
                        x = columna * tamano_casilla + tamano_casilla // 2
                        y = fila * tamano_casilla + tamano_casilla // 2
                        radio = tamano_casilla // 4
                        pygame.draw.rect(ventana, negro, (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                        pygame.draw.circle(ventana, amarillo, (x, y), radio)
                    elif Partida.tablero[fila][columna]==2:
                        x = columna * tamano_casilla + tamano_casilla // 2
                        y = fila * tamano_casilla + tamano_casilla // 2
                        radio = tamano_casilla // 2
                        pygame.draw.rect(ventana, negro, (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                        pygame.draw.circle(ventana, blanco, (x, y), radio)
                    elif Partida.tablero[fila][columna]==3:
                        x = columna * tamano_casilla + tamano_casilla // 2
                        y = fila * tamano_casilla + tamano_casilla // 2
                        radio = tamano_casilla // 3
                        pygame.draw.rect(ventana, negro, (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                        pygame.draw.circle(ventana, naranja, (x, y), radio)
                    elif Partida.tablero[fila][columna]==4:
                        pygame.draw.rect(ventana, negro, (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                    
                    
                
            jugador_rect = jugador_imagen.get_rect()
            jugador_rect.topleft = (Jugador.x * tamano_casilla, Jugador.y * tamano_casilla)
            ventana.blit(jugador_imagen, jugador_rect.topleft)

            for fantasmaR in Partida.Fantasmas:
                fantasma_Aux = pygame.image.load("rojo.png")
                if fantasmaR.color == rosado:
                    fantasma_Aux = pygame.image.load("rosado.png")
                elif fantasmaR.color == naranja:
                    fantasma_Aux = pygame.image.load("naranja.png")
                elif fantasmaR.color == celeste:
                    fantasma_Aux = pygame.image.load("celeste.png")
                    
                fantasma_Aux = pygame.transform.scale(fantasma_Aux, (tamano_casilla, tamano_casilla))
                fantasma = fantasma_Aux.get_rect()
                fantasma.topleft = (fantasmaR.posicion_x * tamano_casilla, fantasmaR.posicion_y * tamano_casilla)
                ventana.blit(fantasma_Aux, fantasma.topleft)    
             
        def draw_button():
             # Alineado en la parte inferior
            pygame.draw.rect(ventana, blanco, (button_x, button_y, button_width, button_height))
            font = pygame.font.Font(None, 36)
            button_text = font.render("Regresar", True, negro)
            text_rect = button_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
            ventana.blit(button_text, text_rect.topleft)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height):
                        # Regresar a la Ventana1
                        pygame.quit()
                        sys.exit()

                    # Regresar a la Ventana
                pygame.display.flip()
                clock.tick(10)
                    # Regresar a la Ventana
            
            
                
                #Control de movimiento de Pac-Man
                keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and Jugador.y > 0 and Partida.tablero[Jugador.y - 1][Jugador.x] != 0:
                if Partida.tablero[Jugador.y - 1][Jugador.x] == 1:
                    Partida.tablero[Jugador.y - 1][Jugador.x] = 4
                    Partida.score+=2
                    
                elif Partida.tablero[Jugador.y - 1][Jugador.x] == 2:
                    Partida.tablero[Jugador.y - 1][Jugador.x] = 4
                elif Partida.tablero[Jugador.y - 1][Jugador.x] == 3:
                    Partida.tablero[Jugador.y - 1][Jugador.x] = 4  
                
                Jugador.y -= 1
            if keys[pygame.K_DOWN] and Jugador.y < 39  and Partida.tablero[Jugador.y + 1][Jugador.x] != 0:
                if Partida.tablero[Jugador.y + 1][Jugador.x] == 1:
                    Partida.tablero[Jugador.y + 1][Jugador.x] = 4
                    Partida.score+=2
               
                elif Partida.tablero[Jugador.y + 1][Jugador.x] == 2:
                    Partida.tablero[Jugador.y + 1][Jugador.x] = 4
                elif Partida.tablero[Jugador.y + 1][Jugador.x] == 3:
                    Partida.tablero[Jugador.y + 1][Jugador.x] = 4
                    
                Jugador.y += 1
            if keys[pygame.K_LEFT] and Jugador.x > 0 and Partida.tablero[Jugador.y][Jugador.x - 1] != 0:
                if Partida.tablero[Jugador.y][Jugador.x - 1] == 1:
                    Partida.tablero[Jugador.y][Jugador.x - 1] = 4
                    Partida.score+=2
                    
                elif Partida.tablero[Jugador.y][Jugador.x - 1] == 2:
                    Partida.tablero[Jugador.y][Jugador.x - 1] = 4
                elif Partida.tablero[Jugador.y][Jugador.x - 1] == 3:
                    Partida.tablero[Jugador.y][Jugador.x - 1] = 4
                    
                Jugador.x -= 1
            if keys[pygame.K_RIGHT] and Jugador.x < 35 and Partida.tablero[Jugador.y][Jugador.x + 1] != 0:
                if Partida.tablero[Jugador.y][Jugador.x + 1] == 1:
                    Partida.tablero[Jugador.y][Jugador.x + 1] = 4
                    Partida.score+=2
                    
                elif Partida.tablero[Jugador.y][Jugador.x + 1] == 2:
                    Partida.tablero[Jugador.y][Jugador.x + 1] = 4
                elif Partida.tablero[Jugador.y][Jugador.x + 1] == 3:
                    Partida.tablero[Jugador.y][Jugador.x + 1] = 4
                    
                Jugador.x += 1
           
            draw_button()
            
            

                # Controlar la velocidad de actualización
            clock.tick(5)

            show_score()
            nombre() 
            dibujar_tablero()
            pygame.display.update()


    
    #Ventana de mejores puntajes
    def abrirventana3():
        menuRank = Tk()
        menuRank.title('Salon de la fama')
        fondo = Canvas(menuRank, width=800, height=500, border=0, bg='pink')
        fondo.pack()
        
           
           # Regresar a la ventana principal
        def regresa():
            menuRank.destroy()
            ventana1.deiconify()
         #boton regresar
        botonRegre = tkinter.Button(fondo, text="❌", command=regresa)
        botonRegre.pack()
        botonRegre.place(x=30 , y=30)

        try: #trata de abrir el domcunento con los puntajes y los recrea en la pantalla una tabla de los mejores
            file = open('data.txt','r')
            read = file.read().split(',')
            print(read)
            top= natsorted(read,reverse=True)
            print(top)
            puesto1 = Label(fondo,text=f'1) {top[0]}',width=15, height=1,font=('Arial Black', 21, 'italic', 'bold'),bg='pink',fg='black')
            puesto1.place(x=320, y=25)
            puesto2 = Label(fondo,text=f'2) {top[1]}',width=15, height=2, font=('Arial Black', 21, 'italic', 'bold'),bg='pink',fg='black')
            puesto2.place(x=320, y=100)
            puesto3 = Label(fondo,text=f'3) {top[2]}', width=15, height=2, font=('Arial Black', 21, 'italic', 'bold'),bg='pink',fg='black')
            puesto3.place(x=320, y=200)
            puesto4 = Label(fondo,text=f'4) {top[3]}', width=15, height=2, font=('Arial Black', 21, 'italic', 'bold'),bg='pink',fg='black')
            puesto4.place(x=320, y=300)
            puesto5 = Label(fondo,text=f'5) {top[4]}', width=15, height=2, font=('Arial Black', 21, 'italic', 'bold'),bg='pink',fg='black')
            puesto5.place(x=320, y=400)

        except:
            None

        menuRank.mainloop()
        
        
    
    #Fución abrir ventana de Configuración
    def abrirventana4():
        ventana1.withdraw()
        ventana4 = Toplevel()
        ventana4.title("Ventana 4")
        ventana4.geometry("800x480")
        ventana4.configure(background="black")
        canvasC4 = tk.Canvas(ventana4, width=800, height=680, borderwidth=0, highlightthickness=0, background="black")
        canvasC4.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        titulo= tk.Label(canvasC4, text="Sonido", font=("Courier New", 16, "bold"), background="black", fg="white")
        titulo.place(x=330 ,y=170)
        ventana4.resizable(height=False, width=False)

        # Botón de play
        botonP = Button(ventana4, text="Play", font=("Courier New", 12, "bold"), command=play, fg=("white"), bg=("black"), width=8)
        botonP.pack()
        botonP.place(x=500, y=300)
        
        # Botón de stop music
        botonBack = tk.Button(ventana4, text="Stop Music", font=("Courier New", 12, "bold"), command=stop_music, fg=("white"), bg=("black"), width=12)
        botonBack.pack()
        botonBack.place(x=600, y=300)

        #Botón de back Ventana Configuración
        def back():
            ventana4.destroy()
            ventana1.deiconify()
  
        botonBack = tk.Button(ventana4, text="Back", command= back, font=("Courier New", 12, "bold"), fg=("white"), bg=("black"), width=8)
        botonBack.pack()
        botonBack.place(x=650, y=420)

        abrirventana4.mainloop()


    #Fución abrir ventana de Ayuda
    def abrirventana5():
        ventana1.withdraw()
        ventana5 = Toplevel()
        ventana5.title("Ventana 3")
        ventana5.geometry("800x480")
        ventana5.configure(background="white")
        canvasC4 = tk.Canvas(ventana5, width=800, height=680, borderwidth=0, highlightthickness=0, background="black")
        canvasC4.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
        titulo= tk.Label(canvasC4, text="Controles", font=("Courier New", 15, "bold"), fg=("white"), bg=("black"))
        titulo.place(x=310, y=120)
        ventana5.resizable(height=False, width=False)

        texto= tk.Label(canvasC4, text="Mover hacia arriba: W "
                                        "\nMover hacia abajo: X" 
                                        "\nMover hacia la derecha: D"
                                        "\nMover hacia la izquierda: A"
                                        
                                ,font=("Courier New", 12, "bold"), fg=("white"), bg=("black"), justify=tk.LEFT)
        texto.place(x=50, y=180)

        image= Image.open("Teclado.png")
        image = image.resize((500,150))
        img = ImageTk.PhotoImage(image)
        yo_img = Label(canvasC4, image=img)
        yo_img.pack()
        yo_img.place(x=110, y=405)

        #Botón de back Ventana Ayuda
        #The above code creates a button in a tkinter window that, when clicked, closes the current
        #window and opens another window.
        
        def back():
            ventana5.destroy()
            ventana1.deiconify()

        botonBack = tk.Button(ventana5, text="Back", command= back, fg=("white"), font=("Courier New", 12, "bold"), bg=("black"), width=8)
        botonBack.pack()
        botonBack.place(x=650, y=420)

        abrirventana5.mainloop()
        
    #Fución abrir ventana "Acerca de"
    #The function "abrirventana6" opens a new window called "Acerca de" with personal information and
    #a back button.
    def abrirventana6():
        ventana1.withdraw()
        ventana6 = Toplevel()
        ventana6.title("Ventana 3")
        ventana6.geometry("800x480")
        ventana6.configure(background="black")
        canvasC4 = tk.Canvas(ventana6, width=800, height=680, borderwidth=0, highlightthickness=0, background="black")
        canvasC4.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        titulo= tk.Label(canvasC4, text="Informacion Personal", fg=("white"), font=("Courier New", 12, "bold"), bg=("black"))
        titulo.place(x=308, y=110)
        ventana6.resizable(height=False, width=False)
    
    #Botón de back Ventana "Acerca de"
        def back():
            ventana6.destroy()
            ventana1.deiconify()
            
        botonBack = tk.Button(ventana6, text="Back", font=("Courier New", 12, "bold"), command= back, fg=("white"), bg=("black"), width=8 )
        botonBack.pack()
        botonBack.place(x=650, y=420)
        
        abrirventana6.mainloop()

    
    
    #Botones Principales VENTANA 1
    boton1 = tk.Button(ventana1, text="Jugar", command=ventana_nombre,font=("Courier New", 16, "bold"), fg=("white"), bg=("black"))
    boton1.place(x=240, y=60)
    boton2 = tk.Button(ventana1, text="Configuración",command=abrirventana4, font=("Courier New", 16, "bold"), fg=("white"), bg=("black"))
    boton2.place(x=185, y=217)
    boton3 = tk.Button(ventana1, text="Ayuda", command=abrirventana5, font=("Courier New", 14, "bold"), fg=("white"), bg=("black"))
    boton3.place(x=75, y=420)
    boton4 = tk.Button(ventana1, text="Mejores Puntajes",command=abrirventana3, font=("Courier New", 16, "bold"), fg=("white"), bg=("black"))
    boton4.place(x=170, y=140)
    boton5 = tk.Button(ventana1, text="Acerca de", command=abrirventana6, font=("Courier New", 14, "bold"), fg=("white"), bg=("black"))
    boton5.place(x=350, y=420)
    
    ventana1.mainloop() 
ventana_inicio()
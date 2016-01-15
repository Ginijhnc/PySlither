import pygame
import time
import random


pygame.init()

#Seteando colores RGB customizados
white = (220,220,220) 
black = (0,0,0)
red = (255,0,0)
green = (0,100,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height)) #Muestra pantalla del juego 800x600
pygame.display.set_caption("La serpienteh") #Titulo del juego. Caption.

icon = pygame.image.load('icon.png')
#Sin ruta completa ya que la imagen esta en el mismo lugar que el script

pygame.display.set_icon(icon) #Seteando icono

#--------------------------------------------------#


imgHead = pygame.image.load('snakehead.png')
imgApple = pygame.image.load('apple.png')

clock = pygame.time.Clock()
FPS = 30

direction = 'right' #Empieza apuntando hacia la derecha

font = pygame.font.SysFont(None, 25)

def snake(block_size, snakeList):
    if direction == 'right':
        head = pygame.transform.rotate(imgHead, 270)
    if direction == 'left':
        head = pygame.transform.rotate(imgHead, 90)
    if direction == 'up':
        head = imgHead #El estado original de la cabeza es mirando para arriba, por lo tanto no se rota.-
    if direction == 'down':
        head = pygame.transform.rotate(imgHead, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    #Creando las extremidades para hacer mas larga la serpiente
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, green,[XnY[0], XnY[1],block_size,block_size])

def message_to_screen(msg,color): #Creando la funcion de mensajes para usarlo despues
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text,[display_width/3.5, display_height/2.2])

block_size = 10
appleThickness = 20

#Se puede indentar todo el codigo seleccionandolo y apretando TAB
def gameLoop():
    global direction
    gameExit = False
    gameOver = False 
    
    lead_x = (display_width)/2 #-Primer- Bloque de la serpiente
    lead_y = (display_height)/2
    lead_x_change = 0
    lead_y_change = 0

    snakeList = []
    snakeLength = 1
    score = 0

#/10.0)*11.10) = Redondear los datos para mayor precision en las colisiones del juego
    randAppleX = round(random.randrange(0, display_width-(appleThickness)+20)/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-(appleThickness)+20)/10.0)*10.0

    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Perdiste :(. Apretá C para jugar de nuevo o Q para cerrar el juego.", red)
            pygame.display.update() #Actualizando para que se vea el mensaje

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                    break #Romper el loop, se cierra todo
                
                if event.type == pygame.KEYDOWN: #Si se toca una tecla : ...
                    if event.key == pygame.K_q: #Si toca "q", se cierra el juego
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop() #Hace loop de todo el juego para que empiece denuevo

        for event in pygame.event.get(): #Event handling (teclas y sus funciones)
            if event.type == pygame.QUIT: #Si clickea la cruz, entonces cierra
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = block_size
                    lead_x_change = 0

        #Definiendo limites y colisiones
        if lead_x >= display_width or lead_x < 10 or lead_y >= display_height or lead_y < 0:
            gameOver = True #Si se va del limite, gameOver.


                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    lead_x_change = 0

        lead_x = (lead_x)+(lead_x_change)
        lead_y = (lead_y)+(lead_y_change)

        gameDisplay.fill(white) #Seteando el FONDO como blanco

# Creando las extremidades para hacer mas larga la serpiente
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y) 
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]: #[:-1] = Anything up to the last element.
            if eachSegment == snakeHead: #Colisiona, entonces perdes el juego
                gameOver = True

        
        snake(block_size,snakeList) #Serpiente
    #Dibuja rectangulo. En gameDisplay. Rojo. Posicionado en 400x300. 30x30 de alto y ancho.
    #Mas info: https://www.pygame.org/docs/ref/draw.html#pygame.draw.rect
        gameDisplay.fill(black, rect=[200,200,100,100]) #fill: Otra manera de crear formas

        gameDisplay.blit(imgApple, (randAppleX, randAppleY)) #Carga la imagen
        pygame.display.update() #Updatear asi se ve el fondo blanco


#       Sistema de colisiones
        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
                randAppleY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
                snakeLength = snakeLength + 1
                score = score + 1
                print ("Score: "+str(score)) #Printing puntaje

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX = round(random.randrange(0, display_width-block_size)/10.0)*10.0
                randAppleY = round(random.randrange(0, display_height-block_size)/10.0)*10.0
                snakeLength = snakeLength + 1
#       /Sistema de colisiones

        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()

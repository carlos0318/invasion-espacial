import pygame
import random
import math
from pygame import mixer

# inicializar pygame
pygame.init()

# para el tamaño de la pantalla en este caso 800px de alto y 600px para el ancho de la pantalla
pantalla = pygame.display.set_mode((800, 600))

# configuracion para el icon y el titulo
pygame.display.set_caption("Invasión Espacial")
icon = pygame.image.load("ovni.png")
pygame.display.set_icon(icon)
fondo = pygame.image.load("Fondo.jpg")

# agregar musica de fondo
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.5)
mixer.music.play(-1)  # se va a reproducir cada vez que termine

# variables del jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# variables de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf", 32)
texto_x = 10
texto_y = 10

# texto de final de juego
fuente_final = pygame.font.Font("freesansbold.ttf", 40)


def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# agregar el protagonista del juego
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# agregar el enemigo del juego
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    operacion1 = math.pow(x_1 - x_2, 2)
    operacion2 = math.pow(y_2 - y_1, 2)
    distancia = math.sqrt(operacion1 + operacion2)
    if distancia < 27:
        return True
    else:
        return False


# con el siguiente codigo hacemos un loop con el cual se queda la pantalla hasta que se le de en la x para cerrar la venta
se_ejecuta = True
while se_ejecuta:
    # cambiar el color de la pantalla (rgb)
    # pantalla.fill((205, 144, 228))

    # agregar una imagen como fongo de pantalla
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala = {"x": jugador_x, "y": jugador_y, "velocidad": -5}
                balas.append(nueva_bala)
                # if not bala_visible:
                #     bala_x = jugador_x
                #     disparar_bala(bala_x, bala_y)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar en donde se pitna el jugador
    jugador_x += jugador_x_cambio

    # mantener el jugador dentro de la pantalla
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar en donde se pitna el enemigo
    for e in range(cantidad_enemigos):
        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener el enemigo dentro de la pantalla
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        for bala in balas:
            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)

        # pintar enemigos en pantalla
        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala_y < 0:
            balas.remove(bala)

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    # pinta jugador y puntaje
    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()

import pygame
import random
import math
import sys
import os

# INICIALIZAR PYGAME
pygame.init()

# ESTABLECE TAMAÑO DE PANTALLA
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# FUNCION PARA OBTENER LA RUTA DE LOS RECURSOS
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

# CARGAR IMAGEN DE FONDO
asset_background = resource_path('invasion/images/background.png')
background = pygame.image.load(asset_background)

# CARGAR ICONOS DE VENTANA
asset_icon = resource_path('invasion/images/ufo.png')
icon = pygame.image.load(asset_icon)

# CARGAR SONIDO DE FONDO
asset_sound = resource_path('invasion/audios/background_music.mp3')
pygame.mixer.music.load(asset_sound)

# CARGAR IMAGEN DE JUGADOR
asset_playerimg = resource_path('invasion/images/space-invaders.png')
playerimg = pygame.image.load(asset_playerimg)

# CARGAR IMAGEN DE BALA
asset_bulletimg = resource_path('invasion/images/bullet.png')
bulletimg = pygame.image.load(asset_bulletimg)

# CARGAR FUENTE PARA TEXTO DE GAME OVER
asset_over_font = resource_path('invasion/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)

# CARGAR FUENTE PARA PUNTAJE
asset_font = resource_path('invasion/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# ESTABLECER TITULO DE VENTANA
pygame.display.set_caption('INVASION')

# ESTABLECER ICONO DE VENTANA
pygame.display.set_icon(icon)

# REPRODUCIR SONIDO DE FONDO EN LOOP
pygame.mixer.music.play(-1)

# CREAR RELOJ PARA CONTROLAR LA VELOCIDAD DEL JUEGO
clock = pygame.time.Clock()

# POSICION INICIAL DEL JUGADOR
playerX = 370
playerY = 470
playerx_change = 0
playery_change = 0

# LISTA PARA ALMACENAR POSICIONES DE LOS ENEMIGOS
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 10

#SE INICIALIZAN LAS VARIABLES PARA GUARDAR LAS POSICIONES DE LOS ENEMIGOS
for i in range(no_of_enemies):
    #enemigo 1
    enemy1 = resource_path('invasion/images/enemy1.png')
    enemyimg.append(pygame.image.load(enemy1))
    #enemigo 2
    enemy2 = resource_path('invasion/images/enemy2.png')
    enemyimg.append(pygame.image.load(enemy2))

    #SE ASIGNA POSICION ALEATORIA EN X Y Y PARA ENEMIGOS
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

    #SE ESTABLECE VELOCIDAD DE MOVIMIENTO DEL ENEMIGO EN X Y Y
    enemyX_change.append(5)
    enemyY_change.append(40)

# SE INICIALIZA LAS VARIABLES PARA GUARDAR LA POSICION DE LA BALA
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = 'ready'

# SE INICIALIZA LA PUNTUACION EN 0
score = 0

# FUNCION PARA MOSTRAR LA PUNTUACION EN LA PANTALLA
def show_score():
    score_value = font.render('SCORE: ' + str(score), True, (255, 255, 255))
    screen.blit(score_value, (10, 10))

# FUNCION PARA DIBUJAR AL JUGADOR EN LA PANTALLA
def player(x, y):
    screen.blit(playerimg, (x, y))

# FUNCION PARA DIBUJAR AL ENEMIGO EN LA PANTALLA
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

# FUNCION PARA DISPARAR LA BALA
def fire_bullet(x, y):
    global bullet_state

    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

# FUNCION PARA COMPROBAR SI HA HABIDO UNA COLISION ENTRE LA BALA Y EL ENEMIGO
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) +
                         (math.pow(enemyY - bulletY, 2)))

    if distance < 27:
        return True
    else:
        return False

# FUNCION PARA MOSTRAR EL TEXTO DE GAME OVER
def game_over_text():
    over_text = over_font.render('PERDISTE :)', True, (255, 255, 255))
    text_rect = over_text.get_rect(
        center=(int(screen_width / 2), int(screen_height / 2)))
    screen.blit(over_text, text_rect)
    pygame.display.update()

    pygame.time.delay(3000)

    # Cierra el juego
    pygame.quit()
    sys.exit()

# BUCLE PRINCIPAL DEL JUEGO
def gameloop():
    # DECLARAR VARIABLES GLOBALES
    global score
    global playerX
    global playerx_change
    global bulletX
    global bulletY
    global bullet_state

    in_game = True
    while in_game:
        # MANEJA EVENTOS, ACTUALIZA Y RENDERIZA EL JUEGO
        # LIMPIA LA PANTALLA
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # MANEJA LOS MOVIMIENTOS DEL JUGADOR Y DISPARO
                if event.key == pygame.K_LEFT:
                    playerx_change = -5

                if event.key == pygame.K_RIGHT:
                    playerx_change = 5

                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                playerx_change = 0

        # AQUI SE ESTA ACTUALIZANDO LA POSICION DEL JUGADOR
        playerX += playerx_change

        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # BUCLE QUE SE EJECUTA PARA CADA ENEMIGO
        for i in range(no_of_enemies):
            if enemyY[i] > 440:
                for j in range(no_of_enemies):
                    enemyY[j] = 2000
                game_over_text()

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            # AQUI SE COMPRUEBA SI HA HABIDO UNA COLISION ENTRE UN ENEMIGO Y UNA BALA
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                bulletY = 454
                bullet_state = 'ready'
                score += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(0, 150)
            enemy(enemyX[i], enemyY[i], i)

        if bulletY < 0:
            bulletY = 454
            bullet_state = 'ready'
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score()

        pygame.display.update()

        clock.tick(120)

gameloop()
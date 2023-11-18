import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Guy's Death")

# Colores
black = (0, 0, 0)

# Jugador
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 5

# Cargar imágenes
player_image_up = pygame.image.load("image/niño_up.png")
player_image_down = pygame.image.load("image/niño_down.png")
player_image_left = pygame.image.load("image/niño_left.png")
player_image_right = pygame.image.load("image/niño_right.png")

# Cambiar el tamaño de las imágenes
player_image_up = pygame.transform.scale(player_image_up, (player_size, player_size))
player_image_down = pygame.transform.scale(player_image_down, (player_size, player_size))
player_image_left = pygame.transform.scale(player_image_left, (player_size, player_size))
player_image_right = pygame.transform.scale(player_image_right, (player_size, player_size))

# Inicializar la imagen actual del jugador
player_image = player_image_up

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover el jugador y cambiar la imagen
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        player_image = player_image_left
    if keys[pygame.K_RIGHT] and player_x < width - player_size:
        player_x += player_speed
        player_image = player_image_right
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
        player_image = player_image_up
    if keys[pygame.K_DOWN] and player_y < height - player_size:
        player_y += player_speed
        player_image = player_image_down

    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar al jugador
    screen.blit(player_image, (player_x, player_y))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.Clock().tick(30)

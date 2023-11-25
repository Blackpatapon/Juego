import pygame
import sys
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FNAF 2 Mini Game')

# Colores
black = (0, 0, 0)
white = (255, 255, 255)

# Jugador
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height // 2 - player_size // 2

# Enemigo
enemy_size = 50
enemy_x = random.randint(0, screen_width - enemy_size)
enemy_y = random.randint(0, screen_height - enemy_size)

# Sonidosjusta la ruta del archivo de sonido

# Loop principal del juego
clock = pygame.time.Clock()
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= 5
    if keys[pygame.K_RIGHT]:
        player_x += 5
    if keys[pygame.K_UP]:
        player_y -= 5
    if keys[pygame.K_DOWN]:
        player_y += 5

    # Verificar colisión con el enemigo
    if (
        player_x < enemy_x + enemy_size
        and player_x + player_size > enemy_x
        and player_y < enemy_y + enemy_size
        and player_y + player_size > enemy_y
    ):
        print("Game Over")
        time.sleep(2)
        game_over = True

    # Dibujar en la pantalla
    screen.fill(black)
    pygame.draw.rect(screen, white, [player_x, player_y, player_size, player_size])
    pygame.draw.rect(screen, white, [enemy_x, enemy_y, enemy_size, enemy_size])

    pygame.display.update()

    clock.tick(30)

# Salir del juego
pygame.quit()
sys.exit()

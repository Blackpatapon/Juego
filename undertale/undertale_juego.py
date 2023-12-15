import pygame
import sys
import serial

# Inicializar pygame
pygame.init()

# Obtener información de la pantalla del dispositivo
screen_info = pygame.display.Info()

# Configuración de la pantalla
width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Juego")

# Colores
black = (0, 0, 0)

# Jugador
player_size = 50
player_x = width // 2 - player_size // 2
player_y = height // 2 - player_size // 2
player_speed = 100

# Cargar imagen del jugador
player_image = pygame.image.load("images/corazon.png")
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Inicializar puerto serie
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplaza 'COM3' con el puerto correcto

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Leer datos del puerto serie
    data = ser.read().decode('latin-1')  # Cambia a 'latin-1' para admitir todos los bytes

    # Mover el jugador según los datos recibidos
    if data == 'L' and player_x > 0:
        player_x -= player_speed
    if data == 'R' and player_x < width - player_size:
        player_x += player_speed
    if data == 'U' and player_y > 0:
        player_y -= player_speed
    if data == 'D' and player_y < height - player_size:
        player_y += player_speed

    # Asegurarse de que el jugador no se salga de los límites de la pantalla
    player_x = max(0, min(player_x, width - player_size))
    player_y = max(0, min(player_y, height - player_size))

    # Limpiar la pantalla
    screen.fill(black)

    # Dibujar al jugador
    screen.blit(player_image, (player_x, player_y))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    pygame.time.Clock().tick(30)
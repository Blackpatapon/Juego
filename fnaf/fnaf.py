import pygame
import sys
import random
import time

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Give Life')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Sonidos
pygame.mixer.init()
interference_sound = pygame.mixer.Sound('sound/interferencia.mp3')  # Ajusta la ruta del archivo de sonido

# Reproducir sonido de interferencia
interference_sound.play()

# Mostrar estática de color rojo durante la interferencia
for _ in range(90):  # 90 frames (3 segundos a 30 fps)
    screen.fill(red if random.randint(0, 1) == 0 else black)
    pygame.display.update()

time.sleep(3)  # Esperar 3 segundos

# Detener sonido de interferencia
interference_sound.stop()

# Puppet
puppet_size = 100
puppet_image_left = pygame.image.load('image/puppet_left.png')
puppet_image_right = pygame.image.load('image/puppet_right.png')
puppet_image_left = pygame.transform.scale(puppet_image_left, (puppet_size, puppet_size))
puppet_image_right = pygame.transform.scale(puppet_image_right, (puppet_size, puppet_size))
puppet_image = puppet_image_left
puppet_x = screen_width // 2 - puppet_size // 2
puppet_y = screen_height // 2 - puppet_size // 2

# Niños
niño_size = 50
niño_images = [
    pygame.image.load('image/niños.png'),  # Ajusta la ruta de la imagen del niño 1
    pygame.image.load('image/niños.png'),  # Ajusta la ruta de la imagen del niño 2
    pygame.image.load('image/niños.png'),  # Ajusta la ruta de la imagen del niño 3
    pygame.image.load('image/niños.png')   # Ajusta la ruta de la imagen del niño 4
]

# Imagen específica junto a los niños
bonus_image = pygame.image.load('image/regalo.png')  # Ajusta la ruta de la imagen específica

new_images = [
    pygame.image.load('image/freddy_head.png'),
    pygame.image.load('image/bonie_head.png'),
    pygame.image.load('image/chica_head.png'),
    pygame.image.load('image/foxy_head.png')
]

new_images = [pygame.transform.scale(img, (niño_size, niño_size)) for img in new_images]
new_images_positions = [None] * 4

niños = []
for i, position in enumerate([(50, 100), (screen_width - niño_size - 50, 100),
                              (50, screen_height - niño_size - 50), (screen_width - niño_size - 50, screen_height - niño_size - 50)]):
    niños.append({
        'x': position[0],
        'y': position[1],
        'size': niño_size,
        'image': pygame.transform.scale(niño_images[i], (niño_size, niño_size)),
        'bonus': pygame.transform.scale(bonus_image, (niño_size, niño_size)),  # Imagen específica junto al niño
        'bonus_position': None  # Posición inicial sin imagen
    })

# Sonidos
footstep_sound = pygame.mixer.Sound('sound/found_puppet.mp3')
laugh_sound = pygame.mixer.Sound('sound/FNAF2_Jumpscare_Sound.mp3')

# Música de fondo
pygame.mixer.music.load('sound/found_puppet.mp3')  # Ajusta la ruta del archivo de música
pygame.mixer.music.play(-1)  # -1 significa reproducir en bucle

# Tamaño del cuadro con bordes blancos
cuadro_x = 50
cuadro_y = 100
cuadro_width = screen_width - cuadro_x * 2
cuadro_height = screen_height - 150

# Separación para el texto
separacion_texto = 20

# Fuente para el texto
font_size = 55
font = pygame.font.Font(None, font_size)

# Tiempo de espera después de que todas las imágenes específicas aparezcan
tiempo_espera = 2  # segundos
tiempo_inicial = None

tiempo_inicial_bonus = None
tiempo_inicial_new_images = None

# Loop principal del juego
clock = pygame.time.Clock()
game_over = False

# Loop principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and puppet_x > cuadro_x:
        puppet_x -= 5
        puppet_image = puppet_image_left
    if keys[pygame.K_RIGHT] and puppet_x < cuadro_x + cuadro_width - puppet_size:
        puppet_x += 5
        puppet_image = puppet_image_right
    if keys[pygame.K_UP] and puppet_y > cuadro_y:
        puppet_y -= 5
    if keys[pygame.K_DOWN] and puppet_y < cuadro_y + cuadro_height - puppet_size:
        puppet_y += 5

    # Verificar colisión con los niños y mostrar imagen específica junto a ellos dentro del cuadro
    for niño in niños:
        if (
            puppet_x < niño['x'] + niño['size']
            and puppet_x + puppet_size > niño['x']
            and puppet_y < niño['y'] + niño['size']
            and puppet_y + puppet_size > niño['y']
        ):
            if niño['bonus_position'] is None:
                niño['bonus_position'] = (niño['x'] - niño['size'], niño['y']) if niño['x'] > screen_width / 2 else (niño['x'] + niño['size'], niño['y'])
        elif niño['bonus_position'] is not None:
            # La imagen específica permanece si ya ha aparecido
            pass

    # Verificar si todas las imágenes específicas han aparecido
    todas_aparecidas_bonus = all(niño['bonus_position'] is not None for niño in niños)

    # Si todas han aparecido, esperar 2 segundos y quitar las bonus_images
    if todas_aparecidas_bonus and tiempo_inicial_bonus is None:
        tiempo_inicial_bonus = time.time()

    if tiempo_inicial_bonus is not None and time.time() - tiempo_inicial_bonus > tiempo_espera:
        for niño in niños:
            niño['bonus_position'] = None
        tiempo_inicial_bonus = None

        # Si es la segunda vez que bonus_image desaparece, mostrar nuevas imágenes
        if tiempo_inicial_new_images is None:
            tiempo_inicial_new_images = time.time()

    # Si han pasado 2 segundos desde que bonus_image desapareció por segunda vez, mostrar nuevas imágenes
    if tiempo_inicial_new_images is not None and time.time() - tiempo_inicial_new_images > tiempo_espera:
        for i, niño in enumerate(niños):
            new_images_positions[i] = niño['bonus_position']

    # Dibujar en pantalla
    screen.fill(black)
    screen.blit(puppet_image, (puppet_x, puppet_y))

    for i, niño in enumerate(niños):
        screen.blit(niño['image'], (niño['x'], niño['y']))
        if niño['bonus_position'] is not None and cuadro_x < niño['bonus_position'][0] < cuadro_x + cuadro_width:
            if new_images_positions[i] is None:
                screen.blit(niño['bonus'], niño['bonus_position'])

        # Dibujar nuevas imágenes
        if new_images_positions[i] is not None:
            screen.blit(new_images[i], new_images_positions[i])

    # Dibujar el cuadro con bordes blancos
    pygame.draw.rect(screen, white, (cuadro_x, cuadro_y, cuadro_width, cuadro_height), 2)

    # Dibujar texto
    text = font.render("0100 GIVE LIFE", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, cuadro_y - separacion_texto - text.get_height() // 2))
    screen.blit(text, text_rect)

    pygame.display.update()

    clock.tick(30)

    # Verificar si la música ha terminado y volver a reproducirla
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

pygame.mixer.music.stop()  # Detener la música al salir del bucle principal
pygame.quit()
sys.exit()
import pygame
import sys
import random
import time

pygame.init()

#Pantalla del juego
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Give Life')
# Icono del menú
icon = pygame.image.load("image/icono.png")
pygame.display.set_icon(icon)

#Colores
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#Sonidos
pygame.mixer.init()
interference_sound = pygame.mixer.Sound('sound/interferencia.mp3')
background_sound = pygame.mixer.music
background_sound.load('sound/found_puppet.mp3')
jumpsacare_sound = pygame.mixer.Sound('sound/FNAF2_Jumpscare_Sound.mp3')

#Sonido de Interferencia
interference_sound.play()

#Mostrar interferencia
for _ in range(90):
    screen.fill(red if random.randint(0, 1) == 0 else black)
    pygame.display.update()

#Esperar 3 segundos
time.sleep(3)

#Detener sonido de interferencia
interference_sound.stop()

#Tamaño y Posicipn de Puppet
puppet_size = 100
puppet_image_left = pygame.image.load('image/puppet_left.png')
puppet_image_right = pygame.image.load('image/puppet_right.png')
puppet_image_left = pygame.transform.scale(puppet_image_left, (puppet_size, puppet_size))
puppet_image_right = pygame.transform.scale(puppet_image_right, (puppet_size, puppet_size))
puppet_image = puppet_image_right
puppet_x = screen_width // 2 - puppet_size // 2
puppet_y = screen_height // 2 - puppet_size // 2

#Tamaño y posicion de los niños
niño_size = 50
niño_images = [
    pygame.image.load('image/niños.png'),
    pygame.image.load('image/niños.png'),
    pygame.image.load('image/niños.png'),
    pygame.image.load('image/niños.png')
]

#Tamaño y posicion del regalo
regalo_image = pygame.image.load('image/regalo.png')

#Tamaño y posicion de los animatronicos
animatronicos_images = [
    pygame.image.load('image/freddy_head.png'),
    pygame.image.load('image/bonie_head.png'),
    pygame.image.load('image/chica_head.png'),
    pygame.image.load('image/foxy_head.png')
]

#Tamaño y posicion de golden freddy
golden_freddy_image = pygame.image.load('image/golden_freddy.png')
golden_freddy_original_size = 10
golden_freddy_size = golden_freddy_original_size
golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2, screen_height // 2 - golden_freddy_size // 2]

# Velocidad de crecimiento
growth_speed = 1

#Aparicion de las mascaras
animatronicos_images = [pygame.transform.scale(img, (int(niño_size * 1.5), int(niño_size * 1))) for img in animatronicos_images]
animatronicos_positions = [None] * 4

#Posicion de los niños
niños = []
for i, position in enumerate([(50, 100), (screen_width - niño_size - 50, 100),
                              (50, screen_height - niño_size - 50), (screen_width - niño_size - 50, screen_height - niño_size - 50)]):
    niños.append({
        'x': position[0],
        'y': position[1],
        'size': niño_size,
        'image': pygame.transform.scale(niño_images[i], (niño_size, niño_size)),
        'regalo': pygame.transform.scale(regalo_image, (niño_size, niño_size)),
        'regalo_position': None
    })

#Found me
background_sound.play(-1)

#Cuadro de movimiento
cuadro_x = 50
cuadro_y = 100
cuadro_width = screen_width - cuadro_x * 2
cuadro_height = screen_height - 150

#Espacios del texto
separacion_texto = 20

#Tamaño del texto
font_size = 55
font = pygame.font.Font(None, font_size)

#Velocidad de crecimiento
growth_speed = 50

#Tiempos de espera
tiempo_espera = 1
tiempo_espera_gf = 1
tiempo_inicial = None

tiempo_inicial_regalo = None
tiempo_inicial_animatronicos = None
tiempo_inicial_gf = None

#Velocidad del juego
clock = pygame.time.Clock()

#Estado del juego
game_over = False
play_jumpsacare_sound = True

#Numero de "Give Life"
give_life_number = 100

# Bucle principal del juego
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    #Teclas para mover a Puppet
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

    #Acercamiento de Puppet a los niños
    for niño in niños:
        if (
            puppet_x < niño['x'] + niño['size']
            and puppet_x + puppet_size > niño['x']
            and puppet_y < niño['y'] + niño['size']
            and puppet_y + puppet_size > niño['y']
        ):
            if niño['regalo_position'] is None:
                niño['regalo_position'] = (niño['x'] - niño['size'], niño['y']) if niño['x'] > screen_width / 2 else (
                    niño['x'] + niño['size'], niño['y'])
                give_life_number += 100
        elif niño['regalo_position'] is not None:
            pass

    #Jumpscare de golden freddy
    if tiempo_inicial_gf is not None:
        tiempo_transcurrido_gf = time.time() - tiempo_inicial_gf

        if tiempo_transcurrido_gf <= tiempo_espera_gf:
            golden_freddy_size += growth_speed

            golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2,
                                      screen_height // 2 - golden_freddy_size // 2]

            screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)),
                        golden_freddy_position)

            if play_jumpsacare_sound:
                jumpsacare_sound.play()
                play_jumpsacare_sound = False

    #Los regalos aparecen
    todas_aparecidas_regalo = all(niño['regalo_position'] is not None for niño in niños)

    #Tiempo de aparicion de los regalos
    if todas_aparecidas_regalo and tiempo_inicial_regalo is None:
        tiempo_inicial_regalo = time.time()

    #Borrar regalos y aparecer mascaras
    if tiempo_inicial_regalo is not None and time.time() - tiempo_inicial_regalo > tiempo_espera:
        for niño in niños:
            niño['regalo_position'] = None
        tiempo_inicial_regalo = None

        if tiempo_inicial_animatronicos is None:
            tiempo_inicial_animatronicos = time.time()

    #Tiempo de aparicion de las mascaras
    if tiempo_inicial_animatronicos is not None and time.time() - tiempo_inicial_animatronicos > tiempo_espera:
        for i, niño in enumerate(niños):
            animatronicos_positions[i] = niño['regalo_position']

        #Inicia jumpscare de golden freddy
        if all(position is not None for position in animatronicos_positions) and tiempo_inicial_gf is None:
            tiempo_inicial_gf = time.time()

    #Crecimiento del jumpscare
    if tiempo_inicial_gf is not None:
        tiempo_transcurrido_gf = time.time() - tiempo_inicial_gf

        if tiempo_transcurrido_gf <= tiempo_espera_gf:
            golden_freddy_size += growth_speed

            golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2,
                                      screen_height // 2 - golden_freddy_size // 2]

            screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)),
                        golden_freddy_position)

    # Limpiar pantalla
    screen.fill(black)

    #Aparicion de Puppet
    screen.blit(puppet_image, (puppet_x, puppet_y))

    #Niños y regalos en el cuadro
    for i, niño in enumerate(niños):
        screen.blit(niño['image'], (niño['x'], niño['y']))
        if niño['regalo_position'] is not None and cuadro_x < niño['regalo_position'][0] < cuadro_x + cuadro_width:
            if animatronicos_positions[i] is None:
                screen.blit(niño['regalo'], niño['regalo_position'])

        if animatronicos_positions[i] is not None:
            screen.blit(animatronicos_images[i], animatronicos_positions[i])

    #Jumpscare con sonido de fondo
    if tiempo_inicial_gf is not None and tiempo_transcurrido_gf <= tiempo_espera_gf:
        screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)),
                    golden_freddy_position)

    #Borde del cuadro
    pygame.draw.rect(screen, white, (cuadro_x, cuadro_y, cuadro_width, cuadro_height), 2)

    #Desaparecer el jumpscare
    if tiempo_inicial_gf is not None and tiempo_transcurrido_gf > tiempo_espera_gf:
        if tiempo_inicial is None:
            tiempo_inicial = time.time()

    #Terminar el juego
    if tiempo_inicial is not None and time.time() - tiempo_inicial > 1:
        interference_sound.play()

        for _ in range(90):
            screen.fill(red if random.randint(0, 1) == 0 else black)
            pygame.display.update()

        time.sleep(1)

        interference_sound.stop()

        game_over = True

    #Texto superior
    text = font.render(f"{give_life_number:04d} GIVE LIFE", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, cuadro_y - separacion_texto - text.get_height() // 2))
    screen.blit(text, text_rect)

    #Actualizar
    pygame.display.update()

    #Velocidad del juego
    clock.tick(30)

    #Reproducir musica al terminar
    if not background_sound.get_busy():
        background_sound.play()
    
    # Pregunta para volver a jugar
    if tiempo_inicial is not None and time.time() - tiempo_inicial > 1:
        interference_sound.play()

        for _ in range(90):
            screen.fill(red if random.randint(0, 1) == 0 else black)
            pygame.display.update()

        time.sleep(1)

        interference_sound.stop()

        # Mostrar la pregunta
        font_question = pygame.font.Font(None, font_size)
        question_text = font_question.render("¿QUIERES VOLVER A JUGAR? (Y/N)", True, white)
        question_rect = question_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(question_text, question_rect)
        pygame.display.update()

        # Esperar la respuesta
        waiting_for_response = True
        while waiting_for_response:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        # Reiniciar el juego
                        interference_sound.stop()
                        game_over = False
                        tiempo_inicial = None
                        tiempo_inicial_gf = None
                        tiempo_inicial_regalo = None
                        tiempo_inicial_animatronicos = None
                        give_life_number = 100
                        golden_freddy_size = golden_freddy_original_size
                        play_jumpsacare_sound = True  # Reiniciar la variable
                        for niño in niños:
                            niño['regalo_position'] = None
                        for i in range(4):
                            animatronicos_positions[i] = None
                        background_sound.play(-1)
                        waiting_for_response = False
                    elif event.key == pygame.K_n:
                        # Salir del juego
                        interference_sound.stop()
                        game_over = True
                        waiting_for_response = False

# Cerrar
background_sound.stop()
pygame.quit()
sys.exit()
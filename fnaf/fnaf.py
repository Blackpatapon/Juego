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
interference_sound = pygame.mixer.Sound('sound/interferencia.mp3')
footstep_sound = pygame.mixer.Sound('sound/found_puppet.mp3')
laugh_sound = pygame.mixer.Sound('sound/FNAF2_Jumpscare_Sound.mp3')

interference_sound.play()

for _ in range(90):
    screen.fill(red if random.randint(0, 1) == 0 else black)
    pygame.display.update()

time.sleep(3)

interference_sound.stop()

puppet_size = 100
puppet_image_left = pygame.image.load('image/puppet_left.png')
puppet_image_right = pygame.image.load('image/puppet_right.png')
puppet_image_left = pygame.transform.scale(puppet_image_left, (puppet_size, puppet_size))
puppet_image_right = pygame.transform.scale(puppet_image_right, (puppet_size, puppet_size))
puppet_image = puppet_image_left
puppet_x = screen_width // 2 - puppet_size // 2
puppet_y = screen_height // 2 - puppet_size // 2

niño_size = 50
niño_images = [
    pygame.image.load('image/niños.png'), 
    pygame.image.load('image/niños.png'),
    pygame.image.load('image/niños.png'),
    pygame.image.load('image/niños.png')
]

bonus_image = pygame.image.load('image/regalo.png')

new_images = [
    pygame.image.load('image/freddy_head.png'),
    pygame.image.load('image/bonie_head.png'),
    pygame.image.load('image/chica_head.png'),
    pygame.image.load('image/foxy_head.png')
]

golden_freddy_image = pygame.image.load('image/golden_freddy.png')
golden_freddy_original_size = 10 
golden_freddy_size = golden_freddy_original_size
golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2, screen_height // 2 - golden_freddy_size // 2]

growth_speed = 1

new_images = [pygame.transform.scale(img, (int(niño_size * 1.5), int(niño_size * 1))) for img in new_images]
new_images_positions = [None] * 4

niños = []
for i, position in enumerate([(50, 100), (screen_width - niño_size - 50, 100),
                              (50, screen_height - niño_size - 50), (screen_width - niño_size - 50, screen_height - niño_size - 50)]):
    niños.append({
        'x': position[0],
        'y': position[1],
        'size': niño_size,
        'image': pygame.transform.scale(niño_images[i], (niño_size, niño_size)),
        'bonus': pygame.transform.scale(bonus_image, (niño_size, niño_size)),
        'bonus_position': None
    })

pygame.mixer.music.load('sound/found_puppet.mp3')
pygame.mixer.music.play(-1)

cuadro_x = 50
cuadro_y = 100
cuadro_width = screen_width - cuadro_x * 2
cuadro_height = screen_height - 150

separacion_texto = 20

font_size = 55
font = pygame.font.Font(None, font_size)

growth_speed = 50

tiempo_espera = 1
tiempo_espera_gf = 1
tiempo_inicial = None

tiempo_inicial_bonus = None
tiempo_inicial_new_images = None
tiempo_inicial_gf = None

clock = pygame.time.Clock()
game_over = False
play_laugh_sound = True  

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
            pass
    
    if tiempo_inicial_gf is not None:
        tiempo_transcurrido_gf = time.time() - tiempo_inicial_gf

        if tiempo_transcurrido_gf <= tiempo_espera_gf:
            golden_freddy_size += growth_speed

            golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2, screen_height // 2 - golden_freddy_size // 2]

            screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)), golden_freddy_position)

            if play_laugh_sound:
                laugh_sound.play()
                play_laugh_sound = False

    todas_aparecidas_bonus = all(niño['bonus_position'] is not None for niño in niños)

    if todas_aparecidas_bonus and tiempo_inicial_bonus is None:
        tiempo_inicial_bonus = time.time()

    if tiempo_inicial_bonus is not None and time.time() - tiempo_inicial_bonus > tiempo_espera:
        for niño in niños:
            niño['bonus_position'] = None
        tiempo_inicial_bonus = None

        if tiempo_inicial_new_images is None:
            tiempo_inicial_new_images = time.time()

    if tiempo_inicial_new_images is not None and time.time() - tiempo_inicial_new_images > tiempo_espera:
        for i, niño in enumerate(niños):
            new_images_positions[i] = niño['bonus_position']

        if all(position is not None for position in new_images_positions) and tiempo_inicial_gf is None:
            tiempo_inicial_gf = time.time()

    if tiempo_inicial_gf is not None:
        tiempo_transcurrido_gf = time.time() - tiempo_inicial_gf

        if tiempo_transcurrido_gf <= tiempo_espera_gf:
            golden_freddy_size += growth_speed

            golden_freddy_position = [screen_width // 2 - golden_freddy_size // 2, screen_height // 2 - golden_freddy_size // 2]

            screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)), golden_freddy_position)

    screen.fill(black)

    screen.blit(puppet_image, (puppet_x, puppet_y))

    for i, niño in enumerate(niños):
        screen.blit(niño['image'], (niño['x'], niño['y']))
        if niño['bonus_position'] is not None and cuadro_x < niño['bonus_position'][0] < cuadro_x + cuadro_width:
            if new_images_positions[i] is None:
                screen.blit(niño['bonus'], niño['bonus_position'])

        if new_images_positions[i] is not None:
            screen.blit(new_images[i], new_images_positions[i])

    if tiempo_inicial_gf is not None and tiempo_transcurrido_gf <= tiempo_espera_gf:
        screen.blit(pygame.transform.scale(golden_freddy_image, (golden_freddy_size, golden_freddy_size)), golden_freddy_position)

    pygame.draw.rect(screen, white, (cuadro_x, cuadro_y, cuadro_width, cuadro_height), 2)

    if tiempo_inicial_gf is not None and tiempo_transcurrido_gf > tiempo_espera_gf:
        if tiempo_inicial is None:
            tiempo_inicial = time.time()

    if tiempo_inicial is not None and time.time() - tiempo_inicial > 1:
        interference_sound.play()

        for _ in range(90):
            screen.fill(red if random.randint(0, 1) == 0 else black)
            pygame.display.update()

        time.sleep(1)

        interference_sound.stop()

        game_over = True

    text = font.render("0100 GIVE LIFE", True, white)
    text_rect = text.get_rect(center=(screen_width // 2, cuadro_y - separacion_texto - text.get_height() // 2))
    screen.blit(text, text_rect)

    pygame.display.update()

    clock.tick(30)

    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
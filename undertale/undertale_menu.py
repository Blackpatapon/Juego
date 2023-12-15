import pygame
import sys
import time
import subprocess
import serial

# Inicializar Pygame
pygame.init()

# Obtener la información de la pantalla del dispositivo
screen_info = pygame.display.Info()

# Definir el ancho y alto de la pantalla
width = screen_info.current_w
height = screen_info.current_h

# Colores
white = (255, 255, 255)
yellow = (255, 255, 0)

# Crear la ventana de Pygame en modo pantalla completa
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Establecer el título de la ventana
pygame.display.set_caption("Botones Pygame")

# Cargar la imagen de espera
waiting_image = pygame.image.load('images/undertale_letras.png')  # Reemplaza 'path/to/waiting_image.png' con la ruta de tu imagen

# Redimensionar la imagen de espera
waiting_image = pygame.transform.scale(waiting_image, (width, height))

# Mostrar la imagen de espera durante 3 segundos
screen.blit(waiting_image, (0, 0))
pygame.display.flip()
time.sleep(3)

# Inicializar el reproductor de música
pygame.mixer.init()

# Cargar la canción
pygame.mixer.music.load('sound/undertale_menu.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Cargar las imágenes
image_top = pygame.image.load('images/pilares_menu.png')  # Reemplaza 'path/to/top_image.png' con la ruta de tu imagen
image_bottom = pygame.image.load('images/toriel_menu.png')  # Reemplaza 'path/to/bottom_image.png' con la ruta de tu imagen

# Redimensionar las imágenes
new_width_top = int(width * 0.3)
new_height_top = int(new_width_top * image_top.get_height() / image_top.get_width())
image_top = pygame.transform.scale(image_top, (new_width_top, new_height_top))

new_width_bottom = int(width * 0.4)
new_height_bottom = int(new_width_bottom * image_bottom.get_height() / image_bottom.get_width())
image_bottom = pygame.transform.scale(image_bottom, (new_width_bottom, new_height_bottom))

# Definir las propiedades de los botones
button_width = 150
button_height = 150
button_spacing = 20

button_x_jugar = (width - (2 * button_width + button_spacing)) // 2
button_x_salir = button_x_jugar + button_width + button_spacing
button_y = (height - button_height) // 2

button_text_color_default = white
button_text_color_selected = yellow

selected_button = "Jugar"

# Conexión con el puerto serial del Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplaza 'COMX' con el puerto al que está conectado tu Arduino

# Función para salir del programa
def salir():
    pygame.quit()
    sys.exit()

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Leer desde el puerto serial del Arduino
    if arduino.in_waiting > 0:
        button_press = arduino.read().decode().strip()
        
        if button_press == 'L':  # Pulsador izquierdo
            selected_button = "Jugar"
        elif button_press == 'R':  # Pulsador derecho
            selected_button = "Salir"
        elif button_press == 'E':  # Pulsador de "Enter"
            if selected_button == "Jugar":
                # Lógica para el botón "Jugar" aquí si es necesario
                pygame.mixer.music.pause()  # Pausar la música del primer archivo
                subprocess.run(["python3", "undertale_juego.py"])  # Ejecutar el segundo archivo .py
                pygame.mixer.music.unpause()  # Reanudar la música del primer archivo después de ejecutar el segundo archivo
            elif selected_button == "Salir":
                salir()

    # Limpiar la pantalla
    screen.fill((0, 0, 0))

    # Dibujar botón "Jugar"
    font = pygame.font.Font(None, 36)
    jugar_text = font.render("Jugar", True, button_text_color_selected if selected_button == "Jugar" else button_text_color_default)
    screen.blit(jugar_text, (button_x_jugar + (button_width - jugar_text.get_width()) // 2, button_y))

    # Dibujar botón "Salir"
    salir_text = font.render("Salir", True, button_text_color_selected if selected_button == "Salir" else button_text_color_default)
    screen.blit(salir_text, (button_x_salir + (button_width - salir_text.get_width()) // 2, button_y))

    # Agregar texto centrado entre los botones y el borde de la ventana
    info_font = pygame.font.Font(None, 48)
    info_text = info_font.render("UNDERTALE", True, white)
    text_x = (width - info_text.get_width()) // 2
    text_y = button_y - (info_text.get_height() + 20)
    screen.blit(info_text, (text_x, text_y))

    # Agregar segundo texto centrado encima del primer texto
    second_info_text = info_font.render("LV1", True, white)
    second_text_x = (width - second_info_text.get_width()) // 2
    second_text_y = text_y - (second_info_text.get_height() + 10)
    screen.blit(second_info_text, (second_text_x, second_text_y))

    # Obtener el tamaño de las imágenes
    image_top_width, image_top_height = image_top.get_size()
    image_bottom_width, image_bottom_height = image_bottom.get_size()

    # Dibujar la imagen superior centrada
    screen.blit(image_top, ((width - image_top_width) // 2, 10))

    # Ajustar la posición de la imagen inferior
    image_bottom_y = height - image_bottom_height - 30  # Ajusta la posición de acuerdo a tus necesidades
    screen.blit(image_bottom, ((width - image_bottom_width) // 2, image_bottom_y))

    # Agregar texto gris debajo de la imagen inferior
    bottom_text = info_font.render("UNDERTALE V1.00 PYTHON BY LUIS", True, (100, 100, 100))
    screen.blit(bottom_text, ((width - bottom_text.get_width()) // 2, image_bottom_y + image_bottom_height + 10))

    # Actualizar la pantalla
    pygame.display.flip()
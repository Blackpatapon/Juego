import pygame
import sys
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

# Inicializar el reproductor de música
pygame.mixer.init()

# Cargar la canción
pygame.mixer.music.load('sound/undertale_menu.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Inicializar la conexión serial con Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Reemplaza 'COM3' con el puerto COM correcto

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

    # Leer los pulsadores desde Arduino
    pulsadores = ser.readline().decode().strip().split(',')
    if len(pulsadores) == 5:
        pulsador_jugar, pulsador_salir, pulsador_izquierda, pulsador_derecha, pulsador_enter = map(int, pulsadores)

        if pulsador_izquierda:
            selected_button = "Jugar"
        elif pulsador_derecha:
            selected_button = "Salir"
        elif pulsador_enter:
            if selected_button == "Jugar":
                # Lógica para el botón "Jugar" aquí si es necesario
                pygame.mixer.music.pause()
                subprocess.run(["python3", "undertale_juego.py"])
                pygame.mixer.music.unpause()
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

    # Actualizar la pantalla
    pygame.display.flip()

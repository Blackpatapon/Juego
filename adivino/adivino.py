import pygame
import random
import sys

pygame.init()

ventana = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Adivina el número")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

fuente = pygame.font.Font(None, 36)

numero_objetivo = random.randint(1, 100)

intentos = 0
mensaje = "Adivina el número entre 1 y 100: "
entrada = ""

jugando = True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando = False
        if intentos < 5:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    jugando = False
                elif evento.key == pygame.K_RETURN:
                    if entrada:
                        intento = int(entrada)
                        intentos += 1
                        if intento == numero_objetivo:
                            mensaje = f"¡Felicidades! Adivinaste el número {numero_objetivo}."
                            pygame.time.wait(2000)
                            jugando = False
                        else:
                            mensaje = f"El número es mayor." if intento < numero_objetivo else f"El número es menor."
                            if intentos < 5:
                                mensaje += f" Intentos restantes: {5 - intentos} \n"
                        entrada = ""
                elif evento.key == pygame.K_BACKSPACE:
                    entrada = entrada[:-1]
                else:
                    entrada += evento.unicode
        else:
            mensaje = "Se acabaron los intentos El número era " + str(numero_objetivo)
            jugando = False

    ventana.fill(BLANCO)
    
    texto = fuente.render(mensaje + entrada, True, NEGRO)
    rectangulo = texto.get_rect(center=ventana.get_rect().center)
    ventana.blit(texto, rectangulo)
    
    pygame.display.flip()

pygame.time.delay(3000)
sys.exit()
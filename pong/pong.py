import pygame
import time

pygame.init()

window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong Game')

white = (255, 255, 255)
black = (0, 0, 0)

bat_width, bat_height = 100, 20
batX = (window_width - bat_width) // 2
batY = window_height - bat_height - 10
ball_width, ball_height = 20, 20
ballX = window_width // 2
ballY = window_height // 2
ballMoveX = 5
ballMoveY = 5
rightPressed = False
leftPressed = False
gameOver = False
score = 0

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def main():
    global batX, ballX, ballY, ballMoveX, ballMoveY, rightPressed, leftPressed, gameOver, score

    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    leftPressed = True
                if event.key == pygame.K_RIGHT:
                    rightPressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    leftPressed = False
                if event.key == pygame.K_RIGHT:
                    rightPressed = False

        moveBat()
        moveBall()
        locateObjects()
        checkGameOver()

        clock.tick(60)

    display_end_message()

def display_end_message():
    global score

    end_message = font.render("Perdiste. Puntuación: " + str(score), True, black)
    text_rect = end_message.get_rect(center=(window_width // 2, window_height // 2))
    window.blit(end_message, text_rect)
    pygame.display.update()

    end_time = pygame.time.get_ticks() + 2000
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  

    pygame.quit()

def moveBat():
    global batX

    inRangeLeft = batX > 0
    inRangeRight = batX < window_width - bat_width

    if rightPressed and inRangeRight:
        batX += 10
    if leftPressed and inRangeLeft:
        batX -= 10

def moveBall():
    global ballX, ballY, ballMoveX, ballMoveY, score

    ballX += ballMoveX
    ballY += ballMoveY

    touchingBat = (ballX > batX) and (ballX < batX + bat_width) and (ballY > batY)

    if ballX > window_width - ball_width or ballX < 0:
        ballMoveX = -ballMoveX
    if ballY < 0:
        ballMoveY = -ballMoveY
    if ballY > window_height:
        gameOver = True

    if touchingBat:
        ballMoveY = -ballMoveY
        score += 1

background_image = pygame.image.load("imagenes/forest.png")

def locateObjects():
    window.blit(background_image, (0, 0))
    
    pygame.draw.rect(window, black, (batX, batY, bat_width, bat_height))
    pygame.draw.ellipse(window, black, (ballX, ballY, ball_width, ball_height))

    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, black)
    window.blit(score_text, (10, 10))
    
    pygame.display.update()

def checkGameOver():
    global gameOver
    if ballY > batY + bat_height:
        gameOver = True

if __name__ == "__main__":
    main()

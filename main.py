import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runboy')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

back_surface = pygame.image.load('assets/background.png')
ground = pygame.image.load('assets/ground.png')
text_surface = test_font.render('Score: ', True, 'Green')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(back_surface, (0, 0))
    screen.blit(ground, (0, 320))
    screen.blit(ground, (400, 320))
    screen.blit(text_surface, (300, 25))

    pygame.display.update()
    clock.tick(60)


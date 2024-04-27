import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runboy')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)

back_surface = pygame.image.load('background.png').convert()
ground = pygame.image.load('ground.png').convert()
text_surface = test_font.render('Score: ', True, 'Green')

scorpion_surf = pygame.image.load('graphics/scorpion/scorpion1.png').convert_alpha()
scorpion_rect = scorpion_surf.get_rect(midbottom=(600, 320))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(back_surface, (0, 0))
    screen.blit(ground, (0, 320))
    screen.blit(ground, (400, 320))
    screen.blit(text_surface, (300, 25))

    scorpion_rect.x -= 5
    if scorpion_rect.right <= 0:
        scorpion_rect.left = 800
    screen.blit(scorpion_surf, scorpion_rect)
    screen.blit(player_surf, player_rect)

    pygame.display.update()
    clock.tick(60)


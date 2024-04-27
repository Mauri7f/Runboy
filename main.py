import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', True, ('Green'))
    score_rect = score_surf.get_rect(center=(400, 25))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 320:
                screen.blit(scorpion_surf, obstacle_rect)
            else:
                screen.blit(beast_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 320:
        player_surf = player_jump
    else:
        player_index += 0.2
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runboy')
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 50)
game_active = True
start_time = 0
score = 0

back_surface = pygame.image.load('background.png').convert()
ground = pygame.image.load('ground.png').convert()

# score_surf = test_font.render('Score: ', True, 'Green')
# score_rect = score_surf.get_rect(center=(400, 25))

# Obstacles
fiend_frame_1 = pygame.image.load('graphics/fiend/f_1.png').convert_alpha()
fiend_frame_2 = pygame.image.load('graphics/fiend/f_2.png').convert_alpha()
fiend_frames = [fiend_frame_1, fiend_frame_2]
fiend_frame_index = 0
fiend_surf = fiend_frames[fiend_frame_index]

beast_surf = pygame.image.load('graphics/beast/beast1.png').convert_alpha()

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 320))
player_gravity = 0

player_dead = pygame.image.load('graphics/player/player_dead.png').convert_alpha()
player_dead = pygame.transform.rotozoom(player_dead, 0, 2)
player_dead_rect = player_dead.get_rect(center=(400, 200))

game_name = test_font.render('You Have Died', True, (181, 2, 2))
game_name_rect = game_name.get_rect(center=(400, 70))

game_message = test_font.render('Press space to continue', True, (181, 2, 2))
game_message_rect = game_message.get_rect(center=(400, 370))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

scorpion_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(scorpion_animation_timer, 500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 320:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True

                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer and game_active:
                if randint(0,2):
                    obstacle_rect_list.append(fiend_surf.get_rect(bottomright=(randint(900, 1100), 320)))
                else:
                    obstacle_rect_list.append(beast_surf.get_rect(bottomright=(randint(900, 1100), 200)))
            if event.type == scorpion_animation_timer:
                if fiend_frame_index == 0:
                    fiend_frame_index = 1
                else: fiend_frame_index = 0
                scorpion_surf = fiend_frames[fiend_frame_index]

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground, (0, 320))
        screen.blit(ground, (400, 320))
        # pygame.draw.rect(screen, 'Black', score_rect)
        # pygame.draw.rect(screen, 'Black', score_rect, 20)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # scorpion_rect.x -= 5
        # if scorpion_rect.right <= 0:
        #     scorpion_rect.left = 800
        # screen.blit(scorpion_surf, scorpion_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 320:
            player_rect.bottom = 320
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((47, 7, 99))
        screen.blit(player_dead, player_dead_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 320)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', True, (181, 2, 2))
        score_message_rect = score_message.get_rect(center=(400, 320))
        screen.blit(score_message, score_message_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)


    pygame.display.update()
    clock.tick(60)


import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(150, 320))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 320:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 320:
            self.rect.bottom = 320

    def animation_state(self):
        if self.rect.bottom < 320:
            self.image = self.player_jump
        else:
            self.player_index += 0.2
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'beast':
            beast = pygame.image.load('graphics/beast/beast1.png')
            self.frames = [beast]
            y_pos = 210
        else:
            fiend_1 = pygame.image.load('graphics/fiend/f_1.png').convert_alpha()
            fiend_2 = pygame.image.load('graphics/fiend/f_2.png').convert_alpha()
            self.frames = [fiend_1, fiend_2]
            y_pos = 320

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


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


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True


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
bg_music = pygame.mixer.Sound('audio/music.mp3')
bg_music.play(loops=-1)
bg_music.set_volume(0.5)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

back_surface = pygame.image.load('background.png').convert()
ground = pygame.image.load('ground.png').convert()

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

fiend_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fiend_animation_timer, 500)

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
                obstacle_group.add(Obstacle(choice(['beast', 'fiend', 'fiend', 'fiend'])))

            if event.type == fiend_animation_timer:
                if fiend_frame_index == 0:
                    fiend_frame_index = 1
                else: fiend_frame_index = 0
                scorpion_surf = fiend_frames[fiend_frame_index]

    if game_active:
        screen.blit(back_surface, (0, 0))
        screen.blit(ground, (0, 320))
        screen.blit(ground, (400, 320))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

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


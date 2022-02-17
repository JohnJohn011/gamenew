import pygame  # import pygame, duh
from sys import exit  # exit the game




pygame.init()                                                   # init pygame will start pygame
screen = pygame.display.set_mode((800, 400))                    # Window size
pygame.display.set_caption('Snail It!')                         # Name of window
clock = pygame.time.Clock()                                     # Calls clock for Framerate
test_font = pygame.font.Font('font/Pixeltype.ttf', 80)          # Choose font if you want to use a words surface(should check if it can use system fonts)
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
gameover_font = pygame.font.Font('font/Pixeltype.ttf', 150)
game_active = True
start_time = 0

# Surfaces- bottom will be last to load

sky_surface = pygame.image.load('graphics/Sky.png').convert()   # pygame.image.load- load image from file in same folder always use .convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

title_surface = test_font.render('Snail It!', False, 'Black')      #('words', AA(smoothing), 'color')
title_rect = title_surface.get_rect(center = (400, 50))           # puts words into a rectangle

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()   # use alpha when?
player_rect = player_surface.get_rect(midbottom = (80, 300))        # .get_rect is calling player surface and forcing it into a rectangle so you can choose where it goes
player_gravity = 0

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surface.get_rect(bottomright = (600, 300))
snail_speed = 5

gameover_surf = gameover_font.render('GAME OVER!', False, 'Black')
gameover_rect = gameover_surf.get_rect(center = (400, 200))

key_press = 0

while True:                                                      # While True loop actually implements it
    for event in pygame.event.get():
        if player_rect.bottom == 300:
            key_press = 0
        if event.type == pygame.QUIT:
            pygame.quit()                                        # You have to call this or it will try to loop and break unless you use this function
            exit()                                               # Have to use this to break the loop using sys tools
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    key_press += 1
                if event.key == pygame.K_SPACE and key_press < 2:
                    player_gravity = -20
        #restart game after gameover
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                snail_speed = 5
                start_time = pygame.time.get_ticks()

    # Methods
    if game_active:
        screen.blit(sky_surface, (0, 0))                             # screen.blit (calls whatever surface you want, (sets the position)
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, 'White', title_rect)                # background fill color
        pygame.draw.rect(screen, 'White', title_rect, 10)            #border to make background bigger. add one more variable after to round corners
        screen.blit(title_surface, title_rect)
        current_time = pygame.time.get_ticks() - start_time
        score_surfs = score_font.render(f'{current_time}', False, 'Black')
        score_rect = score_surfs.get_rect(center = (400, 200))
        score_rect2 = score_surfs.get_rect(center = (400, 300))
        screen.blit(score_surfs, score_rect)

        snail_rect.x -= snail_speed                                           #Moves snail_rect
        if snail_rect.right <= 0:
            snail_rect.left = 800
            snail_speed += 1
            if snail_speed > 10:
                snail_speed -= 0.8

        screen.blit(snail_surface, snail_rect)                    #puts snail on surface

        #Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300      #puts player on ground, doesn't allow it to fall
        screen.blit(player_surface, player_rect)                    # puts player surface on screen

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    # game over screen
    else:
        screen.fill('Yellow')
        screen.blit(gameover_surf, gameover_rect)
        screen.blit(score_surfs, score_rect2)


    pygame.display.update()                                      # updates it every time the while loop runs
    clock.tick(60)                                               # Framerate

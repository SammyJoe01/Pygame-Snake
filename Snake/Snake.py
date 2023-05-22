import pygame, random

pygame.init()

#Set display surface
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake")

#Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

#Set game values
SNAKE_SIZE = 20

head_x = WINDOW_WIDTH//2
head_y = WINDOW_HEIGHT//2 + 100

snake_dx = 0
snake_dy = 0

score = 0

#Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PINK = (255,20,147)

#Set fonts
font = pygame.font.Font('/Users/sammymylove/Desktop/Pygame/Snake/AttackGraffiti.ttf', 40)

#Set text
title_text = font.render("Snake", True, PINK, None)
title_rect = title_text.get_rect()
title_rect.topleft = (350, 10)

score_text = font.render("Score: " + str(score), True, BLACK, WHITE)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("GAMEOVER", True, PINK, BLACK)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, PINK, BLACK)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

#Set sounds and music
pick_up_sound = pygame.mixer.Sound("/Users/sammymylove/Desktop/Pygame/Snake/snake.wav")

#Set images (For rectangle you need top-left x, top-left y, width, height)
apple_coord = (500,500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []

back_image = pygame.image.load("/Users/sammymylove/Desktop/Pygame/Snake/back.jpg")
back_rect = back_image.get_rect()
back_rect.topleft = (0,0)

#Loop
running = True
while running:
    #Check if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #Move Snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1*SNAKE_SIZE
                snake_dy = 0
            if event.key ==pygame.K_RIGHT:
                snake_dx = SNAKE_SIZE
                snake_dy = 0
            if event.key ==pygame.K_UP:
                snake_dx = 0
                snake_dy = -1*SNAKE_SIZE
            if event.key ==pygame.K_DOWN:
                snake_dx = 0
                snake_dy = SNAKE_SIZE
        
    #Add the head coordinate to the first index of the body coordinate list
    #This will essentilalyl move all of the snakes body by one position in the list
    body_coords.insert(0, head_coord)
    body_coords.pop()

    #Update x,y position snake head and make new coordinates
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    #Check for game over
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game untile the player presses a key, then reset the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0

                    head_x = WINDOW_WIDTH//2
                    head_y = WINDOW_HEIGHT//2 + 100
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
                    
                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0

                    is_paused = False
                #The play wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    #Check for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)

    #Update HUD
    score_text = font.render("Score: " + str(score), True, WHITE, BLACK)

    #Blit background
    display_surface.blit(back_image, back_rect)

    #Blit HUD 
    display_surface.blit(score_text,score_rect)
    display_surface.blit(title_text,title_rect)
    
    #Blit Assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    #Update display and tick the clock 
    pygame.display.update()
    clock.tick(FPS)


#End the game
pygame.quit()
import pygame


pygame.init()

display_width = 580
display_height = 510

black = (0, 0, 0)
white = (255, 255, 255)

red = (200, 0, 0)
green = (0, 200, 0)

bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

image_dir = 'assets/sprites/'

yellow_bird_mid = pygame.image.load(image_dir + 'yellowbird-midflap.png')
yellow_bird_up = pygame.image.load(image_dir + 'yellowbird-upflap.png')
yellow_bird_down = pygame.image.load(image_dir + 'yellowbird-downflap.png')
background_day = pygame.image.load(image_dir + 'background-day.png').convert()
green_pipe = pygame.image.load(image_dir + 'pipe-green.png')

FPS = 120


# class FlappyBird:
#     def __init__(self, pos_x, pos_y):
#         self.pos_x = pos_x
#         self.pos_y = pos_y
#         self.set_pos(self.pos_x, self.pos_y)
#
#     def move_up(self):
#         FlappyBird(self.pos_x, self.pos_y + 50)
#
#     def set_pos(self, pos_x, pos_y):
#         self.pos_y = pos_y
#         self.pos_x = pos_x
#         game_display.blit(yellow_bird_mid, (self.pos_x, self.pos_y))


def bird(pos_x, pos_y, bird_type=yellow_bird_mid):
    game_display.blit(bird_type, (pos_x, pos_y))


def pipe(pos_x, pos_y, reverse=False):
    if reverse:
        new_pipe = pygame.transform.flip(green_pipe, False, True)
    else:
        new_pipe = green_pipe
    game_display.blit(new_pipe, (pos_x, pos_y))


def game_loop():
    background_x = 0
    game_exit = False
    pos_x = (display_width * 0.1)
    pos_y = (display_height * 0.3)
    change_count = 0

    while not game_exit:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    change_count += 40
                    # game_exit = True

        rel_background_x = background_x % background_day.get_rect().width

        game_display.blit(background_day, (rel_background_x - background_day.get_rect().width, 0))
        game_display.blit(background_day, (rel_background_x + background_day.get_rect().width, 0))
        if rel_background_x < display_height:
            game_display.blit(background_day, (rel_background_x, 0))

        # debug for background placement
        # pygame.draw.line(game_display, (255, 0, 0), (rel_background_x, 0), (rel_background_x, display_height), 3)

        if change_count > 0:
            pos_change = -1
            change_count -= 1
            bird_type = yellow_bird_down
        else:
            pos_change = 1
            bird_type = yellow_bird_up

        pos_y += pos_change
        pipe(200, 40, reverse=True)
        pipe(100, 400, reverse=False)

        bird(pos_x, pos_y, bird_type)
        background_x -= 1
        pygame.display.update()
        clock.tick(FPS)


game_loop()

pygame.quit()
quit()

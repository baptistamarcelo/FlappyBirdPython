import random
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


def bird(pos_x, pos_y, bird_type=yellow_bird_mid):
    game_display.blit(bird_type, (pos_x, pos_y))


def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()


class Pipe:
    def __init__(self, pipe_1_pos_y):
        self.pipe_2_pos_y = display_height - (pipe_1_pos_y + 100)
        self.pipe_1_pos_y = (pipe_1_pos_y * -1)
        self.pipe_pos_x = 550
        self.pipe_collision_x = 0
        self.pipe_collision_y = 0

    def __new__(cls, *args, **kwargs):
        instance = super(Pipe, cls).__new__(cls)
        return instance


def hit():
    large_text = pygame.font.SysFont("comicsansms", 115)
    TextSurf, TextRect = text_objects("You Crashed", large_text)
    TextRect.center = ((display_width / 2), (display_height / 2))
    game_display.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(white)


def game_loop():
    background_x = 0
    game_exit = False
    pos_x = (display_width * 0.1)
    pos_y = (display_height * 0.3)
    change_count = 0
    pipe_spawn_count = 0
    pipe_speed = 1
    pipe_list = []
    pipe_pos_y_limit = 190

    while not game_exit:
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    change_count += 15
                    # game_exit = True

        rel_background_x = background_x % background_day.get_rect().width

        game_display.blit(background_day, (rel_background_x - background_day.get_rect().width, 0))
        game_display.blit(background_day, (rel_background_x + background_day.get_rect().width, 0))
        if rel_background_x < display_height:
            game_display.blit(background_day, (rel_background_x, 0))

        # debug for background placement
        # pygame.draw.line(game_display, (255, 0, 0), (rel_background_x, 0), (rel_background_x, display_height), 3)

        pipe_spawn_count += 1

        if change_count > 0:
            pos_change = -3
            change_count -= 1
            bird_type = yellow_bird_down
        else:
            pos_change = 1
            bird_type = yellow_bird_up

        if pipe_spawn_count % 250 == 0:
            pipe_spawn_count = 0
            pipe = Pipe(random.randint(0, pipe_pos_y_limit))
            pipe_list.append(pipe)

        for pipe in pipe_list:
            # debug pipe class
            # print("pipe 1 / 2: {} / {}".format(pipe.pipe_1_pos_y, pipe.pipe_2_pos_y))
            game_display.blit(pygame.transform.flip(green_pipe, False, True), (pipe.pipe_pos_x, pipe.pipe_1_pos_y))
            game_display.blit(green_pipe, (pipe.pipe_pos_x, pipe.pipe_2_pos_y))
            pipe.pipe_pos_x -= pipe_speed
            if pipe.pipe_pos_x == -50:
                pipe_list.remove(pipe)


        # debug green pipe position
        # game_display.blit(pygame.transform.flip(green_pipe, False, True), (500, 0))
        pos_y += pos_change

        bird(pos_x, pos_y, bird_type)
        background_x -= 1
        print("bird 1 / 2: {} / {}".format(pos_x, pos_y))
        if (pos_x, pos_y) in pipe_list:
            print("you hit a pipe!")
        pygame.display.update()
        clock.tick(FPS)


game_loop()

pygame.quit()
quit()

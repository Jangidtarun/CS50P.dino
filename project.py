import pygame
import random
import csv
from datetime import datetime
from constants import *


# Setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Dino Game")
SCREEN = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))
SCREEN.fill("white")
clock = pygame.time.Clock()


# Fonts
arial_b48 = pygame.font.SysFont('Arial', bold=True, size=48)
arial_36 = pygame.font.SysFont('Arial', size=36)
monospace_24 = pygame.font.SysFont('monospace', bold=False, size=16)


# Game State Variables
state = STARTING
dt = 0
enem_list = []
pygame.time.set_timer(ENEMY_SPAWN_EVENT, SPAWN_INTERVAL, loops=1)
score = 0
reference_time = pygame.time.get_ticks()


class Player(pygame.sprite.Sprite):
    """
    Player class for instantiating dear dino
    """

    def __init__(self, size:int = 50):

        super().__init__()
        self.size = size
        self.onground = True
        self.x = SC_WIDTH/4
        self.y = SC_HEIGHT/2
        self.velx = 0
        self.vely = 0
        self.accx = 0
        self.accy = 0
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def jump(self):
        if self.onground:
            self.vely = UPWARD_THRUST
            self.onground = False

    def move(self, dt):
        self.velx += self.accx*dt
        self.x += self.velx*dt

        if not self.onground:
            if self.vely < MAX_VEL:
                self.vely += (G)*dt
            self.y += self.vely*dt

            if self.y >= SC_CENTER.y:
                self.y = SC_CENTER.y
                self.vely = 0
                self.onground = True


        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.y == SC_CENTER.y:
            self.jump()

    def draw(self, surface):
        self.rect.center = (self.x, self.y)
        pygame.draw.rect(surface=surface, color="red", rect=self.rect)

    def __str__(self):
        return f"Player at [{self.x}, {self.y}]"


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.height = random.randint(MIN_ENEMY_HEIGHT, MAX_ENEMY_HEIGHT)
        self.width = ENEMY_RECT_AREA/self.height
        self.x = SC_WIDTH + random.randint(MIN_ENEMY_WIDTH, MAX_ENEMY_WIDTH)
        self.y = random.randint((SC_HEIGHT-self.height)//2+10, SC_HEIGHT//2)
        self.velx = ENEMY_VEL
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.passed = False


    def draw(self, surface):
        self.rect.center = self.x, self.y
        pygame.draw.rect(surface=surface, color="black", rect=self.rect)


    def move(self, dt):
        self.x += self.velx*dt
        if self.x <= -self.width*2:
            self.passed = True


    def __str__(self):
        return f"Enemy at [{self.x}, {self.y}]"


def main():
    global state, enem_list, score, dear_dino
    while state != EXIT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = EXIT
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    state = EXIT
                elif event.key == pygame.K_ESCAPE:
                    if state == RUNNING:
                        state = PAUSE
                    elif state == PAUSE:
                        state = RUNNING
                elif event.key == pygame.K_SPACE and state == STARTING:
                    reset_game()
                    pygame.time.set_timer(ENEMY_SPAWN_EVENT, SPAWN_INTERVAL)
                    reference_time = pygame.time.get_ticks()
                    state = RUNNING
                    dear_dino = Player()
                    dear_enemy = Enemy()
                    enem_list.append(dear_enemy)
            elif event.type == ENEMY_SPAWN_EVENT:
                dear_enemy = Enemy()
                enem_list.append(dear_enemy)

        if state == RUNNING:
            # fill the screen with white color to wipe away everything from last frame
            SCREEN.fill("white")

            # Drawing horizontal line just for fun
            pygame.draw.line(SCREEN, 'black', (0,SC_HEIGHT/2), (SC_WIDTH,SC_HEIGHT/2))

            # Drawing score on screen
            create_text(f"{score:04}", arial_b48, "black", position=(SC_WIDTH // 2, SC_HEIGHT // 8), screen_surface=SCREEN)

            create_text(f"HI {HIGH_SCORE:04}", monospace_24, "grey", (SC_WIDTH//4, SC_HEIGHT//8), SCREEN)

            # Drawing and Updating player
            dear_dino.draw(SCREEN)
            dear_dino.move(dt=dt)

            # Draw and update Enemy
            for dear_enemy in enem_list[:]:
                if dear_enemy:
                    if dear_enemy.passed:
                        enem_list.remove(dear_enemy)
                        dear_enemy = None
                    elif dear_dino.rect.colliderect(dear_enemy.rect):
                        create_text("Write your name in terminal to save the score", monospace_24, "grey", (SC_WIDTH//2, SC_HEIGHT*5//6), SCREEN)

                        name = take_name_input_in_game(SCREEN, monospace_24, 20)
                        if name:
                            write_score_to_file(SCORE_FILE_PATH, name, score)
                        reset_game()

                    else:
                        dear_enemy.draw(SCREEN)
                        dear_enemy.move(dt)


            current_time = pygame.time.get_ticks()
            score = (current_time - reference_time) // 1000


        elif state == PAUSE:
            create_text("Paused", arial_b48, "grey", SC_CENTER, SCREEN)


        elif state == STARTING:
            create_text("Press SPACE to start the game", monospace_24, "grey", (SC_WIDTH//2, SC_HEIGHT*3//4), SCREEN)
            create_text("Press X to exit", monospace_24, "black", (SC_WIDTH//2, SC_HEIGHT*4//5), SCREEN)


        # flip() the display to put your work on screen
        pygame.display.flip()
        dt = clock.tick(60) / 1000


    pygame.quit()


def reset_game():
    global state, enem_list, score, dear_dino
    state = STARTING
    enem_list = []
    score = 0
    dear_dino = Player()
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, 0)
    get_highscore_from_file(SCORE_FILE_PATH)


def create_text(text:str, font, color, position:tuple, screen_surface):
    try:
        surf = font.render(text, True, color)
        rect = surf.get_rect()
        rect.center = position
        screen_surface.blit(surf,rect)
    except ValueError:
        raise ValueError("Invalid Input")
    except TypeError:
        raise TypeError("Invalid Input")


def write_score_to_file(filepath:str, name:str, score):
    if not score:
        raise TypeError("Score is None")
    with open(filepath, "a") as scorefile_csv:
        writer = csv.writer(scorefile_csv)
        writer.writerow([datetime.now(), name, score])


def take_name_input_in_game(screen, font, max_length=10):
    input_active = True
    name = ""
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < max_length:
                        name += event.unicode

        screen.fill("white")
        create_text(f"{score}", arial_36, "black", (SC_WIDTH//2, SC_HEIGHT/3), screen)
        create_text(f"Enter your name: {name}", font, "black", (SC_WIDTH // 2, SC_HEIGHT // 2), screen)
        pygame.display.flip()
    return name.strip().capitalize()


def get_highscore_from_file(filepath:str):
    global HIGH_SCORE
    try:
        with open(filepath) as scorefile_csv:
            reader = csv.reader(scorefile_csv)
            for row in reader:
                try:
                    HIGH_SCORE = max(HIGH_SCORE, int(row[2]))
                except (ValueError, IndexError):
                    continue
    except FileNotFoundError:
        HIGH_SCORE = 0


if __name__ == "__main__":
    main()
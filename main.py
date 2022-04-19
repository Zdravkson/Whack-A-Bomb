import pygame
import random
import time
import os

pygame.init()

#time

clock = pygame.time.Clock()
fps = 60

#screen setup

screen_width = 384
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Whack-A-Bomb")

#loading images

file_dir = os.path.dirname(__file__)
image_dir = file_dir + "/sprite_images/"
background_img = pygame.image.load(image_dir + "background.png")
ground_img = pygame.image.load(image_dir + "grass_ground.png")
restart_img = pygame.image.load(image_dir + "restart.png")

#game variables

score = 0
bomb_frequency = 1000 #miliseconds
last_bomb = pygame.time.get_ticks() - bomb_frequency
game_over = False

#text setup

font = pygame.font.SysFont('Bauhas 93', 45)
white = (255, 255, 255)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    bomb_group.empty()
    score = 0
    return score

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, bt):
        pygame.sprite.Sprite.__init__(self)
        self.bomb_type = bt
        # bomb_type = True is nuke type, bomb_type = False is normal type
        if self.bomb_type == False:
            img = pygame.image.load(image_dir + "bomb.png")
        if self.bomb_type == True:
            img = pygame.image.load(image_dir + "nuke.png")
        img = pygame.transform.scale(img, (64, 64))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
    
    def update(self):
        if self.bomb_type == True:
            self.velocity += 1.5
        if self.bomb_type == False:
            self.velocity += 1
        if self.velocity > 8 and self.bomb_type == False:
            self.velocity = 8
        if self.velocity > 10 and self.bomb_type == True:
            self.velocity = 10
        if self.rect.bottom <= 704:
            self.rect.y += int(self.velocity)
        if self.rect.bottom > 704:
            global game_over
            game_over = True
            self.kill()
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0] == 1:
                global score
                score += 1
                self.kill()

class Button():
    def __init__(self, x, y, image):
        img = pygame.transform.scale(image, (93, 27))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

bomb_group = pygame.sprite.Group()

restart_button = Button(int(screen_width / 2), int(screen_height / 2), restart_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(background_img, (0, 0))
    screen.blit(ground_img, (0, 704))

    bomb_group.draw(screen)
    bomb_group.update()

    print(game_over)

    if game_over == False:
        time_now = pygame.time.get_ticks()
        if time_now - last_bomb > bomb_frequency:
            bomb_position = random.randint(32, screen_width - 32)
            bomb_type_num = random.randint(1, 9)
            if bomb_type_num == 9:
                generated_bomb = Bomb(bomb_position, -100, True)
                bomb_group.add(generated_bomb)
            else:
                generated_bomb = Bomb(bomb_position, -100, False)
                bomb_group.add(generated_bomb)
            last_bomb = time_now

    draw_text(str(score), font, white, int(screen_width * 0.9), int(screen_height * 0.95))

    if game_over == True:
        if restart_button.draw() == True:
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
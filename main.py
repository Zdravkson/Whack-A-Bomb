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
radar_img1 = pygame.image.load(image_dir + "radar_on.png")
radar_img2 = pygame.image.load(image_dir + "radar_off.png")

#game variables

score = 0
bomb_frequency = 500 #miliseconds
last_bomb = pygame.time.get_ticks() - bomb_frequency
game_over = True
clicked = False
radar = False

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
        self.death_images = []
        self.death_images.append(pygame.image.load(image_dir + "explosion_1.png"))
        self.death_images.append(pygame.image.load(image_dir + "explosion_2.png"))
        self.death_images.append(pygame.image.load(image_dir + "explosion_3.png"))
        self.death_images[0] = pygame.transform.scale(self.death_images[0], (64, 64))
        self.death_images[1] = pygame.transform.scale(self.death_images[1], (64, 64))
        self.death_images[2] = pygame.transform.scale(self.death_images[2], (64, 64))
        self.current_image = 0
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.is_dead = False

    def update(self):
        if self.is_dead == True:
            self.current_image += 0.3
            if self.current_image >= len(self.death_images):
                self.current_image = len(self.death_images) - 1
                self.kill()
            self.image = self.death_images[int(self.current_image)]
        if self.bomb_type == True:
            self.velocity += 1.5
        if self.bomb_type == False:
            self.velocity += 1
        if self.velocity > 5 and self.bomb_type == False:
            self.velocity = 5
        if self.velocity > 8 and self.bomb_type == True:
            self.velocity = 8
        if self.rect.bottom <= 704:
            self.rect.y += int(self.velocity)
        if self.rect.bottom > 704:
            global game_over
            game_over = True
            self.is_dead = True
        mousepos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousepos):
            if pygame.mouse.get_pressed()[0] == 1 and clicked == False:
                global score
                score += 1
                self.is_dead = True

class Button():
    def __init__(self, x, y, image):
        img = pygame.transform.scale(image, (92, 36))
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

class Radar():
    def __init__(self, x, y):
        img = pygame.transform.scale(radar_img1, (64, 64))
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if radar == True:
            img = pygame.transform.scale(radar_img1, (48, 48))
            self.image = img
        else:
            img = pygame.transform.scale(radar_img2, (48, 48))
            self.image = img
        screen.blit(self.image, (self.rect.x, self.rect.y)) 

bomb_group = pygame.sprite.Group()

restart_button = Button(int(screen_width / 2), int(screen_height / 2), restart_img)
radar_object = Radar(50, int(screen_height * 0.97))

run = True
while run:

    clock.tick(fps)

    screen.blit(background_img, (0, 0))
    screen.blit(ground_img, (0, 704))

    bomb_group.draw(screen)
    bomb_group.update()

    temp = False
    for b in bomb_group:
        if b.bomb_type == True:
            temp = True

    radar = temp

    radar_object.update()

    if pygame.mouse.get_pressed()[0] == 1:
        clicked = True
    if pygame.mouse.get_pressed()[0] == 0:
        clicked = False

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

    draw_text(str(score), font, white, int(screen_width * 0.8), int(screen_height * 0.95))

    if game_over == True:
        if restart_button.draw() == True:
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
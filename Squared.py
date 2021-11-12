import pygame
import pygame.locals
from pygame.locals import *
import math
import random

#screen setup
background_color = (255, 255, 255)
(width, height) = (1500, 900)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Squared by Herb')
pygame.init()
screen.fill(background_color)
game_scores = [0, 0, 0]
game_state = 0

#block class
class Block:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.vel = 5
        self.x_count = 0
        self.y_count = 0
    
    def draw(self):
        pygame.draw.rect(screen, self.sprite, (self.x - 25, self.y - 25, 50, 50))


#defining blocks
player = Block(750, 450, (0, 0, 255))

enemies = []

Level = [[False for x in range(30)] for y in range(18)] 
for i in range(30):
    Level[0][i] = True
    Level[17][i] = True
for i in range(18):
    Level[i][0] = True
    Level[i][29] = True

border_blocks = []
for i in range(30):
    for j in range(18):
        if Level[j][i]:
            border_blocks.append(Block(i * 50 + 25, j * 50 + 25, (0, 0, 0)))

#collision checking
def collide(x, y, block_array):
    r_val = False
    for i in block_array:
        if ((x + 24 > i.x - 25) & (x - 25 < i.x + 25) & (y + 24 > i.y - 25) & (y - 25 < i.y + 25)):
            r_val = True
    return r_val


def check_collision(x, y, block_array):
    if collide(x, y, block_array) or collide(x, y, border_blocks):
        return True
    else:
        return False
    

#moves enemies
def move_enemies():
    count = 0
    for i in enemies:
        en = []
        for h in enemies:
            en.append(h)

        del en[count]
        i.vel = 3
        x_c = i.x_count
        y_c = i.y_count
        r_1 = random.random()
        r_2 = random.random()
        loop_count = True
        while loop_count:
            if (i.y_count == 0) or (i.x_count == 0):
                if not(check_collision(i.x + (i.x_count * i.vel), i.y, en)) and i.x_count != 0:
                    i.x += i.x_count * i.vel
                    loop_count = False
                if not(check_collision(i.x, i.y + (i.y_count * i.vel), en)) and i.y_count != 0:
                    i.y += i.y_count * i.vel
                    loop_count = False
            else:
                if not(check_collision(i.x + int(i.x_count * i.vel * math.sqrt(2) / 2), i.y, en)):
                    i.x += int(i.x_count * i.vel * math.sqrt(2) / 2)
                    i.x_count = 0
                if not(check_collision(i.x, i.y + int(i.y_count * i.vel * math.sqrt(2) / 2), en)):
                    i.y += int(i.y_count * i.vel * math.sqrt(2) / 2)
                    i.y_count = 0
            if(i.vel > 0 and loop_count):
                i.vel -= 1
            else:
                loop_count = False
        if r_1 > .98 and x_c < 1:
            x_c += 1
        elif r_1 < .02 and x_c > -1:
            x_c -= 1
        if r_2 > .98 and y_c < 1:
            y_c += 1
        elif r_2 < .02 and y_c > -1:
            y_c -= 1
        if random.random() < .03:
            if i.x > player.x:
                x_c = -1
            else:
                x_c = 1
        if random.random() < .03:
            if i.y > player.y:
                y_c = -1
            else:
                y_c = 1

        i.x_count = x_c
        i.y_count = y_c
        count += 1 



#moves player with arrow keys
def move_player():
    x_count = 0
    y_count = 0
    loop_count = False
    if keys[pygame.K_LEFT]:
        x_count -= 1
        loop_count = True
    if keys[pygame.K_RIGHT]:
        x_count += 1
        loop_count = True
    if keys[pygame.K_UP]:
        y_count -= 1
        loop_count = True
    if keys[pygame.K_DOWN]:
        y_count += 1
        loop_count = True
    while loop_count:
        if (y_count == 0) or (x_count == 0):
            if not(check_collision(player.x + (x_count * player.vel), player.y, enemies)) and x_count != 0:
                player.x += x_count * player.vel
                loop_count = False
            if not(check_collision(player.x, player.y + (y_count * player.vel), enemies)) and y_count != 0:
                player.y += y_count * player.vel
                loop_count = False
        else:
            if not(check_collision(player.x + int(x_count * player.vel * math.sqrt(2) / 2), player.y, enemies)):
                player.x += int(x_count * player.vel * math.sqrt(2) / 2)
                x_count = 0
            if not(check_collision(player.x, player.y + int(y_count * player.vel * math.sqrt(2) / 2), enemies)):
                player.y += int(y_count * player.vel * math.sqrt(2) / 2)
                y_count = 0
        if(player.vel > 0 and loop_count):
            player.vel -= 1
        else:
            loop_count = False
    player.vel = 5

#checks to see death
def check_death():
    r_val = False
    if collide(player.x + 1, player.y + 1, enemies):
        r_val = True
    if collide(player.x - 1, player.y + 1, enemies):
        r_val = True
    if collide(player.x + 1, player.y - 1, enemies):
        r_val = True
    if collide(player.x - 1, player.y - 1, enemies):
        r_val = True
    return r_val

#sorts game scores
def top_three(numbers):
    r_array = []
    o_array = numbers
    for g in range(3):
        for i in o_array:
            isHighest = True
            for j in o_array:
                if j > i:
                    isHighest = False
            if isHighest:
                r_array.append(i)
                o_array.remove(i)
                break
    return r_array
            

    
font_1 = pygame.font.SysFont(None, 100)
img = font_1.render('GAME OVER', True, (255, 55, 55))
squared_img= font_1.render('SQUARED', True, (55, 55, 255))
font_2 = pygame.font.SysFont(None, 50)
press_space_img = font_2.render('PRESS SPACE TO PLAY', True, (255, 255, 255))

#updates screen 
def update_game_screen():
    screen.fill(background_color)
    for h in border_blocks:
        h.draw()
    for h in enemies:
        h.draw()
    player.draw()
    show_score = font_2.render(str(loop_count), True, (0, 255, 0))
    screen.blit(show_score, (20, 20))
    pygame.display.update()



#main loop
running = True
loop_count = 0

while(running):
    pygame.time.delay(5)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            running = True
        if event.type == pygame.QUIT:
            running = False 

    keys = pygame.key.get_pressed()

    if game_state == 0:
        screen.fill((0, 0, 0))
        screen.blit(squared_img, (570, 400))
        screen.blit(press_space_img, (535, 525))

        pygame.display.update()
        if keys[pygame.K_SPACE]:
            enemies = []
            loop_count = 0
            game_state = 1
    
    if game_state == 1:
        move_player()
        
        move_enemies()

        update_game_screen()

        if loop_count % 200 == 0:
            while True:
                r_1 = 50 + int(random.random() * 1500)
                r_2 = 50 + int(random.random() * 800)
                if not(collide(r_1, r_2, enemies)) and not(check_collision(r_1, r_2, [player])):
                    enemies.append(Block(r_1, r_2, (255, 0, 0)))
                    break
        
        loop_count += 1

        if check_death():
            game_state = 2
            if loop_count > game_scores[2]:
                game_scores.append(loop_count)
                game_scores = top_three(game_scores)
    
    if game_state == 2:
        screen.fill((0, 0, 0))
        screen.blit(img, (540, 400))
        show_score = font_2.render(str(loop_count), True, (0, 255, 0))
        screen.blit(show_score, (20, 20))
        screen.blit(press_space_img, (550, 525))

        #displays top scores
        for u in range(3):
            try:
                if game_scores[u] == loop_count and game_scores[u + 1] < loop_count:
                    top_score = font_2.render(str(u + 1) + ": " + str(game_scores[u]), True, (55, 255, 255))
                    screen.blit(top_score, (700, 600 + (50 * u)))
                else:
                    top_score = font_2.render(str(u + 1) + ": " + str(game_scores[u]), True, (55, 255, 55))
                    screen.blit(top_score, (700, 600 + (50 * u)))
            except IndexError:
                if game_scores[u] == loop_count:
                    top_score = font_2.render(str(u + 1) + ": " + str(game_scores[u]), True, (55, 255, 255))
                    screen.blit(top_score, (700, 600 + (50 * u)))
                else:
                    top_score = font_2.render(str(i + 1) + ": " + str(game_scores[i]), True, (55, 255, 55))
                    screen.blit(top_score, (700, 600 + (50 * u)))
        pygame.display.update()
        
        if keys[pygame.K_SPACE]:
            enemies = []
            loop_count = 0
            game_state = 1

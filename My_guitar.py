# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 18:03:04 2020

@author: jbris
"""

import random
import pygame

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
swid = 800 # Screen width
sheight = 600 # Screen height
screen = pygame.display.set_mode((swid,sheight)) # set window size (wid, height)
black=(0,0,0)
blue = (0,0,255) # colours are RGB
red = (155,0,0)
white = (255,255,255)
grey = (100,100,100)
guit = pygame.image.load('newguit.png')
pygame.display.set_caption('Richards FOF') # set caption of game
font = pygame.font.SysFont(None, 72) # Set font settings
font2 = pygame.font.SysFont(None, 52)
FR = 60 # Frame rate
# oof = pygame.mixer.music.load("sound.wav") add sound to folder with name blank.wav for sound effects
# pygame.mixer.music.set_volume(0.7)

def play():
    pygame.mixer.music.play()

class tile:
    def __init__(self, x, y, d, colour=red,pressed = False):
        self.x = x
        self.y = y
        self.d = d
        self.colour = colour
        self.pressed = pressed
        self.img = font.render(d,True,white)

def findx(d):
    if d == 'Q':
        return 333 - font.render(d,True,white).get_width()/2    
    if d == 'W':
        return 368 - font.render(d,True,white).get_width()/2
    if d == 'E':
        return 404 - font.render(d,True,white).get_width()/2
    if d == 'R':
        return 437 - font.render(d,True,white).get_width()/2
    if d == 'T':
        return 472 - font.render(d,True,white).get_width()/2
    if d == 'Y':
        return 505 - font.render(d,True,white).get_width()/2
    else:
        print('something went wrong with placing the tile')

running = False
start_screen = True
while start_screen: # Load start screen
    clock.tick(FR)
    screen.fill((155,0,0))
    intro = font.render('Press any button to start!',True,white) 
    instrmsg = "Press the correct QWERTY key"
    instrmsg2 = "when it reaches the white line"
    instr = font.render(instrmsg,True,white)
    instr2 = font.render(instrmsg2,True,white)
    screen.blit(instr, instr.get_rect(centerx=400,y=sheight/2-150))
    screen.blit(instr2, instr2.get_rect(centerx=400,y=sheight/2-75))
    screen.blit(intro, intro.get_rect(centerx=400,y=sheight/2+50))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_screen = False
            running = True
        if event.type == pygame.KEYDOWN:
            running = True
            start_screen = False
    
sweet = font.render('Sweet!',True,white) # streak msg

# Initial Settings
score = 0
streak = 0
tiles = []
directions = ['Q','W','E','R','T','Y']
cooldown = 0
length = 60 # Game length in seconds
game_length = round(length*FR) 
multi = 1
tile_speed = set_speed = 4
streakmax = 0
total_tiles = 0
correct = 0
lmargin = 150
while running:
    clock.tick(FR)
    screen.blit(guit, (0,0))
    if streak == 0:
        tile_speed = set_speed
        msgcount = 0
    if streak == 10 and tile_speed == set_speed:
        strkmsg = 'Good!'
        tile_speed += 1
        msgcount = 100
    if streak == 20 and tile_speed == set_speed + 1:
        msgcount = 100
        strkmsg = 'Sweet!'
    if streak == 50 and tile_speed == set_speed + 1:
        tile_speed += 1
        msgcount = 100
        strkmsg = 'WOW!'
    if msgcount>0:
        msgcount -= 1
        screen.blit(font.render(strkmsg,True,red), (lmargin-font.render(strkmsg,True,white).get_width()/2,30))    
    if game_length > 0:
        game_length -= 1
    if cooldown > 0:
        cooldown -= 1
    if game_length != 0:
        if cooldown == 0:
            di = random.choice(directions)
            tiles.append(tile(findx(di),-50,di))
            total_tiles += 1
            cooldown = 50
            if streak >= 20:
                cooldown = 30
    
    for letter in tiles:
        letter.y += tile_speed
        pygame.draw.rect(screen, letter.colour,(letter.x-5,letter.y-8,font.render(letter.d,True,white).get_width()+10,60))
        screen.blit(letter.img, (letter.x, letter.y))
        if letter.y > sheight:
            tiles.remove(letter)
    
    scoreimg = font.render(str(score), True, white)
    if score<10:
        screen.blit(scoreimg, (lmargin-scoreimg.get_width()/2,525))
    else:
        screen.blit(scoreimg, (lmargin-scoreimg.get_width()/2,525))
    scoretxt = font2.render('SCORE', True, white)
    screen.blit(scoretxt, (lmargin-scoretxt.get_width()/2,485))
    streaktxt = font2.render('STREAK', True, white)
    streakimg = font.render(str(streak), True, white)
    multitxt = font.render('MULTI', True, white)
    screen.blit(multitxt, (lmargin-multitxt.get_width()/2,180))
    xm = font.render('X'+str(multi),True,white)
    screen.blit(xm,(lmargin-xm.get_width()/2,235))
    if streak<10:
        screen.blit(streakimg, (lmargin-streakimg.get_width()/2,370))
    else:
        screen.blit(streakimg, (lmargin-streakimg.get_width()/2,370))
    screen.blit(streaktxt, (lmargin-streaktxt.get_width()/2,325))
    pygame.draw.rect(screen, (red),(lmargin-50,425,100,10))
    if streak < 100:
        pygame.draw.rect(screen, (0,255,0), (lmargin-50,425,2*streak,10))
    else:
        pygame.draw.rect(screen, (0,255,0), (lmargin-50,425,100,10))
    if 9<streak<20:
        multi = 2
    if 20<=streak<50:
        multi = 3
    if streak >= 50:
        multi = 4
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            end_screen = True
        pressed = ''
        should_press = []
        for letter in tiles:
            if (340<letter.y<400) and not letter.pressed:
                should_press.append(letter.d)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pressed = 'Q' 
            if event.key == pygame.K_r:
                pressed = 'R'
            if event.key == pygame.K_w:
                pressed = 'W'
            if event.key == pygame.K_e:
                pressed = 'E'
            if event.key == pygame.K_t:
                pressed = 'T'
            if event.key == pygame.K_y:
                pressed = 'Y'
            if pressed not in should_press: # if pressed before tile reached line
                pressnext = []
                for letter in tiles:
                    if letter.y<340 and not letter.pressed:
                        pressnext.append(letter)
                if pressnext and not should_press:
                    pressnext[0].colour = grey
                    pressnext[0].pressed = True
                    streak = 0
                    multi = 1
        
        for letter in tiles:
            if (340<letter.y<400) and letter.d == pressed:
                if not letter.pressed:
                    score += 1*multi
                    correct += 1
                    streak += 1
                    letter.pressed = True
                    letter.colour = (0,255,0)
                    #play() plays loaded sound on pressing note
    for letter in tiles:
        if letter.y > 410 and not letter.pressed:
                letter.colour = grey
                streak = 0
                multi = 1
                letter.pressed = True
    if streakmax < streak:
        streakmax = streak
    streakmax_img = font.render('MAX STREAK: '+str(streakmax), True, white)
    
    # Layout
    pygame.draw.rect(screen, (255,255,255),(293,400,472-333+120,10))
    pygame.display.update()
    
    if not tiles:
        running = False
        end_screen = True

while end_screen:
    clock.tick(FR)
    screen.fill(grey)
    p_correct = round(100*correct/total_tiles)
    p_msg = font.render('Percentage Score: '+str(p_correct)+'%',True, white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_screen = False
    scorerect = scoreimg.get_rect(centerx=400,y=sheight/2-150)
    scoretxt = font.render('Score', True, white)
    screen.blit(scoretxt, scoretxt.get_rect(centerx=400,y=sheight/2-200))
    screen.blit(scoreimg, scorerect)
    screen.blit(streakmax_img, streakmax_img.get_rect(centerx = 400, y=sheight/2+100))
    screen.blit(p_msg, p_msg.get_rect(centerx=400, y=sheight/2 - 50))
    pygame.display.update()
pygame.quit()
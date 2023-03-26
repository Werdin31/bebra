from pygame import *
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from map import make_map
from time import time as timer
init()

mixer.init()
window = display.set_mode((700, 500))
display.set_caption("Лабіринт")
background = transform.scale(image.load("PYGAME/labirint/fonchik.jpg"), (700, 500))
window.blit(background, (0, 0))
musik = mixer.music.load("PYGAME/labirint/jungles.ogg")
kick = mixer.Sound("PYGAME/labirint/kick.ogg")
money = mixer.Sound("PYGAME/labirint/money.ogg")
clock = time.Clock()
game = True


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player (GameSprite):
    def update(self):
        pressed_keys = key.get_pressed()
        if pressed_keys [K_w] and self.rect.y >= 0: 
            self.rect.y -= self.speed
        if pressed_keys [K_s] and self.rect.y +self.rect.height<=500:
            self.rect.y += self.speed
        if pressed_keys[K_a] and self.rect.x >= 0: 
            self.rect.x-= self.speed 
        if pressed_keys [K_d] and self.rect.x +self.rect.height<=700:
            self.rect.x += self.speed
    def touch(self, sprite):
        return self.rect.colliderect(sprite.rect)
        
class Enemy (GameSprite):
    def update(self,x1, x2):
        self.rect.x += self.speed
        if self.rect.x <= x1 or self.rect.x + self.rect.width >= x2:
            self.speed*= -1

hero = Player('PYGAME/labirint/hero.png', 0, 0, 5)
hero.draw_sprite()
cyborg = Enemy('PYGAME/labirint/cyborg.png', 470, 300, 2)
cyborg.draw_sprite()
treasure = GameSprite('PYGAME/labirint/treasure.png', 550, 400)
treasure.draw_sprite()

game_map = make_map()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    hero.update()
    cyborg.update(425, 650)
    if hero.touch(cyborg):                                  
        hero.rect.x = 0
        hero.rect.y = 0
        kick.play()
    if hero.touch(treasure):
        money.play()
        text = font.SysFont('Algerian', 50).render('You won!!!', True, (0,0,0))
        game = False        
    window.blit(background, (0, 0))
    for block in game_map:
        if hero.rect.colliderect(block):                    
            hero.rect.x = 0
            hero.rect.y = 0
            kick.play()
        draw.rect(window, (0, 187, 252), block)
    hero.draw_sprite()
    cyborg.draw_sprite()
    treasure.draw_sprite()
    display.update()
    clock.tick(60)

window.blit(text, (200, 200))
display.update()
game = True
start_timer = timer()
while game and timer() - start_timer < 5:
    for e in event.get():
        if e.type == QUIT:
            game = False
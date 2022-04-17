from pygame import *
from random import randint

w = 700
h = 500
window = display.set_mode((w, h))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

lost = 0
score = 0
max_lost = 3
goal = 10
class GameSprite(sprite.Sprite):
   #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       #every sprite must have the rect property – the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Player(GameSprite):
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < w - 80:
           self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx-8,self.rect.top,15,20,-15)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > h:
            self.rect.x = randint(80, w - 80)
            self.rect.y = 0
            lost += 1


font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',80)

win = font2.render("You Win!",1,(255,255,255))
lose = font2.render("You lose!",1,(255,255,255))

ship = Player("rocket.png",5,400,80,100,10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png",randint(80,h-80),-40,80,50,randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

game = True
while game:
    window.blit(background,(0, 0))

    ship.update()
    ship.reset()
    monsters.update()
    monsters.draw(window)
    bullets.draw(window)
    bullets.update()

    text_score = font1.render("Score: " + str(score),1,(255,255,255))
    window.blit(text_score,(10,10))
    text_lose = font1.render("Missed: " + str(lost),1,(255,255,255))
    window.blit(text_lose,(10,40))

    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            game = False
        if keys[K_SPACE]:
            ship.fire()
            #fire_sound.play()
    
    group_colide = sprite.groupcollide(monsters, bullets, True, True)
    for c in group_colide:
        score += 1
        monster = Enemy("ufo.png",randint(80,h-80),-40,80,50,randint(1,5))
        monsters.add(monster)
    if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
        game = False
        window.blit(lose,(200,200))
    if score >= goal:
        game = False
        window.blit(win,(200,200))
    
    display.update()
    time.delay(50)
time.delay(3000)
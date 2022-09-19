from pygame import *
from random import randint

w = 700
h = 500
window = display.set_mode((w, h)) #กำหนด ความกว้างและสูงของ window
display.set_caption("Shooter") #กำหนด  ชื่อ หน้าต่าง ชื่อ Shooter
background = transform.scale(image.load("galaxy.jpg"), (700, 500)) #เปลี่ยนรูปภาพให้เป็นพื้นหลัง

class GameSprite(sprite.Sprite):# สร้างคลาสพื้นฐานสำหรับspriteในเกม
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       super().__init__()
       #ต้องกำหนดค่าต่างๆของspriteในเกม
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y)) #แสดงรูปภาพในตำแหน่ง x y นั้นๆ

class Bullet(GameSprite): #สร้างคลาส bullet ซึ่งทำต่อเนื่องจาก class GameSprite
    def update(self):
        self.rect.y += self.speed #ให้ตำแหน่งเพิ่มขึ้น1ครั้งเท่ากับค่าspeed
        if self.rect.y < 0:
            self.kill() #ถ้าค่าyน้อยกว่า 0 สั่งให้ตัวself(bullet)หายไป

class Player(GameSprite):  #สร้างคลาส player ซึ่งทำต่อเนื่องจาก class GameSprite
    def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed #ถ้ากดปุ่ม ซ้าย ให้เคลื่อนไปทางซ้าย 1 ครั้ง เท่ากับ ค่า speed ของ self
       if keys[K_RIGHT] and self.rect.x < w - 80:
           self.rect.x += self.speed #ถ้ากดปุ่ม ขวา ให้เคลื่อนไปทางขวา 1 ครั้ง เท่ากับ ค่า speed ของ self
    def fire(self): #สร้างคลาส fire ซึ่งทำต่อเนื่องจาก class player
        bullet = Bullet("bullet.png",self.rect.centerx-8,self.rect.top,15,20,-15) #ใส่parameter เพื่อป้อนข้อมูลตามที่class bullet ต้องการ
        bullets.add(bullet)# add bullet to bullets


class Enemy(GameSprite): #สร้างคลาส Enemy ซึ่งทำต่อเนื่องจาก class GameSprite
    def update(self):
        self.rect.y += self.speed
        global lost #นำเข้าตัวแปร lost
        if self.rect.y > h:
            self.rect.x = randint(80, w - 80)# แรนด้อมค่าแกนxของ enemy
            self.rect.y = 0 #ถ้าspriteในclass enemy มีค่าy = 0
            lost += 1 # lost เพิ่ม1

class Block(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > w:
            self.rect.x -= w
        if self.rect.x < 0:
            self.rect.x += self.speed
        self.rect.y = randint(100,200)
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

class Block2(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x > w:
            self.rect.x -= 1
        if self.rect.x <= 0:
            self.rect.x = w
        self.rect.y = randint(100,200)
    def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))

font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',80)

win = font2.render("You Win!",1,(255,255,255))#สร้างtext ลงในwindow
lose = font2.render("You lose!",1,(255,255,255))

ship = Player("rocket.png",5,400,80,100,10) #ใส่parameter เพื่อป้อนข้อมูลตามที่class Player ต้องการ
wallx = 100
wally = 80
block = Block("alien.png.png",0,200,128,128,10)
block2 = Block2("alien.png.png",w,200,128,128,10)
while True:
    monsters = sprite.Group()#สร้าง ตัวแปร monsters ให้อยู่ใน sprite group
    for i in range(3):
        monster = Enemy("ufo.png",randint(80,h-80),-40,80,50,randint(10,13)) #ใส่parameter เพื่อป้อนข้อมูลตามที่class Enemy ต้องการ
        monsters.add(monster)

    bullets = sprite.Group()
    #กำหนดตัวค่าเริ่มของเกม
    game = True
    lost = 0
    score = 0
    max_lost = 3
    goal = 51
    while game: #ในขณะที่เกมดำเนืน
        window.blit(background,(0, 0))

        ship.update() #ใช้function updae และ reset สำหรับ sprite ทุกตัว
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        block.update()
        block.reset()
        block2.update()
        block2.reset()


        text_score = font1.render("Score: " + str(score),1,(255,255,255)) #แสดงข้อความคะแนนเพิ่มจำนวนตาม variable score
        window.blit(text_score,(10,10))
        text_lose = font1.render("Missed: " + str(lost),1,(255,255,255))#แสดงข้อความMissedพิ่มจำนวนตาม variable lost
        window.blit(text_lose,(10,40))


        for e in event.get():# main loop
            keys = key.get_pressed()
            if e.type == QUIT:
                quit()
            if keys[K_SPACE]:#เมื่อกดspace bar ใช้method fire-
                ship.fire()


        group_colide = sprite.groupcollide(monsters, bullets, True, True)
        for c in group_colide: #ถ้า sprite ชนกันตามfunction collide
            score += 1
            monster = Enemy("ufo.png",randint(80,h-80),-40,80,50,randint(10,13))
            monsters.add(monster)#add monster เพิ่มให้ครบ5
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            game = False
        if sprite.spritecollideany(block, bullets):
            bullets.remove(bullets)

        if score >= goal:
            game = False # ออกเกม
            window.blit(win,(200,200))#แสดงผล

        display.update()
        time.delay(50)
    time.delay(1000)

#Создай собственный Шутер!

from pygame import *
from random import randint

font.init()
font1 = font.SysFont('Arial', 40)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))

font2 = font.SysFont('Arial', 36)

score = 0
lost = 0
max_lost = 3
goal = 10

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, hp = 0):
        super().__init__()
        self.hp = hp
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
                self.kill()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Maze')
background = transform.scale(image.load('fon.jpg'), (win_width, win_height))

player = Player('Rocke.png', 5, win_height - 100, 80, 100, 10, 3)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid('asteroid.jpg', randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)


bullets = sprite.Group()
health = GameSprite('hp.png', randint(80, win_width - 80), randint(80, win_height - 80), 30, 30, 50)

game = True
clock = time.Clock()
FPS = 60

finish = False
run = True

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if not finish:  
        window.blit(background,(0, 0))

        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 255))
        window.blit(text,(10, 20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(10, 50))

        text_hp = font2.render('Осталось жизней:' + str(player.hp), 1, (255, 255, 255))
        window.blit(text_hp,(10, 80))

        player.reset()
        health.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        
        sprite.groupcollide(asteroids, bullets, False, True)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            mnoster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        if lost >= max_lost or sprite.spritecollide(player, asteroids, True):
            finish = True
            player.hp = 0
            window.blit(lose, (200, 200))

        if sprite.spritecollide(player, monsters, True):
            if player.hp > 0:
                player.hp -= 1
                mnoster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
                monsters.add(monster)
            else:
                finish = True  
                window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))        


        display.update()
    clock.tick(FPS)
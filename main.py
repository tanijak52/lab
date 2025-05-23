from pygame import *


win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpg"), (win_width, win_height))

game = True
finish = False
clock = time.Clock()
FPS = 60


mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x =  player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        self.reset()
class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.direction == "right":
            self.rect.x += self.speed
        if self.rect.x <= 470:
            self.direction = "left"
        if self.direction == "left":
             self.rect.x -= self.speed
    
   
player = GameSprite("hero.png", 100, 100, 5)
enemy = GameSprite("cyborg.png", 300, 100, 2)
money = GameSprite("treasure.png", 500, 100, 0)




while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
            
    window.blit(background, (0, 0))
    clock.tick(FPS)
    player.reset()
    enemy.reset()
    money.reset()

    display.update()
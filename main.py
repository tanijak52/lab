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
show_money = False
collected_coins = 0 


mixer.init()
mixer.music.load("jungles.ogg")
mixer.music.play()
money_sound = mixer.Sound("money.ogg")
kick_sound = mixer.Sound("kick.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
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
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = "left"

    def update(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x <= 470:
                self.direction = "right"
        else:
            self.rect.x += self.speed
            if self.rect.x >= 620:
                self.direction = "left"

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y, color):
        super().__init__()
        self.image = Surface((20, 400))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Coin(GameSprite):
    def __init__(self, coin_image, coin_x, coin_y):
        super().__init__(coin_image, coin_x, coin_y, 0)
        self.collected = False
    def collect(self):
        self.collected = True
    def draw(self):
        if not self.collected:
            window.blit(self.image, (self.rect.x, self.rect.y))

player = Player("hero.png", 75, 0, 5)
enemy = Enemy("cyborg.png", 600, 300, 2)
money = GameSprite("treasure.png", 550, 400, 0)

coins = [Coin("coin.png", 80, 150, ),Coin("coin.png", 180, 270),Coin("coin.png", 280, 30),Coin("coin.png", 380, 340), Coin("coin.png", 550, 150)]

total_coins = len(coins)

wall1 = Wall(50, 70, (0, 255, 247))
wall2 = Wall(150, 0, (0, 255, 247))
wall3 = Wall(250, 70, (0, 255, 247))
wall4 = Wall(350, 0, (0, 255, 247))
wall5 = Wall(450, 70, (0, 255, 247))
walls = [wall1, wall2, wall3, wall4, wall5]


font.init()
font_big = font.Font(None, 70)
win_text = font_big.render("YOU WIN", True, (0, 255, 0))
lose_text = font_big.render("YOU LOSE", True, (255, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))

        for wall in walls:
            wall.draw_wall()
        for coin in coins:
            coin.draw()

        player.update()
        enemy.update()
        enemy.reset()

        
        for coin in coins:
            if not coin.collected and sprite.collide_rect(player, coin):
                coin.collect()
                collected_coins += 1
                money_sound.play()

        
        if collected_coins == total_coins:
            show_money = True

        if show_money:
            money.reset()

        
        if show_money and sprite.collide_rect(player, money):
            finish = True
            window.blit(win_text, (200, 200))
            money_sound.play()

        
        if sprite.collide_rect(player, enemy):
            finish = True
            window.blit(lose_text, (200, 200))
            kick_sound.play()

       
        for wall in walls:
            if sprite.collide_rect(player, wall):
                finish = True
                window.blit(lose_text, (200, 200))
                kick_sound.play()
                break
    else:
        window.blit(background, (0, 0))
        for wall in walls:
            wall.draw_wall()
        player.reset()
        enemy.reset()
        if show_money:
            money.reset()
        if show_money and sprite.collide_rect(player, money):
            window.blit(win_text, (200, 200))
        else:
            window.blit(lose_text, (200, 200))

    display.update()
    clock.tick(FPS)

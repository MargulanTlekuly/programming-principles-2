import random
import pygame

pygame.init()

WIDTH, HEIGHT = 400, 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
LOSS_SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

SCORE = 0
LIFE = 3

clock = pygame.time.Clock()

background = pygame.image.load('AnimatedStreet.png')

score_font = pygame.font.SysFont("Verdana", 30)
life_font = pygame.font.SysFont("Verdana", 30)

background_sound = pygame.mixer.Sound("background.wav")
crush_sound = pygame.mixer.Sound("crash.wav")

background_y = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(6, 8)
        self.image = pygame.image.load('Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(self.rect.width, WIDTH - self.rect.width),
            0,
        )

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y > HEIGHT:
            self.rect.center = (
                random.randint(self.rect.width, WIDTH - self.rect.width),
                0,
            )

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 7
        self.image = pygame.image.load('Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.rect.height // 2 - 20)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and self.rect.x - self.speed >= 0:
            self.rect.move_ip(-self.speed, 0)
        elif pressed[pygame.K_RIGHT] and self.rect.x + self.speed + self.rect.width <= WIDTH:
            self.rect.move_ip(self.speed, 0)

coins = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = random.randint(5, 8)
        self.random_number = random.randint(0, 6)
        if self.random_number in [0, 1, 2]:
            self.image = pygame.image.load("Coin.png")
        else:
            self.image = pygame.image.load("cent.png")
        self.resized_image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.resized_image.get_rect()
        if WIDTH - self.rect.width > self.rect.width:
            x = random.randint(self.rect.width, WIDTH - self.rect.width)
        else:
            x = random.randint(WIDTH - self.rect.width, self.rect.width)
        self.rect.center = (x, 0)

    def draw(self, surface):
        surface.blit(self.resized_image, self.rect)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y > HEIGHT:
            global LIFE
            LIFE -= 1
            self.rect.center = (
                random.randint(self.rect.width, WIDTH - self.rect.width),
                0,
            )

    def collide(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill() 
            return True

        return False

    def is_mega_coin(self):
        return self.random_number in [0, 1, 2]

def main():
    global background_y
    global coins
    global SCORE
    global LIFE

    running = True

    player = Player()
    enemy = Enemy()
    coin = Coin()

    enemies = pygame.sprite.Group()
    enemies.add(enemy)

    coins.add(coin)

    background_sound.play(-1)

    while running:
        SCREEN.fill(WHITE)

        background_rect = background.get_rect()
        SCREEN.blit(background, (0, background_y))
        SCREEN.blit(background, (0, background_y - background_rect.height))
        background_y += 4  
        if background_y > background_rect.height:
            background_y = 0

        score = score_font.render(f"Your score: {SCORE}", True, BLACK)
        SCREEN.blit(score, (5, 0))
        life = life_font.render(f"Your life: {LIFE}", True, BLACK)
        SCREEN.blit(life, (5, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or LIFE == 0:
                running = False

        player.update()
        enemy.update()

        for coin in coins:
            if coin.collide(player):
                coins.remove(coin)
                SCORE += 1
                coins.add(Coin())
                if coin.is_mega_coin():
                    SCORE += 4

        if SCORE > 30:
            enemy.speed = random.randint(8, 11)

        if LIFE == 0:
            running = False

        for coin in coins:
            coin.draw(SCREEN)
            coin.update()

        player.draw(SCREEN)
        enemy.draw(SCREEN)

        if pygame.sprite.spritecollide(player, enemies, False):
            background_sound.stop()
            crush_sound.play()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()

        clock.tick(60)

main()
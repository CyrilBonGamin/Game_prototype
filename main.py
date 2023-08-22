import pygame  # загружаем библиотеку pygame
import random

pygame.init()  # инициализируем библиотеку pygame

FPS = 15  # переменная частоты смены кадров в секнду (frame per second)
fpsClock = pygame.time.Clock()  # метод клок
winWidth = 1080  # ширина окна
winHeight = 720  # высота окна
win = pygame.display.set_mode((winWidth, winHeight))  # создание окна размерами ширины и высоты окна
pygame.display.set_caption('Pixel World')  # название окна

death = False
exp = 0
e = 50
fill = 0
lvl = 1


class Tree:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # ширина и высота конкретного дерева
        self.width = 39
        self.height = 29

    def drawLeaf(self):
        win.blit(pygame.image.load('Tree/leaf.png'), (self.x - 15, self.y - 97))  # подгонка под текстуры

    def drawTrunk(self):
        win.blit(pygame.image.load('Tree/trunk.png'), (self.x, self.y))


class Hero:
    def __init__(self, x, y, width, height, speed, hp, strength):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp = hp
        self.strength = strength

        self.keys = []
        self.mkeys = []

        self.lastMove = "right"
        self.facing = 1

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.animCount = 0

        self.walkRight = [pygame.image.load('Hero/Walk_R/Step1.png'), pygame.image.load('Hero/Walk_R/Step2.png'),
                          pygame.image.load('Hero/Walk_R/Step3.png')]
        self.walkLeft = [pygame.image.load('Hero/Walk_L/Step1.png'), pygame.image.load('Hero/Walk_L/Step2.png'),
                         pygame.image.load('Hero/Walk_L/Step3.png')]
        self.walkUp = [pygame.image.load('Hero/Walk_Up/Step1.png'), pygame.image.load('Hero/Walk_Up/Step2.png'),
                       pygame.image.load('Hero/Walk_Up/Step3.png')]
        self.walkDown = [pygame.image.load('Hero/Walk_Down/Step1.png'), pygame.image.load('Hero/Walk_Down/Step2.png'),
                         pygame.image.load('Hero/Walk_Down/Step3.png')]
        self.playerStand = pygame.image.load('Hero/Walk_Down/Step2.png')

        self.animCountS = 0

        self.playerAttackR = [pygame.image.load('Hero/Attack_R/Sword1.png'),
                              pygame.image.load('Hero/Attack_R/Sword2.png'),
                              pygame.image.load('Hero/Attack_R/Sword3.png')]

        self.playerAttackL = [pygame.image.load('Hero/Attack_L/Sword1.png'),
                              pygame.image.load('Hero/Attack_L/Sword2.png'),
                              pygame.image.load('Hero/Attack_L/Sword3.png')]

    def moveHero(self, pos):
        (self.x, self.y) = pos
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_a] and self.keys[pygame.K_w] and self.y > 0 and self.x > 0:
            self.y -= self.speed // 3
            self.x -= self.speed // 3
            self.left = True
            self.right = False
            self.up = True
            self.down = False
            self.lastMove = "left"
        elif self.keys[pygame.K_a] and self.keys[
            pygame.K_s] and self.x > 0 and self.y < winHeight - 35 - self.height - 1:
            self.y += self.speed // 3
            self.x -= self.speed // 3
            self.left = True
            self.right = False
            self.up = False
            self.down = True
            self.lastMove = "left"
        elif self.keys[pygame.K_d] and self.keys[pygame.K_w] and self.y > 0 and self.x < winWidth - self.width:
            self.y -= self.speed // 3
            self.x += self.speed // 3
            self.left = False
            self.right = True
            self.up = True
            self.down = False
            self.lastMove = "right"
        elif self.keys[pygame.K_d] \
                and self.keys[
            pygame.K_s] and self.x < winWidth - self.width and self.y < winHeight - 35 - self.height - 1:
            self.y += self.speed // 3
            self.x += self.speed // 3
            self.left = False
            self.right = True
            self.up = False
            self.down = True
            self.lastMove = "right"
        if self.keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            self.left = True
            self.right = False
            self.up = False
            self.down = False
            self.lastMove = "left"
        elif self.keys[pygame.K_d] and self.x < winWidth - self.width:
            self.x += self.speed
            self.right = True
            self.left = False
            self.up = False
            self.down = False
            self.lastMove = "right"
        elif self.keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
            self.up = True
            self.left = False
            self.right = False
            self.down = False
        elif self.keys[pygame.K_s] and self.y < winHeight - 35 - self.height - 1:  # высота не кратна 5
            self.y += self.speed
            self.down = True
            self.left = False
            self.right = False
            self.up = False
        else:
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.animCount = 0
        return self.x, self.y

    def drawHero(self):

        if self.animCount + 1 >= 15:
            self.animCount = 0
        if self.right or (self.right and self.up) or (self.right and self.down):
            win.blit(self.walkRight[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.left or (self.left and self.up) or (self.left and self.down):
            win.blit(self.walkLeft[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.up:
            win.blit(self.walkUp[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.down:
            win.blit(self.walkDown[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        else:
            win.blit(self.playerStand, (self.x, self.y))

    def drawName(self):
        f1 = pygame.font.Font(None, 30)
        text1 = f1.render('Alex', 1, (0, 0, 0))
        win.blit(text1, (Alex.x - 13, Alex.y - 40))

    def healthpoint(self):
        bar_length = 50
        bar_height = 10

        if self.hp < 0:
            self.hp = 0

        fill = (self.hp / 1000) * bar_length
        border_rect = pygame.Rect(self.x - 12, self.y - 15, bar_length, bar_height)
        fill_rect = pygame.Rect(self.x - 12, self.y - 15, int(fill), bar_height)
        pygame.draw.rect(win, (0, 255, 127), fill_rect)
        pygame.draw.rect(win, (0, 0, 0), border_rect, 1)

    def attack(self):

        if self.animCountS + 1 >= 15:
            self.animCountS = 0

        self.mkeys = pygame.mouse.get_pressed()
        hits = []
        enemy_hb = pygame.Rect(Ninja.x, Ninja.y, Ninja.width, Ninja.height)

        if self.lastMove == "right":
            self.facing = 1
            if self.mkeys[0]:
                hit = pygame.Rect(self.x + (26 * self.facing), self.y + 23, 25, 5)
                hit_draw = pygame.draw.rect(win, (255, 215, 0), hit, -1)
                win.blit(self.playerAttackR[self.animCountS // 5], (self.x + (15 * self.facing), self.y + 18))
                self.animCountS += 1
                hits.append((hit, hit_draw))
        else:
            self.facing = -1
            if self.mkeys[0]:
                hit = pygame.Rect(self.x + (26 * self.facing), self.y + 23, 25, 5)
                hit_draw = pygame.draw.rect(win, (255, 215, 0), hit, -1)
                win.blit(self.playerAttackL[self.animCountS // 5], (self.x + (20 * self.facing), self.y + 16))
                self.animCountS += 1
                hits.append((hit, hit_draw))

        for sword in hits:
            if enemy_hb.colliderect(sword[0]):
                Ninja.hp -= self.strength


class Enemy:

    def __init__(self, x, y, width, height, speed, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.hp = hp

        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.animCount = 0

        self.walkRight = [pygame.image.load('Enemy/Walk_R/Step1.png'), pygame.image.load('Enemy/Walk_R/Step2.png'),
                          pygame.image.load('Enemy/Walk_R/Step3.png')]
        self.walkLeft = [pygame.image.load('Enemy/Walk_L/Step1.png'), pygame.image.load('Enemy/Walk_L/Step2.png'),
                         pygame.image.load('Enemy/Walk_L/Step3.png')]
        self.walkUp = [pygame.image.load('Enemy/Walk_U/Step1.png'), pygame.image.load('Enemy/Walk_U/Step2.png'),
                       pygame.image.load('Enemy/Walk_U/Step3.png')]
        self.walkDown = [pygame.image.load('Enemy/Walk_D/Step1.png'), pygame.image.load('Enemy/Walk_D/Step2.png'),
                         pygame.image.load('Enemy/Walk_D/Step3.png')]
        self.playerStand = pygame.image.load('Enemy/Walk_D/Step2.png')

    def zoneEnemy(self):

        zone = pygame.Rect(self.x - 100, self.y - 100, self.width + 200, self.height + 200)
        zone1 = pygame.draw.rect(win, (0, 0, 0), zone, -1)

        zones = []
        zones.append((zone1, zone))

        for z in zones:
            hero_hb = pygame.Rect(heroPos, (Alex.width, Alex.height))
            if hero_hb.colliderect(z[1]):
                return True
            else:
                return False

    def moveEnemy(self):

        if self.x != Alex.x or self.y != Alex.y:
            if Alex.x > self.x + 25 and Alex.y > self.y + 25:
                self.x += self.speed
                self.y += self.speed

                self.right = True
                self.left = False
                self.up = False
                self.down = True

            elif Alex.x > self.x + 25 and Alex.y < self.y - 25:
                self.x += self.speed
                self.y -= self.speed

                self.right = True
                self.left = False
                self.up = True
                self.down = False

            elif Alex.x < self.x - 25 and Alex.y > self.y + 25:
                self.x -= self.speed
                self.y += self.speed

                self.right = False
                self.left = True
                self.up = False
                self.down = True

            elif Alex.x < self.x - 25 and Alex.y < self.y - 25:
                self.x -= self.speed
                self.y -= self.speed

                self.right = False
                self.left = True
                self.up = True
                self.down = False

            elif Alex.x > self.x + 25:
                self.x += self.speed

                self.right = True
                self.left = False
                self.up = False
                self.down = False

            elif Alex.x < self.x - 25:
                self.x -= self.speed

                self.right = False
                self.left = True
                self.up = False
                self.down = False

            elif Alex.y > self.y + 25:
                self.y += self.speed

                self.right = False
                self.left = False
                self.up = False
                self.down = True

            elif Alex.y < self.y - 25:
                self.y -= self.speed

                self.right = False
                self.left = False
                self.up = True
                self.down = False

            else:
                self.left = False
                self.right = False
                self.up = False
                self.down = False

                self.animCount = 0

    def drawEnemy(self):

        if self.animCount + 1 >= 15:
            self.animCount = 0
        if self.right or (self.right and self.up) or (self.right and self.down):
            win.blit(self.walkRight[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.left or (self.left and self.up) or (self.left and self.down):
            win.blit(self.walkLeft[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.up:
            win.blit(self.walkUp[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        elif self.down:
            win.blit(self.walkDown[self.animCount // 5], (self.x, self.y))
            self.animCount += 1
        if self.animCount == 0:
            win.blit(self.playerStand, (self.x, self.y))

    def healthpoint(self):
        bar_length = 50
        bar_height = 10

        if self.hp < 0:
            self.hp = 0

        fill = (self.hp / 100) * bar_length
        border_rect = pygame.Rect(self.x - 12, self.y - 15, bar_length, bar_height)
        fill_rect = pygame.Rect(self.x - 12, self.y - 15, int(fill), bar_height)
        pygame.draw.rect(win, (255, 0, 0), fill_rect)
        pygame.draw.rect(win, (0, 0, 0), border_rect, 1)

    def attack(self):
        if Alex.x <= self.x + 10 or Alex.y <= self.y + 10 or Alex.x >= self.x - 10 or Alex.y >= self.y - 10:
            Alex.hp -= 1


tree = Tree(290, 175)
Alex = Hero(67, 80, 26, 34, 6, 1000, 1)
Ninja = Enemy(random.randint(1, 1040), random.randint(1, 650), 26, 34, 1, 100)

heroPos = (Alex.x, Alex.y)


def touch():
    global heroPos

    hb_t = pygame.Rect(tree.x, tree.y, tree.width, tree.height)
    border1 = pygame.draw.rect(win, (0, 0, 0), hb_t, 1)

    savedPos = heroPos
    heroPos = Alex.moveHero(heroPos)

    borders = []
    borders.append((hb_t, border1))

    for border in borders:
        testRect = pygame.Rect(heroPos, (Alex.width, Alex.height))
        if testRect.colliderect(border[0]):
            heroPos = savedPos

def background():  # Функция заливки заднего фона
    bg = pygame.image.load('Backgrounds/bg.png')  # В переменную записываем адрес картинки
    win.blit(bg, (0, 0))  # Заливаем картинкой из bg, верхний левый угол картинки на координаты (0,0)


def DrawTrunk():
    tree.drawTrunk()


def DrawLeaf():
    tree.drawLeaf()


def LevelBar():
    global exp
    global e
    global fill
    global lvl
    bar_length = 1000
    bar_height = 25

    if death:
        exp += e
    if exp >= bar_length // 10:
        exp = (bar_length // 10 - exp) * -1
        lvl += 1
        Alex.strength += 1
        e -= 10 * lvl
    if e <= 0:
        e = 1

    fill = exp * 10
    border_rect = pygame.Rect(39, 689, bar_length + 1, bar_height + 1)
    fill_rect = pygame.Rect(40, 690, fill, bar_height)
    bg_rect = pygame.Rect(40, 690, bar_length, bar_height)
    pygame.draw.rect(win, (240, 230, 140), bg_rect)
    pygame.draw.rect(win, (255, 215, 0), fill_rect)
    pygame.draw.rect(win, (0, 0, 0), border_rect, 1)

    f1 = pygame.font.Font(None, 30)
    text2 = f1.render('Level: ' + str(lvl), 1, (0, 0, 0))
    win.blit(text2, (540, 693))


runGame = True
while runGame:

    fpsClock.tick(FPS)

    background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    DrawTrunk()
    if Alex.hp > 0:
        Alex.moveHero(heroPos)
        touch()
        Alex.drawHero()
        Alex.attack()
    else:
        heroPos = (67, 80)
        Alex.hp = 1000
    LevelBar()
    if Ninja.hp > 0:
        death = False
        Ninja.healthpoint()
        if Ninja.zoneEnemy():
            Ninja.moveEnemy()
            Ninja.drawEnemy()
            Ninja.attack()
        else:
            win.blit(Ninja.playerStand, (Ninja.x, Ninja.y))
    else:
        death = True
        Ninja.x = random.randint(1, 1040)
        Ninja.y = random.randint(1, 650)
        Ninja.hp = 100

    DrawLeaf()
    Alex.healthpoint()
    Alex.drawName()

    pygame.display.update()

pygame.quit()

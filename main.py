from pygame import *
from random import choice

init()
scr = display.set_mode((700, 500))
game = True
bg = transform.scale(image.load("fon.jpg"), (700, 500))
sources = ["1x1red.jpg", "1x1blue.png", "1x1_green.png", "orange.png"]
frame = time.Clock()
speed_flag = 0
global fallen
fallen = []
finish = False
global score
score = 0
f1 = font.Font(None, 30)
def printms(score):
    finish_text = f1.render(f"score:{score}", True, (212, 11, 11))
    scr.blit(finish_text, (50, 75))

def stop(j, i):
    fallen.append(j)
    blocks.remove(j)
    j.can_move = False


class gamesprites(sprite.Sprite):
    def __init__(self, imga, speed, px, py, x,y):
        self.img = transform.scale(image.load(imga), (px, py))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = speed
        self.can_move = True
    def show(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))


class block(gamesprites):
    def fall(self):
        if self.can_move:
            if self.rect.bottomleft[1] < 463:
                self.rect.y += self.velocity
            else:
                self.can_move = False
                return True
        return False

    def check_for_keypress(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.bottomleft[0] <= 437:
            if self.can_move:
                self.rect.x += 5
        if keys[K_a] and self.rect.bottomleft[0] >= 240:
            if self.can_move:
                self.rect.x -= 5
    def rotate1(self):
        rotated_image = transform.rotate(self.img, 90)
        x = self.rect.x
        y = self.rect.y
        self.img = rotated_image
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
                

    def increase_speed(self):
        if self.velocity < 7:
            if self.rect.y > 0:
                self.velocity += 3
    def decrease_speed(self):
        if self.velocity > 4:
            self.velocity -= 3

class partial_block():
    def __init__(self, img, speed, px, py, x, y, sections):
        self.img = transform.scale(image.load(img), (px, py))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.sections = sections
        self.partial = True
        self.switch = False
        self.velocity = speed
        self.can_move = True
        self.rect2_img = transform.scale(image.load(img), (25, 25 * sections))
        self.rect2 = self.rect2_img.get_rect()

    def show(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))
        scr.blit(self.rect2_img, (self.rect2.x, self.rect2.y))

    def fall(self):
        if self.can_move:
            if self.rect.bottom < 470 and self.rect2.bottom < 470:
                self.rect.y += self.velocity
                if not self.switch:
                    if self.sections == 2:
                        self.rect2.left = self.rect.right
                        self.rect2.centery = self.rect.top
                    else:
                        self.rect2.left = self.rect.right
                        self.rect2.top = self.rect.top
                else:
                    if self.sections == 2:
                        self.rect2.top = self.rect.bottom
                        self.rect2.centerx = self.rect.right
                    else:
                        self.rect2.top = self.rect.bottom
                        self.rect2.right = self.rect.right
            else:
                self.can_move = False
                return True
        return False

    def check_for_keypress(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.bottomleft[0] <= 437:
            if self.can_move:
                self.rect.x += 5
        if keys[K_a] and self.rect.bottomleft[0] >= 240:
            if self.can_move:
                self.rect.x -= 5

    def rotate1(self):
        rotated_image = transform.rotate(self.img, 90)
        x = self.rect.x
        y = self.rect.y
        self.img = rotated_image
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.sections > 1:
            rot2 = transform.rotate(self.rect2_img, 90)
            self.rect2_img = rot2
            self.rect2 = self.rect2_img.get_rect()
        if self.switch:
            self.switch = False
        else:
            self.switch = True

    def increase_speed(self):
        if self.velocity < 7:
            if self.rect.y > 0:
                self.velocity += 3
    def decrease_speed(self):
        if self.velocity > 4:
            self.velocity -= 3


blocks = []
for j in range(50):
    i = choice(sources)
    if "red" in i:
        tile = block(i, 4, 25, 25, 350, (j*-500))
        blocks.append(tile)
    if "blue" in i:
        tile = partial_block(i, 4, 25, 75, 350, (j*-500), 1)
        blocks.append(tile)
    if "green" in i:
        tile = block(i, 4, 25, 50, 350, (j*-500))
        blocks.append(tile)
    if 'orange' in i:
        tile = partial_block(i, 4, 25, 50, 350, (j*-500), 2)
        blocks.append(tile)
while game:
    rotate = False
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                rotate = True
            if i.key == K_w:
                speed_flag = 1
        if i.type == KEYUP:
            if i.key == K_w:
                speed_flag = 0

    scr.blit(bg, (0, 0))
    printms(len(fallen))
    for i in blocks:
        i.check_for_keypress()
        if rotate:
            i.rotate1()
        i.show()
        if i.fall():
            fallen.append(i)
            blocks.remove(i)
        if speed_flag == 1:
            i.increase_speed()
        if speed_flag == 0:
            i.decrease_speed()
    if len(fallen) > 0:
        for i in fallen:
            if i.rect.y <= 0:
                finish = True
            i.show()
            for j in blocks:
                try:
                    if (j.rect.right > i.rect.left and j.rect.left < i.rect.right and j.rect.bottom > i.rect.top and j.rect.top < i.rect.bottom) or (j.rect.right > i.rect2.left and j.rect.left < i.rect2.right and j.rect.bottom > i.rect2.top and j.rect.top < i.rect2.bottom) or (j.rect2.right > i.rect2.left and j.rect2.left < i.rect2.right and j.rect2.bottom > i.rect2.top and j.rect2.top < i.rect2.bottom) or (j.rect2.right > i.rect.left and j.rect2.left < i.rect.right and j.rect2.bottom > i.rect.top and j.rect2.top < i.rect.bottom) or (j.rect2.right > i.rect2.left and j.rect2.left < i.rect2.right and j.rect2.bottom > i.rect2.top and j.rect2.top < i.rect2.bottom):
                        stop(j, i)
                except:
                    pass

    if not finish:
        display.update()
        frame.tick(20)

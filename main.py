from pygame import *
from random import choice

init()
scr = display.set_mode((700, 500))
game = True
bg = transform.scale(image.load("fon.jpg"), (700, 500))
sources = ["1x1red.jpg", "1x1blue.png"]#, "1x1_green.png"
frame = time.Clock()
speed_flag = 0
global fallen
fallen = []

class gamesprites(sprite.Sprite):
    def __init__(self, imga, speed, px, py, x,y, sections):
        self.img = transform.scale(image.load(imga), (px, py))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = speed
        self.gravity = 3
        self.can_move = True
        self.more_sections = False
        self.rot = False
        if "blue" in imga:
            self.more_sections = True
            self.section_img = transform.scale(image.load(imga), (25, 25))
            self.rect2 = self.section_img.get_rect()
            self.rect2.left = self.rect.right
            self.rect2.top = self.rect.top
    def show(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))
        if self.more_sections:
            scr.blit(self.section_img, (self.rect2.x, self.rect2.y))

class block(gamesprites):
    def fall(self):
        if self.can_move and self.more_sections:
            if self.rect.bottom < 463 and self.rect2.bottom:
                self.rect.y += self.velocity
                if not self.rot:
                    self.rect2.left = self.rect.right
                    self.rect2.top = self.rect.top
                else:
                    self.rect2.top = self.rect.bottom
                    self.rect2.right = self.rect.right
            else:
                self.can_move = False
                return True
        return False            

        if self.can_move:
            if self.rect.bottom < 463:
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
        if not self.rot:
            if self.more_sections:
                self.rect2.top = self.rect.bottom
                self.rect2.right = self.rect.right
                self.rot = True
        else:
            self.rot = False
                

    def increase_speed(self):
        if self.velocity < 7:
            if self.rect.y > 0:
                self.velocity += 3
    def decrease_speed(self):
        if self.velocity > 4:
            self.velocity -= 3
    def set_move(self):
        self.can_move = False


blocks = []
for j in range(50):
    i = choice(sources)
    if "red" in i:
        tile = block(i, 4, 25, 25, 350, (j*-500), 1)
        blocks.append(tile)
    if "blue" in i:
        tile = block(i, 4, 25, 75, 350, (j*-500), 3)
        blocks.append(tile)
    if "green" in i:
        tile = block(i, 4, 25, 50, 350, (j*-500), 4)
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
            i.show()
            for j in blocks:
                try:
                    if j.rect.bottom > i.rect.top and j.rect.top < i.rect.bottom and j.rect.right > i.rect.left and j.rect.left < i.rect.right:
                        if i.rect.top < j.rect.bottom:
                            if j.rect.centerx > i.rect.right:
                                j.rect.left = i.rect.right
                            elif j.rect.centerx < i.rect.left:
                                j.rect.right = i.rect.left
                        fallen.append(j)
                        blocks.remove(j)
                    if j.more_sections:
                        if j.rect2.bottom > i.rect.top and j.rect2.top < i.rect.bottom and j.rect2.right > i.rect.left and j.rect2.left < i.rect.right:
                            if j.rect2.bottom > i.rect.top:
                                if j.rect2.bottom > i.rect.top:
                                    j.rect2.bottom = i.rect.top
                                if j.rect2.right > i.rect.left:
                                    j.rect2.right = i.rect.left
                                if j.rect2.left < i.rect.right:
                                    j.rect2.left = i.rect.right
                            fallen.append(j)
                            blocks.remove(j)
                        j.set_move()
                except:
                    pass


    display.update()
    frame.tick(20)

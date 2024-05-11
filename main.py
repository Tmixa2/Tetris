from pygame import *
from random import choice

init()
scr = display.set_mode((700, 500))
game = True
bg = transform.scale(image.load("fon.jpg"), (700, 500))
sources = ["1x1blue.png"]#["1x1red.jpg", "1x1blue.png", "1x1_green.png"]
frame = time.Clock()
speed_flag = 0
global fallen
fallen = []
def rect_collide(rect1, rect2):
    if rect2.rect.right > rect1.rect.left and rect2.rect.left < rect1.rect.right and rect2.rect.bottom > rect1.rect.top and rect2.rect.top < rect1.rect.bottom or rect2.part_rect.right > rect1.rect.left and rect2.part_rect.left < rect1.rect.right and rect2.part_rect.bottom > rect1.rect.top and rect2.part_rect.top < rect1.rect.bottom or rect2.part_rect.right > rect1.part_rect.left and rect2.part_rect.left < rect1.part_rect.right and rect2.part_rect.bottom > rect1.part_rect.top and rect2.part_rect.top < rect1.part_rect.bottom or rect2.rect.right > rect1.part_rect.left and rect2.rect.left < rect1.part_rect.right and rect2.rect.bottom > rect1.part_rect.top and rect2.rect.top < rect1.part_rect.bottom:
        return True
class gamesprites(sprite.Sprite):
    def __init__(self, imga, speed, px, py, x,y, sections, few_sections):
        self.img = transform.scale(image.load(imga), (px, py))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.few_sections = few_sections
        self.rect.y = y
        self.velocity = speed
        self.rot = False
        self.gravity = 3
        self.can_move = True
        if self.few_sections:
            self.part_img = transform.scale(image.load(imga), (25, 25))
            self.part_rect = self.part_img.get_rect()
    def show(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))
        if self.few_sections:
            scr.blit(self.part_img, (self.part_rect.x, self.part_rect.y))


class block(gamesprites):
    def fall(self):
        if self.few_sections:
            if self.rot:
                self.part_rect.top = self.rect.bottom
                self.part_rect.right = self.rect.right
            else:
                self.part_rect.left = self.rect.right
                self.part_rect.top = self.rect.top
        if self.can_move:
            if self.rect.bottom < 463 and self.part_rect.bottom < 463:
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
    def set_move(self):
        self.can_move = False
    def ret_y(self, y):
        if y - self.rect.bottom <= 3:
            pass
        else:
            self.rect.y += (y - self.rect.bottom)
    def get_y(self):
        return self.rect.top

blocks = []
for j in range(50):
    i = choice(sources)
    if "red" in i:
        tile = block(i, 4, 25, 25, 350, (j*-500), 1, False)
        blocks.append(tile)
    if "blue" in i:
        tile = block(i, 4, 25, 75, 350, (j*-500), 3, True)
        blocks.append(tile)
    if "green" in i:
        tile = block(i, 4, 25, 50, 350, (j*-500), 4, False)
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
        if i.type == KEYDOWN:
            pass


    scr.blit(bg, (0, 0))
    for i in blocks:
        i.check_for_keypress()
        if rotate:
            i.rotate1()
            if i.few_sections:
                if i.rot:
                    i.rot = False
                else:
                    i.rot = True
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
                if rect_collide(i, j):
                    if i.rect.top < j.rect.bottom:
                        if j.rect.centerx > i.rect.right:
                            j.rect.left = i.rect.right
                        elif j.rect.centerx < i.rect.left:
                            j.rect.right = i.rect.left
                    if j.few_sections:
                        if j.part_rect.bottom > i.rect.top:
                            j.part_rect.bottom = i.rect.top
                            j.rect.bottom = j.part_rect.top
                        else:
                            j.rect.bottom = i.rect.top
                            j.part_rect.left = j.rect.right
                            j.part_rect.top = j.rect.top
                        fallen.append(j)
                    blocks.remove(j)
                    j.set_move()


    display.update()
    frame.tick(20)

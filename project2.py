import pyxel
import random

# scenes
title = 0
instructions = 1
play = 2
end = 3
lose = 4

screen_width = 128
screen_height = 128

mound_count = 10
key_count = 3
mound_grid_nums = [25, 45, 65, 85, 105]


class App:
    def __init__(self):
        pyxel.init(screen_width, screen_height, caption="AquaCat")  # initiating, loading resources, establishing objects
        pyxel.load("resources1.pyxres") # load pixel art created in the pyxel editor
        self.scene = title
        self.key_collected = 0
        self.cat = Cat(0, 0)
        self.mound_list = [Mound(True) for i in range(key_count)] + [Mound(False) for i in range(mound_count - key_count)]
        self.chest = Chest(15, 15)
        self.bubble1 = Bubble(2, 120)
        self.bubble2 = Bubble(80, 40)
        self.bubble3 = Bubble(60, 160)
        self.fish1 = Fishie(42, 84)
        self.fish2 = Fishie(54, 84)
        self.fish3 = Fishie(66, 84)
        self.cat2 = InstructionsCat(65, 58)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): # quit with q key
            pyxel.quit()
        if self.scene == title: # update scenes when they are called
            self.update_title_scene()
        elif self.scene == instructions:
            self.update_instructions_scene()
        elif self.scene == play:
            self.update_play_scene()
        elif self.scene == end:
            self.update_end_scene()
        elif self.scene == lose:
            self.update_lose_scene()
        for mound in self.mound_list: # digging mounds
            if mound.x > self.cat.x - 7 and mound.x < self.cat.x + 7 \
                    and mound.y > self.cat.y - 7 and mound.y < self.cat.y + 7 \
                    and pyxel.btnp(pyxel.KEY_D):
                mound.dug = True
            if mound.key == True and mound.dug == True:
                self.key_collected += 1
        if self.key_collected >= 3 \
                and self.chest.x > self.cat.x - 10 and self.chest.x < self.cat.x + 10 \
                and self.chest.y > self.cat.y - 10 and self.chest.y < self.cat.y + 10 \
                and pyxel.btnp(pyxel.KEY_D): # check to win
            self.chest.imgx = 80
        if self.cat.timer < 0: # check to lose
            self.scene = lose
        if self.key_collected == 1: # change cat img to hold keys when they are picked up
            self.cat.imgx_key = 128
        elif self.key_collected == 2:
            self.cat.imgx_key = 112
        elif self.key_collected == 3:
            self.cat.imgx_key = 96

    def update_title_scene(self):
        self.fish1.update()
        self.fish2.update()
        self.fish3.update()
        if pyxel.btnp(pyxel.KEY_ENTER): # switch from title to instrucitons with enter key
            self.scene = instructions
        if pyxel.btnp(pyxel.KEY_S): # this was for testing, so i didn't have to play thru game to see/edit end screen
            self.scene = end
    def update_instructions_scene(self):
        self.cat2.update()
        if pyxel.btnp(pyxel.KEY_ENTER): # switch from instructions to play with enter key
            self.scene = play
    def update_play_scene(self): # update all
        self.cat.update()
        self.bubble1.update()
        self.bubble2.update()
        self.bubble3.update()
        for mound in self.mound_list:
            mound.update()
        if self.cat.timer < 0 and self.key_collected < 3: # check for lose
            self.scene = lose
        if self.chest.imgx == 80 and self.key_collected >= 3: # check for win
            self.scene = end
    def update_end_scene(self):
        self.cat.update()
        self.bubble1.update()
        self.bubble2.update()
        self.bubble3.update()
    def update_lose_scene(self):
        pass



    def draw(self):
        pyxel.cls(0)
        if self.scene == title: # draw scenes when called
            self.draw_title_scene()
        elif self.scene == instructions:
            self.draw_instructions_scene()
        elif self.scene == play:
            self.draw_play_scene()
        elif self.scene == end:
            self.draw_end_scene()
        elif self.scene == lose:
            self.draw_lose_scene()

    def draw_title_scene(self): # drawing title scene
        pyxel.rect(0, 0, screen_width, screen_height, 3)
        pyxel.rect(6,6, screen_width - 12, screen_height - 12, 11)
        pyxel.rect(15, 15, screen_width - 30, 56, pyxel.frame_count % 16)
        pyxel.rect(16, 16, screen_width - 32, 54, 0)
        pyxel.blt(54, 26, 0, 16, 0, 16, 16, 0) # cat
        pyxel.blt(34, 26, 0, 32, 16, 16, 16, 0) # mouse 1
        pyxel.blt(74, 26, 0, 32, 16, 16, 16, 0) # mouse 2
        self.fish1.draw()
        self.fish2.draw()
        self.fish3.draw()
        pyxel.text(29, 46, "The Adventures of", pyxel.frame_count % 16)
        pyxel.text(50, 56, "AQUACAT", pyxel.frame_count % 16)
        pyxel.text(18, 76, "- PRESS ENTER TO PLAY -", 3)
        pyxel.text(37, 102, "Help her find", 3)
        pyxel.text(27, 110, "the lost tuna can!", 3)
    def draw_instructions_scene(self):  # drawing instrucitons scene
        pyxel.rect(0, 0, screen_width, screen_height, 11)
        pyxel.rect(5, 103, screen_width - 10, 20, pyxel.frame_count % 16)
        pyxel.rect(6, 104, screen_width - 12, 18, 0)
        pyxel.rect(5, 5, screen_width - 10, 30, 3)
        pyxel.rect(8, 8, screen_width - 16, 24, 7)
        pyxel.text(30, 18, "- INSTRUCTIONS -", 3)
        pyxel.blt(85, 44, 0, 64, 0, 16, 16, 0) # mound
        pyxel.text(10, 40, "Press \"D\" to dig", 3)
        pyxel.text(10, 50, "Look for dig sites:", 3)
        pyxel.text(10, 60, "Collect keys:", 3)
        self.cat2.draw()
        pyxel.blt(94, 59, 0, 16, 16, 16, 16, 0)  # chest
        pyxel.blt(83, 59, 0, 80, 0, 16, 16, 0) # key
        pyxel.text(10, 75, "Find 3 keys", 3)
        pyxel.text(10, 81, "and unlock the chest with", 3)
        pyxel.text(10, 89, "\"D\" to win in 30 seconds!", 3)
        pyxel.text(18, 110, "- PRESS ENTER TO PLAY -", pyxel.frame_count % 16)
    def draw_play_scene(self): # drawing play scene
        pyxel.bltm(0,0,1,0.5,0.5,160,120)
        pyxel.clip(self.cat.x - 4, self.cat.y - 4, 25, 25)
        for mound in self.mound_list:
            mound.draw()
        self.chest.draw()
        self.cat.draw()
        self.bubble1.draw()
        self.bubble2.draw()
        self.bubble3.draw()
    def draw_end_scene(self):  # drawing end scene
        self.cat.timer_show = False
        self.cat.end = True
        pyxel.clip()
        pyxel.bltm(0, 0, 1, 0.5, 0.5, 160, 120)
        self.chest.draw()
        pyxel.blt(43, 30, 0, 64, 36, 64, 64, 0)  # TUNA CAN!!
        self.cat.draw()
        self.bubble1.draw()
        self.bubble2.draw()
        self.bubble3.draw()
        pyxel.rect(8, 65, screen_width - 16, 45, pyxel.frame_count % 16)
        pyxel.rect(9, 66, screen_width - 18, 43, 0)
        pyxel.text(13, 70, "Congratulations, you found", 3)
        pyxel.text(20, 80, "The Golden Tuna Can in:", 3)
        pyxel.text(42, 93, str(30 - self.cat.timer), pyxel.frame_count % 16)
        pyxel.text(52, 93, "SECONDS!", pyxel.frame_count % 16)
        pyxel.text(24, 115, "- PRESS Q TO EXIT -", 0)
    def draw_lose_scene(self):
        pyxel.clip()
        pyxel.rect(0, 0, screen_width, screen_height, 0)
        pyxel.text(24, 95, "- PRESS Q TO EXIT -", 7)
        pyxel.blt(55, 30, 0, 144, 0, 16, 16, 0)
        pyxel.text(45, 50, "GAME OVER", 8)
        pyxel.text(20, 60, "Better luck next time!", 7)



class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.digging = False
        self.right = True
        self.imgx_key = 180
        self.imgy_key = 0
        self.img = 0
        self.timer = 30
        self.timer_show = True
        self.end = False
    def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT): # arrow controls to be replaced
            self.x += 4
            self.right = True
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 4
            self.right = False
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 4
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 4
        if self.x < -1: # screen bounds
            self.x = -1
        elif self.y < -3:
            self.y = -3
        elif self.x > 113:
            self.x = 113
        elif self.y > 113:
            self.y = 113
        if self.right == True:
            self.img = 0
            self.imgy_key = 0
        else:
            self.img = 32
            self.imgy_key = 16

        if pyxel.frame_count % 30 == 0 and self.end == False: # timer count down
            self.timer -= 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.img, 0, 16, 16, 0) # draw cat
        pyxel.blt(self.x, self.y, 0, self.imgx_key, self.imgy_key, 16, 16, 0) # draw key count
        if self.timer_show == True:
            pyxel.text(self.x - 2, self.y - 3, "0:", 0)
            pyxel.text(self.x + 5, self.y - 3, str(self.timer), 0)



class Bubble:
    def __init__(self, x, y):
        self. x = x
        self.y = y
    def update(self): # bubble loops
        self.y -= 0.3
        if self.y < -40:
            self.y = 160
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16, 0)

class Fishie:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imgy = 16
    def update(self):
        self.x -= 0.7
        if self.x <= -16:
            self.x = 120
        if pyxel.frame_count % 10 == 0:
            if self.imgy == 16:
                self.imgy = 0
            else:
                self.imgy = 16
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, self.imgy, 16, 16, 0)  # fish 1


class Mound:
    def __init__(self, bool):
        self.x = mound_grid_nums[random.randrange(5)]
        self.y = mound_grid_nums[random.randrange(5)]
        self.dug = False
        self.key = bool
        self.imgy = 0
    def update(self):
        if self.dug == True:
            self.imgy = 16
            self.dug = False
    def draw(self):
        pyxel. blt(self.x, self.y, 0, 64, self.imgy, 16, 16, 0)


class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imgx = 16
    def update(self):
        pass
    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.imgx, 16, 16, 16, 0)

class InstructionsCat: # the animated cat on the instructions page
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imgx = 180
    def update(self):
        if pyxel.frame_count % 10 == 0:
            if self.imgx == 180:
                self.imgx = 128
            elif self.imgx == 128:
                self.imgx = 112
            elif self.imgx == 112:
                self.imgx = 96
            elif self.imgx == 96:
                self.imgx = 180
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 16, 16, 0)
        pyxel.blt(self.x, self.y, 0, self.imgx, 0, 16, 16, 0)


App()

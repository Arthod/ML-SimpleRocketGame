from rocket import Rocket
import pygame as pg
import math
import random

class Main:
    def __init__(self):
        self.rocket = []
        for i in range(10):
            self.rocket.append(Rocket(200, 0))

        #Walls
        self.walls = []
        hole_width = 100
        hole_height = 20
        for i in range(20):
            hole_pos = random.randint(0, 400)
            self.walls.append((hole_pos - hole_width/2, i*hole_height*1.5 + 100, hole_width, hole_height))

        #Pygame
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        self.font = pg.font.SysFont("monospace", 15)
        clock = pg.time.Clock()
        pg.font.init()

        done = False
        while not done:
            self.draw(pg)
            #Init
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            for i in range(len(self.rocket)):
                collision = []
                for j in range(len(self.rocket[i].get_vision_positions())):
                    collision.append(0)
                    for k in range(len(self.walls)):
                        if self.check_collision(self.rocket[i].get_vision_positions()[j], self.walls[k]):
                            collision[j] = 1
                
                for j in range(len(self.walls)):
                    if self.check_collision((self.rocket[i].x, self.rocket[i].y), self.walls[j]):
                        self.rocket[i].alive = False
                        self.rocket[i].score = self.rocket[i].y

                self.rocket[i].loop(collision)

            alive = 0
            for i in range(len(self.rocket)):
                if self.rocket[i].alive == 1:
                    alive += 1
            if alive == 0:  #All dead
                #Bubble sort ranking
                for i in range(len(self.rocket)):
                    for j in range(len(self.rocket)):
                        if i != j:
                            if self.rocket[i].score > self.rocket[j].score:
                                temp = self.rocket[i]
                                self.rocket[i] = self.rocket[j]
                                self.rocket[j] = temp

                #Kill half population
                pop_amount = round(len(self.rocket)/2)
                self.rocket = self.rocket[:-pop_amount or None]

                for i in range(len(self.rocket)):
                    self.rocket[i].x = 200
                    self.rocket[i].y = 0
                    self.rocket[i].alive = 1

            pg.display.flip()
            clock.tick(60)


    def check_collision(self, pos, rectangle):
        r_x = pos[0]
        r_y = pos[1]
        if r_x > rectangle[0] and r_x < rectangle[2] + rectangle[0] and r_y > rectangle[1] and r_y < rectangle[3] + rectangle[1]:
            return True
        elif r_x < 0 or r_x > 400 or r_y > 600:
            return True
        else:
            return False

    def draw(self, pygame):
        def rect(x, y, w, h, color_rgb):
            pygame.draw.rect(self.screen, color_rgb, pygame.Rect(x, y, w, h))
        def text(x, y, font, txt, color_rgb=(0, 0, 0)):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        rect(0, 0, 800, 600, (255, 255, 255))

        for j in range(len(self.rocket)):
            rect(self.rocket[j].x, self.rocket[j].y, 20, 20, (0, 0, 0))
            for i in range(len(self.rocket[j].get_vision_positions())):
                rect(self.rocket[j].get_vision_positions()[i][0], self.rocket[j].get_vision_positions()[i][1], 10, 10, (0, 0, 255))

        #Walls
        for i in range(len(self.walls)):
            rect(self.walls[i][0], self.walls[i][1], self.walls[i][2], self.walls[i][3],(180, 180, 180))

        #GUI
        rect(400, 0, 400, 600, (190, 190, 190))
        text(400+10, 10, self.font, "best score: " + str(self.rocket[0].score), (0, 0, 0))
        text(400+10, 30, self.font, "top 10: ", (0, 0, 0))
        for i in range(len(self.rocket)):
            text(400+20, 50+i*1*20, self.font, "score: " + str(self.rocket[i].score) + " | alive: " + str(self.rocket[i].alive))

main = Main()
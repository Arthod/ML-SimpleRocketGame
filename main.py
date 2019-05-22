from rocket import Rocket
import pygame as pg
import math
import random

class Main:
    def __init__(self):
        self.rocket = []
        for i in range(100):
            self.rocket.append(Rocket(200, 0))

        #Walls
        self.generate_walls()

        #Pygame
        pg.init()
        self.screen = pg.display.set_mode((1200, 600))
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
                if self.rocket[i].alive:
                    for j in range(len(self.rocket[i].get_vision_positions())):
                        collision.append(0)
                        for k in range(len(self.walls)):
                            if self.check_vision_collision((self.rocket[i].x, self.rocket[i].y), self.rocket[i].get_vision_positions()[j], self.walls[k]):
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
                            if self.rocket[i].score-1 > self.rocket[j].score:
                                temp = self.rocket[i]
                                self.rocket[i] = self.rocket[j]
                                self.rocket[j] = temp

                #Kill half population
                pop_amount = round(len(self.rocket)/2)
                self.rocket = self.rocket[:-pop_amount or None]

                for i in range(len(self.rocket)):
                    self.rocket[i].x = 200
                    self.rocket[i].y = 0
                    self.rocket[i].alive = True

                #Children
                for i in range(pop_amount):
                    self.rocket.append(Rocket(200, 0))
                    self.rocket[i + pop_amount].perceptron.weights = self.produce_child(self.rocket[0].perceptron.weights, self.rocket[i].perceptron.weights)
                    self.rocket[i + pop_amount].vision = (self.rocket[0].vision + self.rocket[i].vision)/2 + random.uniform(-10, 10)
                
                for i in range(len(self.rocket)):
                    if self.rocket[i].score > 600:
                        self.generate_walls()

            pg.display.flip()
            clock.tick(60)

    def generate_walls(self):
        self.walls = []
        self.hole_width = 50
        self.hole_height = 40
        self.hole_pos = 200
        for i in range(int((600-100)/self.hole_height)):
            self.hole_pos += random.randint(int(-self.hole_width/2.0), int(self.hole_width/2.0))
            self.walls.append((0, i*self.hole_height+100, self.hole_pos-self.hole_width/2.0, self.hole_height))
            self.walls.append((self.hole_pos+self.hole_width/2.0, i*self.hole_height+100, 400-(self.hole_pos+self.hole_width/2.0), self.hole_height))

    def produce_child(self, weights1, weights2):
        child_weight = []
        for i in range(len(weights1)):
            child_weight.append(round((weights1[i] + weights2[2])/2.0 + random.uniform(-1, 1),3))
        return child_weight

    def check_collision(self, pos, rectangle):
        r_x = pos[0]
        r_y = pos[1]
        if r_x > rectangle[0] and r_x < rectangle[2] + rectangle[0] and r_y > rectangle[1] and r_y < rectangle[3] + rectangle[1]:
            return True
        elif r_y > 600:
            return True
        else:
            return False
    
    def check_vision_collision(self, rocket_pos, pos, rectangle):
        r_x = pos[0]
        r_y = pos[1]
        if r_x > rectangle[0] and r_x < rectangle[2] + rectangle[0] and r_y > rectangle[1] and r_y < rectangle[3] + rectangle[1]:
            return True
        elif r_x < 0 or r_x > 400 or r_y > 600:
            return True
        
        #Get all points in a line
        points_to_get = 10.0
        points = []
        vec = ((rocket_pos[0] - pos[0])/points_to_get, (rocket_pos[1] - pos[1])/points_to_get)
        for i in range(round(points_to_get)):
            points.append((vec[0] * i + pos[0], vec[1] * i + pos[1]))
        for i in range(len(points)):
            if self.check_collision(points[i], rectangle):
                return True
        return False

    def draw(self, pygame):
        def rect(x, y, w, h, color_rgb):
            pygame.draw.rect(self.screen, color_rgb, pygame.Rect(x, y, w, h))
        def text(x, y, font, txt, color_rgb=(0, 0, 0)):
            text = font.render(txt, False, color_rgb)
            self.screen.blit(text, (x, y))
        def line(x0, y0, x1, y1, color_rgb=(0, 0, 0)):
            pygame.draw.line(self.screen, color_rgb, (x0, y0), (x1, y1))
        rect(0, 0, 1600, 600, (255, 255, 255))

        for j in range(len(self.rocket)):
            rect(self.rocket[j].x, self.rocket[j].y, 10, 10, (0, 0, 0))
            for i in range(len(self.rocket[j].get_vision_positions())):
                line(self.rocket[j].x, self.rocket[j].y, self.rocket[j].get_vision_positions()[i][0], self.rocket[j].get_vision_positions()[i][1])
                rect(self.rocket[j].get_vision_positions()[i][0], self.rocket[j].get_vision_positions()[i][1], 2, 2, (0, 0, 255))

        #Walls
        for i in range(len(self.walls)):
            rect(self.walls[i][0], self.walls[i][1], self.walls[i][2], self.walls[i][3], (180, 180, 180))

        #GUI
        rect(400, 0, 1200, 600, (190, 190, 190))
        text(400+10, 10, self.font, "best score: " + str(self.rocket[0].score), (0, 0, 0))
        text(400+10, 30, self.font, "top 10: ", (0, 0, 0))
        for i in range(len(self.rocket)):
            if self.rocket[i].alive:
                text(400+20, 50+i*1*20, self.font, "score: " + str(self.rocket[i].score) + " | vision: " + str(round(self.rocket[i].vision, 2)) + " | weights: " + str(self.rocket[i].perceptron.weights))
            else:
                text(400+20, 50+i*1*20, self.font, "score: " + str(self.rocket[i].score) + " | vision: " + str(round(self.rocket[i].vision, 2)) + " | weights: " + str(self.rocket[i].perceptron.weights), (255, 0, 0))
main = Main()
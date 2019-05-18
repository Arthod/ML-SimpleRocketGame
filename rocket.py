import math
from perceptron import Perceptron


class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.perceptron = Perceptron(5)
        self.cirkel_radius = 100
        self.alive = True
        self.score = 0

        self.loop([0, 0, 0, 0, 0, 0])

    def loop(self, inputs):
        if self.alive:
            self.vision_pos = []
            for i in range(1, 6):
                t = math.pi / 6.0
                y = self.cirkel_radius + self.y
                x = math.cos(round(i) * t) * self.cirkel_radius + self.x
                #y = math.sin(round(i) * t) * self.cirkel_radius + self.y
                self.vision_pos.append((x, y))
            self.y += 10

            percept = self.perceptron.return_value(inputs)
            '''
            if percept == 1:
                self.x += 1
            elif percept == -1:
                self.x -= 1
            '''
            if not(-1 < percept*10 < 1):
                self.x += percept*10
        

    def get_vision_positions(self):
        return self.vision_pos
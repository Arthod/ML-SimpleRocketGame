import random

class Perceptron:
    def __init__(self, inputs_amount):
        self.weights = []
        for i in range(inputs_amount):
            self.weights.append(random.randint(0, 10)-5)

    def return_value(self, input):
        sum = 0
        for i in range(len(self.weights)):
            sum += self.weights[i] * input[i]
        return sum

    def zeta(self, n):
        if n > 0:
            return -1
        elif n < 0:
            return 1
        else:
            return 0
from Scenes.theme import *


class Disruptor(object):

    def __init__(self, img):
        self.triggered = False
        self.img = img
        self.x = 0
        self.y = 0

    def draw(self):
        self.img.draw(self.x, self.y)

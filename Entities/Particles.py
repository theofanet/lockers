class Particle(object):
    def __init__(self, life=1, size=5, color=(255, 0, 0)):
        self._life = life
        self._size = size
        self._color = color

    def update(self, elapsed_time):
        pass

    def draw(self):
        pass


class ParticleEmitter(object):
    def __init__(self, position):
        self._position = position


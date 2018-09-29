from PyGnin import *
import math
import random
import pygame


class Particle(object):
    def __init__(self, velocity, position, life=5, size=20, c=(255, 0, 0), c2=()):
        self._position = position
        self._life = life
        self._size = size
        self._color = c
        self._velocity = velocity
        self._live_time = 0

    def update(self):
        t = App.get_time() / 1000
        self._live_time += t
        if self._live_time > self._life:
            return False
        else:
            x, y = self._position
            vx, vy = self._velocity
            self._position = (
                x + vx * t,
                y + vy * t
            )
            return True

    def draw(self):
        print(self._position)
        ratio = 1.0 - self._live_time / self._life
        s = pygame.Surface((self._size, self._size))
        s.set_alpha(ratio * 255)
        s.fill(self._color)
        App.get_display().blit(s, self._position)
        #x, y = self._position
        #pygame.draw.rect(App.get_display(), self._color, pygame.Rect(x, y,  self._size, self._size))


class ParticleEmitter(object):
    def __init__(self, position, pps, direction, life=5, size=20):
        self._position = position
        self._pps = pps
        self._direction = direction
        self._particles = []
        self._position_ranges = [(0, 0), (0, 0)]
        self._particle_size = size
        self._particle_life = life
        self._life_range = (0, 0)
        self._size_range = (0, 0)

    def update(self):
        self._particles = [particle for particle in self._particles if particle.update()]
        self.generate_particles()

    def set_ranges(self, x_range=(0, 0), y_range=(0, 0), size=(0, 0), life=(0, 0)):
        self._position_ranges = [x_range, y_range]
        self._life_range = life
        self._size_range = size

    def generate_particles(self):
        delta = App.get_time() / 1000
        particle_to_create = self._pps * delta
        count = int(math.floor(particle_to_create))
        partial_particle = particle_to_create % 1
        for i in range(0, count):
            self.emit_particle()
        if random.random() < partial_particle:
            self.emit_particle()

    def emit_particle(self):
        velocity = self._direction
        x, y = self._position
        position = (
            x + random.randint(self._position_ranges[0][0], self._position_ranges[0][1]),
            y + random.randint(self._position_ranges[1][0], self._position_ranges[1][1])
        )
        life = self._particle_life + random.randint(self._life_range[0], self._life_range[1])
        size = self._particle_size + random.randint(self._size_range[0], self._size_range[1])
        self._particles.append(Particle(velocity, position, life=life, size=size))

    def draw(self):
        for particle in self._particles:
            particle.draw()

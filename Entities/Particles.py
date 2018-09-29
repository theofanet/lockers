from PyGnin import *
import math
import random
import pygame


class Particle(object):
    def __init__(self, velocity, position, life=5, size=20, c=(18, 203, 196), c2=(0, 148, 50)):
        self._position = position
        self._life = life if life > 0 else 1
        self._size = size if size > 0 else 1
        self._color = c
        self._color2 = c2
        self._velocity = velocity
        self._live_time = 0
        self._img = None # Render.Image("assets/particle2.png", scale=0.15, color=c)
        self._surface = pygame.Surface((self._size, self._size))

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

    def get_color(self, darken=0.6):
        r1, g1, b1 = self._color
        r2, g2, b2 = self._color2
        return (
            (r1 + ((r2 - r1) / self._life) * self._live_time) * darken,
            (g1 + ((g2 - g1) / self._life) * self._live_time) * darken,
            (b1 + ((b2 - b1) / self._life) * self._live_time) * darken
        )

    def draw(self):
        ratio = 1.0 - self._live_time / self._life
        if self._img is None:
            self._surface = pygame.transform.scale(self._surface, (int(ratio * self._size), int(ratio * self._size)))
            self._surface.set_alpha(ratio * 255)
            self._surface.fill(self.get_color())
            App.get_display().blit(self._surface, self._position)
        else:
            x, y = self._position
            self._img.set_color_t(self.get_color())
            self._img.draw(x, y, at_center=True)


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
        self._direction_range = [(0, 0), (0, 0)]

    def update(self):
        self._particles = [particle for particle in self._particles if particle.update()]
        self.generate_particles()

    def set_ranges(self, x_range=(0, 0), y_range=(0, 0), size=(0, 0), life=(0, 0), direction_x=(0, 0), direction_y=(0, 0)):
        self._position_ranges = [x_range, y_range]
        self._direction_range = [direction_x, direction_y]
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

    def emit_particle(self, i=None):
        vx, vy = self._direction
        velocity = [
            vx + random.randint(self._direction_range[0][0], self._direction_range[0][1]),
            vy + random.randint(self._direction_range[1][0], self._direction_range[1][1])
        ]
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

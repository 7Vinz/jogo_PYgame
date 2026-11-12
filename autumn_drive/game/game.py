"""Logica e estados do jogo (title / play / over). Nao desenha nada."""
import random
import pygame

from .config import (MAX_SPEED, OFFROAD_MAX_SPEED, ACCEL, BRAKE, COAST_DECEL, STEER_RATE,
                     CENTRIFUGAL, START_TIME, CHECKPOINT_DIST, CHECKPOINT_BONUS,
                     CRASH_SPEED_FACTOR, CRASH_INVULN)
from .track import L, curve_at
from .traffic import new_traffic, update_traffic

TITLE, PLAY, OVER = "title", "play", "over"


class Game:
    def __init__(self, sprite_count):
        self.rng = random.Random()
        self.sprite_count = sprite_count
        self.state = TITLE
        self.t = 0.0
        self.reset()

    def reset(self):
        self.pos = 0.0          # posicao na pista
        self.px = 0.0           # posicao lateral (-1 .. 1 = pista)
        self.speed = 0.0
        self.time = START_TIME
        self.score = 0.0
        self.dist = 0.0
        self.cp = 0
        self.inv = 0.0          # invulnerabilidade pos-batida
        self.shake = 0.0
        self.msg_t = 0.0        # tempo de exibicao da msg de checkpoint
        self.over_t = 0.0
        self.steer_vis = 0
        self.cars = new_traffic(self.rng, self.sprite_count)

    def start_play(self):
        self.reset()
        self.state = PLAY

    # ------------------------------------------------------------------
    def update(self, dt, start, keys, touch_x):
        self.t += dt
        update_traffic(self.cars, dt)

        if self.state == TITLE:
            self.pos = (self.pos + 22 * dt) % L      # demo automatica
            if start:
                self.start_play()
        elif self.state == OVER:
            self._update_over(dt, start)
        else:
            self._update_play(dt, keys, touch_x)

    def _update_over(self, dt, start):
        self.over_t += dt
        self.speed = max(0.0, self.speed - 15 * dt)
        self.pos = (self.pos + self.speed * dt) % L
        if start and self.over_t > 1.0:
            self.start_play()

    def _update_play(self, dt, keys, touch_x):
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        up = keys[pygame.K_UP] or keys[pygame.K_w]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        if touch_x:                                  # controle por toque
            up = True
            left = left or touch_x < 0.33
            right = right or touch_x > 0.67

        # velocidade
        maxs = OFFROAD_MAX_SPEED if abs(self.px) > 1.0 else MAX_SPEED
        if up and self.speed < maxs:
            self.speed += ACCEL * dt
        elif down:
            self.speed -= BRAKE * dt
        else:
            self.speed -= COAST_DECEL * dt
        if self.speed > maxs:
            self.speed -= 35 * dt
        self.speed = max(0.0, self.speed)

        # direcao + forca centrifuga
        sp = self.speed / MAX_SPEED
        self.steer_vis = (1 if right else 0) - (1 if left else 0)
        self.px += self.steer_vis * sp * dt * STEER_RATE
        self.px -= curve_at(self.pos) * sp * sp * dt * CENTRIFUGAL
        self.px = max(-1.7, min(1.7, self.px))

        # avanco, pontos, tempo
        step = self.speed * dt
        self.pos = (self.pos + step) % L
        self.dist += step
        self.score += step * 10
        self.time -= dt
        self.inv = max(0.0, self.inv - dt)
        self.shake = max(0.0, self.shake - dt)
        self.msg_t = max(0.0, self.msg_t - dt)

        if int(self.dist / CHECKPOINT_DIST) > self.cp:
            self.cp = int(self.dist / CHECKPOINT_DIST)
            self.time += CHECKPOINT_BONUS
            self.msg_t = 2.0

        self._check_collisions()

        if self.time <= 0:
            self.time = 0
            self.state = OVER
            self.over_t = 0.0

    def _check_collisions(self):
        if self.inv > 0:
            return
        for c in self.cars:
            dz = (c['z'] - self.pos + L / 2) % L - L / 2     # distancia com sinal
            if -0.4 < dz < 1.1 and abs(c['x'] - self.px) < 0.3:
                self.speed *= CRASH_SPEED_FACTOR
                self.inv = CRASH_INVULN
                self.shake = 0.4
                c['z'] = (c['z'] + 10) % L                   # empurra o carro batido
                break

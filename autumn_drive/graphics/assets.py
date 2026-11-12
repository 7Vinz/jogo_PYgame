"""Carrega/gera todos os recursos graficos uma unica vez."""
import random
import pygame

from game.track import L
from .sprites import (PALETTES, TRAFFIC_COLORS, make_tree, make_car)
from .sky import make_sky

TREE_SPACING = 3


class Assets:
    def __init__(self):
        self.font = pygame.font.Font(None, 18)
        self.big = pygame.font.Font(None, 34)
        self.sky = make_sky()
        self.tree_sprites = [make_tree(p, i) for i, p in enumerate(PALETTES)]
        self.car_sprites = [make_car(*c) for c in TRAFFIC_COLORS]
        self.player_sprite = pygame.transform.scale(
            make_car((220, 70, 40), (150, 35, 40), (250, 135, 75), tail=(255, 60, 40)), (88, 47))

        # posicao fixa das arvores ao longo do circuito: (z, lado, variacao, afastamento)
        rng = random.Random(7)
        self.trees = []
        for i in range(L // TREE_SPACING):
            for side in (-1, 1):
                self.trees.append((i * TREE_SPACING + rng.uniform(0, 1.5), side,
                                   rng.randrange(len(PALETTES)), rng.uniform(0, 0.4)))

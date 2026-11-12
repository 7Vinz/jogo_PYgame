"""Pre-renderiza o fundo: ceu em faixas, nuvens, raios de sol e arvores distantes."""
import random
import pygame

from game.config import W, HORIZON
from .sprites import PALETTES


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_sky():
    h = HORIZON + 12
    s = pygame.Surface((W, h))

    # degrade em faixas (efeito pixel art)
    top, bot = (0, 205, 235), (255, 238, 125)
    bands = 18
    for i in range(bands):
        t = (i / (bands - 1)) ** 1.7
        y0, y1 = int(i * h / bands), int((i + 1) * h / bands)
        s.fill(lerp(top, bot, t), (0, y0, W, y1 - y0))

    # nuvens (sombra + corpo branco)
    puffs = ((-18, 4, 9), (-6, -2, 12), (8, 0, 11), (20, 4, 8), (0, 6, 10))
    for (cx, cy, sc) in ((40, 22, 1.0), (235, 38, 1.2), (150, 62, 0.8), (285, 14, 0.7), (95, 55, 0.6)):
        for dx, dy, r in puffs:
            pygame.draw.circle(s, (170, 205, 235), (int(cx + dx * sc), int(cy + dy * sc) + 2), int(r * sc))
        for dx, dy, r in puffs:
            pygame.draw.circle(s, (250, 252, 255), (int(cx + dx * sc), int(cy + dy * sc)), int(r * sc) - 1)

    # raios de sol
    rays = pygame.Surface((W, h), pygame.SRCALPHA)
    for poly in ([(70, 0), (86, 0), (172, HORIZON), (150, HORIZON)],
                 [(96, 0), (106, 0), (178, HORIZON), (162, HORIZON)],
                 [(135, 0), (215, 0), (215, HORIZON), (172, HORIZON)]):
        pygame.draw.polygon(rays, (255, 255, 200, 55), poly)
    s.blit(rays, (0, 0))

    # brilho no horizonte
    glow = pygame.Surface((W, h), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (255, 245, 140, 110), (W // 2 - 70, HORIZON - 30, 140, 50))
    s.blit(glow, (0, 0))

    # linha de arvores distantes
    rng = random.Random(3)
    cols = [p[1] for p in PALETTES] + [p[0] for p in PALETTES]
    for _ in range(60):
        pygame.draw.circle(s, rng.choice(cols),
                           (rng.randint(-10, W + 10), HORIZON - 2 - rng.randint(0, 5)), rng.randint(6, 13))
    s.fill((190, 60, 32), (0, HORIZON, W, 12))
    return s

"""Geracao procedural dos sprites (arvores e carros) - sem arquivos de imagem."""
import random
import pygame

# (escuro, medio, claro) de cada variacao de copa de arvore
PALETTES = [((190, 60, 20), (235, 130, 25), (250, 195, 50)),
            ((140, 35, 30), (205, 65, 30), (235, 125, 35)),
            ((95, 120, 20), (165, 175, 30), (220, 220, 75)),
            ((210, 90, 20), (240, 160, 30), (160, 190, 40))]

TREE_W, TREE_H = 128, 176


def make_tree(pal, seed):
    rng = random.Random(seed)
    s = pygame.Surface((TREE_W, TREE_H), pygame.SRCALPHA)
    lean = rng.randint(-3, 3)
    # tronco de bétula
    pygame.draw.polygon(s, (225, 225, 215), [(57, 176), (73, 176), (70 + lean, 60), (59 + lean, 60)])
    pygame.draw.polygon(s, (150, 155, 165), [(67, 176), (73, 176), (70 + lean, 60), (65 + lean, 60)])
    for _ in range(16):
        y = rng.randint(72, 172)
        x = 59 + rng.randint(0, 9)
        pygame.draw.rect(s, (55, 55, 70), (x, y, rng.randint(2, 4), 2))
    pygame.draw.line(s, (215, 215, 205), (64 + lean, 96), (36, 62), 3)
    pygame.draw.line(s, (215, 215, 205), (66 + lean, 90), (94, 58), 3)
    # copa em 3 camadas (sombra, meio, luz)
    blobs = [(rng.uniform(-46, 46), rng.uniform(-22, 22), rng.randint(15, 24)) for _ in range(15)]
    cx, cy = 64, 52
    for col, off, shrink in ((pal[0], (0, 0), 0), (pal[1], (-2, -3), 3), (pal[2], (-5, -8), 9)):
        for bx, by, r in blobs:
            rr = r - shrink
            if rr > 3:
                pygame.draw.circle(s, col, (int(cx + bx + off[0]), int(cy + by + off[1])), rr)
    return s


CAR_W, CAR_H = 56, 30


def make_car(body, dark, light, tail=(235, 40, 40)):
    """Carro visto de tras (56x30)."""
    s = pygame.Surface((CAR_W, CAR_H), pygame.SRCALPHA)
    pygame.draw.rect(s, (18, 18, 26), (1, 19, 10, 11))
    pygame.draw.rect(s, (18, 18, 26), (45, 19, 10, 11))
    pygame.draw.polygon(s, body, [(7, 5), (49, 5), (55, 13), (55, 25), (1, 25), (1, 13)])
    pygame.draw.polygon(s, light, [(7, 5), (49, 5), (52, 9), (4, 9)])
    pygame.draw.polygon(s, (40, 28, 64), [(11, 7), (45, 7), (49, 13), (7, 13)])
    pygame.draw.line(s, (110, 100, 150), (12, 8), (44, 8))
    pygame.draw.rect(s, dark, (1, 20, 54, 5))
    for x in (5, 43):
        pygame.draw.rect(s, tail, (x, 15, 9, 5))
        pygame.draw.rect(s, (255, 150, 120), (x + 1, 16, 3, 2))
    pygame.draw.rect(s, (235, 235, 225), (23, 17, 10, 4))
    pygame.draw.rect(s, (22, 18, 30), (3, 25, 50, 4))
    return s


# cores dos carros de trafego: (corpo, escuro, claro)
TRAFFIC_COLORS = [
    ((40, 70, 190), (25, 40, 120), (90, 130, 230)),
    ((150, 155, 165), (90, 95, 110), (210, 215, 225)),
    ((200, 200, 70), (140, 130, 40), (250, 245, 130)),
    ((120, 40, 140), (70, 25, 90), (180, 90, 200)),
]

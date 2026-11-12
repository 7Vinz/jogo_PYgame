"""Carros de trafego (IA simples: andam em linha reta numa faixa)."""
from .config import LANES, TRAFFIC_COUNT
from .track import L


def new_traffic(rng, sprite_count):
    """Retorna lista de dicts: z (posicao), x (faixa), v (velocidade), sprite (indice)."""
    return [{
        'z': 25 + i * (L - 30) / TRAFFIC_COUNT + rng.uniform(0, 10),
        'x': rng.choice(LANES),
        'v': rng.uniform(9, 24),
        'sprite': rng.randrange(sprite_count),
    } for i in range(TRAFFIC_COUNT)]


def update_traffic(cars, dt):
    for c in cars:
        c['z'] = (c['z'] + c['v'] * dt) % L

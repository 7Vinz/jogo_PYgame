"""Definicao do traçado: lista de (comprimento, curvatura). Total deve ser multiplo de 3."""

SEGMENTS = [(80, 0), (60, 0.8), (40, 0), (70, -1.1), (50, 0), (60, 1.4),
            (40, 0), (80, -0.7), (60, 0), (50, 1.0), (30, 0), (100, -1.3)]


def _build_curve():
    curve = []
    for n, c in SEGMENTS:
        for i in range(n):
            t = i / n
            e = min(1.0, t / 0.25, (1 - t) / 0.25)   # entrada/saida suaves
            e = e * e * (3 - 2 * e)
            curve.append(c * e)
    return curve


CURVE = _build_curve()
L = len(CURVE)          # comprimento total do circuito (loop)


def curve_at(z):
    return CURVE[int(z) % L]

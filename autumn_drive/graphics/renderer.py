"""Renderizacao pseudo-3D: pista por linha de varredura + sprites (arvores/carros)."""
import pygame

from game.config import (W, H, HORIZON, K, RW, CK, ROAD, GRASS, RUMBLE, LANE_LINE)
from game.track import L, curve_at
from game.game import PLAY
from .sprites import TREE_W, TREE_H, CAR_W, CAR_H
from .hud import draw_hud, draw_overlay

MAX_CACHE = 150


class Renderer:
    def __init__(self, assets):
        self.a = assets
        self.cache = {}          # sprites ja redimensionados

    # -------------------------------------------------------------- cena
    def draw(self, surf, g):
        self._draw_world(surf, g.pos, g.px, g.cars)
        if g.state != "title":
            self._draw_player(surf, g)
            draw_hud(surf, self.a, g)
        draw_overlay(surf, self.a, g)

    def _draw_player(self, surf, g):
        if g.inv > 0 and int(g.t * 12) % 2 == 0:      # pisca apos batida
            return
        spr = self.a.player_sprite
        x = W // 2 - spr.get_width() // 2 + g.steer_vis * 2
        surf.blit(spr, (x, H - spr.get_height() - 3))

    # ------------------------------------------------------------- mundo
    def _draw_world(self, surf, pos, px, cars):
        surf.blit(self.a.sky, (0, 0))
        center = self._draw_road(surf, pos, px)
        self._draw_sprites(surf, pos, px, cars, center)

    def _draw_road(self, surf, pos, px):
        """Desenha a pista de tras pra frente. Retorna o centro X de cada linha."""
        center = [W / 2] * (H + 1)
        cum = dxv = pz = 0.0
        for y in range(H - 1, HORIZON, -1):             # de perto (baixo) ate longe
            d = y - HORIZON
            z = K / d
            dz = z - pz
            pz = z
            wz = pos + z
            dxv += curve_at(wz) * dz                    # curva acumulada (efeito de dobra)
            cum += dxv * dz * CK
            hw = d * RW                                 # meia largura da pista nesta linha
            cx = W / 2 - px * hw + cum
            center[y] = cx

            band = int(wz / 3) & 1
            x0, x1 = int(cx - hw), int(cx + hw)
            rw = max(1, int(hw * 0.05))
            surf.fill(GRASS[int(wz / 6) & 1], (0, y, W, 1))
            surf.fill(RUMBLE[band], (x0 - rw, y, rw, 1))
            surf.fill(RUMBLE[band], (x1, y, rw, 1))
            surf.fill(ROAD[band], (x0, y, x1 - x0, 1))
            if int(wz / 1.5) & 1 == 0:                  # tracejado das faixas
                lw = max(1, int(hw * 0.022))
                for k in (-0.5, 0.0, 0.5):
                    surf.fill(LANE_LINE, (int(cx + k * hw) - lw // 2, y, lw, 1))
        return center

    def _draw_sprites(self, surf, pos, px, cars, center):
        a = self.a
        items = []                                      # (dz, tipo, sprite, x, afastamento)
        for tz, side, var, off in a.trees:
            dz = (tz - pos) % L
            if 0.7 < dz < K * 0.99:
                items.append((dz, 0, a.tree_sprites[var], side, off, var))
        for c in cars:
            dz = (c['z'] - pos) % L
            if 0.62 < dz < K * 0.99:
                items.append((dz, 1, a.car_sprites[c['sprite']], c['x'], 0, c['sprite']))
        items.sort(key=lambda i: -i[0])                 # mais longe primeiro

        if len(self.cache) > MAX_CACHE:
            self.cache.clear()

        for dz, kind, base, b, off, var in items:
            d = K / dz
            y = int(HORIZON + d)
            hw = d * RW
            cx = center[y] if y < H else W / 2 - px * hw
            if kind == 0:                               # arvore
                w = max(2, (int(TREE_W * d / 40) // 4) * 4)
                h = int(w * TREE_H / TREE_W)
                sx = cx + b * hw * (1.3 + off)
                if sx + w / 2 < 0 or sx - w / 2 > W:
                    continue
            else:                                       # carro
                w = int(0.46 * hw)
                if w < 3:
                    continue
                h = max(1, int(w * CAR_H / CAR_W))
                sx = cx + b * hw
            key = (kind, var, w)
            spr = self.cache.get(key)
            if spr is None:
                spr = pygame.transform.scale(base, (w, h))
                self.cache[key] = spr
            surf.blit(spr, (int(sx - w / 2), y - h))

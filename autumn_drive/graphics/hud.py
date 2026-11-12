"""Textos, HUD e telas de titulo / fim de jogo."""
from game.config import W
from game.game import TITLE, PLAY, OVER


def draw_text(surf, font, msg, x, y, color=(255, 255, 255), center=False):
    img = font.render(msg, False, color)
    shadow = font.render(msg, False, (25, 10, 35))
    r = img.get_rect()
    if center:
        r.midtop = (x, y)
    else:
        r.topleft = (x, y)
    surf.blit(shadow, r.move(1, 1))
    surf.blit(img, r)


def draw_hud(surf, assets, g):
    f = assets.font
    draw_text(surf, f, "TEMPO", 8, 4, (255, 230, 120))
    draw_text(surf, f, "%02d" % int(g.time), 8, 16)
    draw_text(surf, f, "PONTOS", W // 2, 4, (255, 230, 120), True)
    draw_text(surf, f, "%07d" % int(g.score), W // 2, 16, center=True)
    draw_text(surf, f, "%03d km/h" % int(g.speed * 6), W - 68, 4)
    draw_text(surf, f, "%d m" % int(g.dist * 10), W - 68, 16, (200, 240, 255))
    if g.msg_t > 0:
        draw_text(surf, assets.big, "CHECKPOINT +20s", W // 2, 60, (255, 240, 100), True)


def draw_overlay(surf, assets, g):
    f, big = assets.font, assets.big
    blink = int(g.t * 2) % 2 == 0
    if g.state == TITLE:
        draw_text(surf, big, "AUTUMN DRIVE", W // 2, 40, (255, 240, 120), True)
        if blink:
            draw_text(surf, f, "ENTER / ESPACO / TOQUE para comecar", W // 2, 150, center=True)
        draw_text(surf, f, "Setas ou WASD para dirigir", W // 2, 170, (200, 240, 255), True)
    elif g.state == OVER:
        draw_text(surf, big, "FIM DE JOGO", W // 2, 60, (255, 240, 120), True)
        draw_text(surf, f, "Pontos: %d" % int(g.score), W // 2, 100, center=True)
        if g.over_t > 1.0 and blink:
            draw_text(surf, f, "ENTER para jogar de novo", W // 2, 125, center=True)

"""
AUTUMN DRIVE - corrida pseudo-3D estilo OutRun (Pygame + Pygbag)

Local:    python main.py
Browser:  pygbag autumn_drive   ->  http://localhost:8000
Build:    pygbag --build autumn_drive

Estrutura:
  main.py            ponto de entrada (loop + entrada do usuario)
  game/              logica: config, track, traffic, game (estados/fisica)
  graphics/          visual: sprites, sky, assets, renderer, hud
"""
import asyncio
import random
import pygame

from game.config import W, H, SCALE, FPS
from game.game import Game, PLAY
from graphics.assets import Assets
from graphics.renderer import Renderer


async def main():
    pygame.init()
    screen = pygame.display.set_mode((W * SCALE, H * SCALE))
    pygame.display.set_caption("Autumn Drive")
    surf = pygame.Surface((W, H))           # superficie interna (pixel art)
    clock = pygame.time.Clock()

    assets = Assets()
    renderer = Renderer(assets)
    game = Game(len(assets.car_sprites))

    while True:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)

        start = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return
            if e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_SPACE):
                start = True
            if e.type == pygame.MOUSEBUTTONDOWN and game.state != PLAY:
                start = True

        touch_x = 0
        if game.state == PLAY and pygame.mouse.get_pressed()[0]:
            touch_x = max(0.001, pygame.mouse.get_pos()[0] / (W * SCALE))

        game.update(dt, start, pygame.key.get_pressed(), touch_x)
        renderer.draw(surf, game)

        ox = oy = 0
        if game.shake > 0:                  # tremor ao bater
            ox, oy = random.randint(-2, 2) * SCALE, random.randint(-2, 2) * SCALE
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(surf, (W * SCALE, H * SCALE)), (ox, oy))
        pygame.display.flip()
        await asyncio.sleep(0)              # obrigatorio para o Pygbag


asyncio.run(main())

#!/usr/bin/env python3
"""
Autumn Cat Café – Main entry point
Run with:  python main.py
"""

import sys, os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from src.game  import Game
import src.audio as audio


def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # Optional: set a nice icon using procedural cat face
    icon = pygame.Surface((32, 32), pygame.SRCALPHA)
    pygame.draw.circle(icon, (22, 14, 8), (16, 18), 12)
    pygame.draw.polygon(icon, (22, 14, 8), [(6, 10), (12, 2), (16, 10)])
    pygame.draw.polygon(icon, (22, 14, 8), [(26, 10), (20, 2), (16, 10)])
    pygame.draw.circle(icon, (235, 230, 218), (12, 18), 4)
    pygame.draw.circle(icon, (235, 230, 218), (20, 18), 4)
    pygame.display.set_icon(icon)

    # Init audio (silently fails if numpy missing)
    audio.init_audio()

    clock = pygame.time.Clock()
    game  = Game(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        dt = min(dt, 0.05)   # cap at 50 ms to avoid spiral of death

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            game.handle_event(event)

        game.update(dt)
        game.draw()
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

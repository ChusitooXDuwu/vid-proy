import pygame


class CColorCycle:
    def __init__(self, colors: list[pygame.Color], interval: float) -> None:
        self.colors = colors
        self.interval = interval
        self.timer = 0.0
        self.index = 0
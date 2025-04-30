from enum import Enum
import pygame


class CRotation:
    def __init__(self, directions: list[pygame.Vector2], delay: float) -> None:
        self.directions = directions
        self.index = 0
        self.cooldown = 0.0
        self.delay = delay


class RotationEnum(Enum):
    LEFT = -1
    RIGHT = 1
    NONE = 0

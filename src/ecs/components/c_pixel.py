import pygame


class CPixel:
    """
    Represents a pixel component in the ECS (Entity Component System) architecture.

    Attributes:
        size (int): The size of the pixel.
        color (pygame.Color): The color of the pixel, represented as a pygame.Color object.

    Args:
        size (int): The size of the pixel to initialize.
        color (pygame.Color): The color of the pixel to initialize.
    """
    def __init__(self, size: int, color: pygame.Color):
        self.size = size
        self.color = color
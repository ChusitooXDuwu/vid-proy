import pygame


class CTransform:
    """
    CTransform is a component class that represents the position of an entity in a 2D space.

    Attributes:
        pos (pygame.Vector2): The position of the entity represented as a 2D vector.
    """
    def __init__(self, pos:pygame.Vector2) -> None:
        self.pos = pos
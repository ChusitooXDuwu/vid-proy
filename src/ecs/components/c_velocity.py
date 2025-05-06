import pygame


class CVelocity:
    """
    CVelocity is a component class that represents the velocity of an entity in a 2D space.

    Attributes:
        vel (pygame.Vector2): A vector representing the velocity of the entity, 
                              with both magnitude and direction.
    """
    def __init__(self, vel: pygame.Vector2) -> None:
        self.vel = vel

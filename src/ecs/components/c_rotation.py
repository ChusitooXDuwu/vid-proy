from enum import Enum
import pygame


class CRotation:
    """
    CRotation is a component that manages directional rotation with a delay between changes.

    Attributes:
        directions (list[pygame.Vector2]): A list of directional vectors representing possible rotations.
        index (int): The current index in the directions list.
        cooldown (float): The current cooldown time before the next rotation can occur.
        delay (float): The delay time (in seconds) between consecutive rotations.
        current_vertical (RotationEnum): Current vertical direction (UP/DOWN/NONE)
        current_horizontal (RotationEnum): Current horizontal direction (LEFT/RIGHT/NONE)

    Methods:
        __init__(directions: list[pygame.Vector2], delay: float) -> None:
            Initializes the CRotation component with a list of directions and a delay.
    """

    def __init__(self, directions: list[pygame.Vector2], delay: float) -> None:
        self.directions = directions
        self.index = 0
        self.cooldown = 0.0
        self.delay = delay
        self.current_vertical = RotationEnum.NONE
        self.current_horizontal = RotationEnum.NONE


class RotationEnum(Enum):
    UP = 2
    DOWN = -2
    LEFT = -1
    RIGHT = 1
    NONE = 0

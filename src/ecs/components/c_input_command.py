from enum import Enum
import pygame


class CInputCommand:
    """
    Component to store input commands for the ECS (Entity Component System).
    This component is used to manage and process input commands in the game.
    """

    def __init__(self, name: str, key: int):
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        self.mouse_pos = pygame.Vector2(0, 0)
        
class CommandPhase(Enum):
    NA = 0 # Not Applicable
    START = 1 # Start of the command (pressed)
    END = 2 # End of the command (released)
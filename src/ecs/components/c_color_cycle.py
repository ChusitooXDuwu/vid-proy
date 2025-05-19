import pygame


class CColorCycle:
    """
    CColorCycle is a component that handles cycling through a list of colors over time.

    Attributes:
        colors (list[pygame.Color]): A list of pygame.Color objects to cycle through.
        interval (float): The time interval (in seconds) between color changes.
        timer (float): A timer to track the elapsed time since the last color change.
        index (int): The current index in the colors list.

    Methods:
        __init__(colors: list[pygame.Color], interval: float):
            Initializes the CColorCycle component with a list of colors and a time interval.
    """

    def __init__(self, colors: list[pygame.Color], interval: float) -> None:
        self.colors = colors
        self.interval = interval
        self.timer = 0.0
        self.index = 0

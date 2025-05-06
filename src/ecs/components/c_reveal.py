class CReveal:
    """
    A component class that represents the reveal state of an entity with a delay.

    Attributes:
        delay (int): The delay time (in arbitrary units) before the entity is revealed.
        revealed (bool): A flag indicating whether the entity is currently revealed. Defaults to False.
    """
    def __init__(self, delay: int, revealed: bool = False):
        self.delay = delay
        self.revealed = revealed
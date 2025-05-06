from enum import Enum


class CPlayerState:
    """
    CPlayerState is a component class that represents the state of a player in the game.
    Attributes:
        state (PlayerState): The current state of the player. It is initialized to PlayerState.MOVE0.
    """

    def __init__(self) -> None:
        self.state = PlayerState.MOVE0


class PlayerState(Enum):
    MOVE0 = 0
    MOVE1 = 1
    MOVE2 = 2
    MOVE3 = 3
    MOVE4 = 4
    MOVE5 = 5
    MOVE6 = 6
    MOVE7 = 7
    MOVE8 = 8
    MOVE9 = 9
    MOVE10 = 10
    MOVE11 = 11
    MOVE12 = 12
    MOVE13 = 13
    MOVE14 = 14
    MOVE15 = 15
    MOVE16 = 16
    MOVE17 = 17
    MOVE18 = 18
    MOVE19 = 19
    MOVE20 = 20
    MOVE21 = 21
    MOVE22 = 22
    MOVE23 = 23
    MOVE24 = 24
    MOVE25 = 25
    MOVE26 = 26
    MOVE27 = 27
    MOVE28 = 28
    MOVE29 = 29
    MOVE30 = 30
    MOVE31 = 31

from typing import List

from src.engine.service_locator import ServiceLocator


class CAnimation:
    """
    A class to manage animations for an entity.
    Attributes:
        number_frames (int): The total number of frames available for animations.
        animations_list (List[AnimationData]): A list of AnimationData objects representing the animations.
        current_animation (int): The index of the currently active animation in the animations_list.
        current_animation_time (int): The elapsed time for the current animation.
        current_frame (int): The current frame being displayed in the active animation.
    Methods:
        __init__(animations: dict):
            Initializes the CAnimation object with animation data.
            Parses the input dictionary to create a list of AnimationData objects.
    """
    def __init__(self, animations: dict) -> None:
        self.number_frames = animations["number_frames"]
        self.animations_list: List[AnimationData] = []
        for anim in animations["list"]:
            anim_data = AnimationData(
                anim["name"],
                anim["start"],
                anim["end"],
                anim["framerate"],
            )
            self.animations_list.append(anim_data)

        self.current_animation = 0
        self.current_animation_time = 0
        self.current_frame = self.animations_list[self.current_animation].start


class AnimationData:
    def __init__(self, name: str, start: int, end: int, framerate: float) -> None:
        self.name = name
        self.start = start
        self.end = end
        self.framerate = 1.0 / framerate

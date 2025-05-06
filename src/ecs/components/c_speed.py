class CSpeed:
    """
    Represents the speed component of an entity in the ECS (Entity Component System).

    Attributes:
        speed (float): The speed value associated with the entity.
        
    Args:
        speed (float): The initial speed value to assign to the component.
    """
    def __init__(self, speed: float) -> None:
        self.speed = speed

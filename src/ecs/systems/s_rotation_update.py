import esper
from src.ecs.components.c_rotation import CRotation, RotationEnum


def system_rotation_update(
    world: esper.World, delta_time: float, pending_direction: RotationEnum
) -> None:
    c_r: CRotation
    for _, c_r in world.get_component(CRotation):
        c_r.cooldown -= delta_time

        if pending_direction != RotationEnum.NONE and c_r.cooldown <= 0:
            c_r.index = (c_r.index + pending_direction.value) % len(c_r.directions)
            c_r.cooldown = c_r.delay
            pending_direction = RotationEnum.NONE

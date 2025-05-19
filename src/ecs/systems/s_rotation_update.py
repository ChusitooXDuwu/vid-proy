import esper
import pygame
from src.ecs.components.c_rotation import CRotation, RotationEnum


def system_rotation_update(world: esper.World, delta_time: float) -> None:
    c_r: CRotation
    for _, c_r in world.get_component(CRotation):
        c_r.cooldown -= delta_time

        if c_r.cooldown <= 0:
            target_direction = pygame.Vector2(0, 0)

            if c_r.current_horizontal == RotationEnum.LEFT:
                target_direction.x = -1
            elif c_r.current_horizontal == RotationEnum.RIGHT:
                target_direction.x = 1

            if c_r.current_vertical == RotationEnum.UP:
                target_direction.y = -1
            elif c_r.current_vertical == RotationEnum.DOWN:
                target_direction.y = 1

            if target_direction.length_squared() > 0:
                target_direction = target_direction.normalize()
                closest = -2
                best_index = c_r.index

                for i, direction in enumerate(c_r.directions):
                    dot = target_direction.dot(direction)
                    if dot > closest:
                        closest = dot
                        best_index = i

                if best_index != c_r.index:
                    num_directions = len(c_r.directions)
                    current_index = c_r.index
                    clockwise_distance = (best_index - current_index) % num_directions
                    counterclockwise_distance = (
                        current_index - best_index
                    ) % num_directions

                    if clockwise_distance < counterclockwise_distance:
                        c_r.index = (current_index + 1) % num_directions
                    else:
                        c_r.index = (current_index - 1) % num_directions

                    c_r.cooldown = c_r.delay

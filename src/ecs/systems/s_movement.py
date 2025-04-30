import esper
import pygame
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_cloud import CTagCloud


def system_movement(
    world: esper.World, delta_time: float, global_velocity_direction: pygame.Vector2
) -> None:
    components = world.get_components(CTransform, CVelocity, CSpeed, CTagCloud)

    for _, (c_t, c_v, c_s, _) in components:
        dir_x = global_velocity_direction.x if c_v.vel.x != 0 else 0
        dir_y = global_velocity_direction.y if c_v.vel.y != 0 else 0

        direction = pygame.Vector2(dir_x, dir_y)
        if direction.length_squared() != 0:
            direction = direction.normalize()

        effective_vel = direction * c_s.speed

        c_t.pos += effective_vel * delta_time

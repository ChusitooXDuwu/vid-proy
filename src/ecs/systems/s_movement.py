import esper
import pygame
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud


def system_movement(
    world: esper.World,
    delta_time: float,
    player_entity: int,
    boss_enemy_cfg: dict,
) -> None:
    components = world.get_components(CTransform, CVelocity, CSpeed, CTagCloud)
    enemy_components = world.get_components(
        CTransform, CVelocity, CSpeed, CTagBossEnemy
    )
    c_v: CVelocity
    c_t: CTransform
    c_s: CSpeed
    c_r = world.component_for_entity(player_entity, CRotation)
    global_velocity_direction = c_r.directions[c_r.index]
    for _, (c_t, c_v, c_s, _) in components:
        dir_x = global_velocity_direction.x if c_v.vel.x != 0 else 0
        dir_y = global_velocity_direction.y if c_v.vel.y != 0 else 0

        direction = pygame.Vector2(dir_x, dir_y)
        if direction.length_squared() != 0:
            direction = direction.normalize()

        effective_vel = direction * c_s.speed

        c_t.pos += effective_vel * delta_time

    for _, (c_t, c_v, c_s, _) in enemy_components:
        dir_x = global_velocity_direction.x
        dir_y = global_velocity_direction.y

        direction = pygame.Vector2(dir_x, dir_y)
        if direction.length_squared() != 0:
            direction = direction.normalize()

        effective_vel = pygame.Vector2(0, 0)
        effective_vel.x = direction.x * c_s.speed * 0.5
        effective_vel.y = direction.y * c_s.speed
        enemy_vel = pygame.Vector2(boss_enemy_cfg["velocity"]["x"], 0)

        c_t.pos += (effective_vel + enemy_vel) * delta_time

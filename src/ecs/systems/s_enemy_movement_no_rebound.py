import math
import random

import esper
import pygame

from src.create.prefab_creator import spawn_enemy_random
from src.ecs.components.c_path_change import CPathChange
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_enemy_movement_no_rebound(
    world: esper.World,
    screen_rect: pygame.Rect,
    enemies_info: dict,
    total_spawned: int,
    delta_time: float,
):
    enemies = []

    for entity, (c_t, c_v, c_s, c_a, _, c_pc) in world.get_components(
        CTransform, CVelocity, CSurface, CAnimation, CTagEnemy, CPathChange
    ):
        c_t.pos += c_v.velocity * delta_time

        if c_pc.changes_done < c_pc.max_changes:
            c_pc.time_until_next -= delta_time
            if c_pc.time_until_next <= 0:
                angle = random.uniform(0, 360)
                speed = c_v.velocity.length()  # mantener misma velocidad
                c_v.velocity = pygame.Vector2(speed, 0).rotate(angle)
                c_pc.changes_done += 1
                c_pc.time_until_next = random.uniform(1.5, 3.0)

        if c_v.velocity.length_squared() > 0:
            direction = c_v.velocity.normalize()

            angle = (math.degrees(math.atan2(direction.y, -direction.x)) + 90) % 360

            frame_index = int(angle // 22.5) % 16
            c_a.current_frame = frame_index

            frame_width = 16
            frame_height = 16
            c_s.area = pygame.Rect(
                frame_index * frame_width, 0, frame_width, frame_height
            )

        enemy_rect = pygame.Rect(c_t.pos.x, c_t.pos.y, c_s.area.width, c_s.area.height)
        if not screen_rect.colliderect(enemy_rect):
            world.delete_entity(entity)
        else:
            enemies.append(entity)

    # Si hay menos de 6 y no hemos llegado a total de enemigos, crear más enemigos
    while len(enemies) < 6 and total_spawned < enemies_info["total_minion_enemies"]:
        spawn_enemy_random(world, screen_rect, enemies_info)
        total_spawned += 1
        enemies.append(None)

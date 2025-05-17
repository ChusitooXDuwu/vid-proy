import pygame
import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy


def system_boss_enemy_movement(
    world: esper.World, screen_rect: pygame.Rect, boss_enemy_cfg: dict
):
    boss_enemies = world.get_components(CTagBossEnemy, CVelocity, CTransform)
    for _, (_, c_velocity, c_transform) in boss_enemies:
        print(c_transform.pos.x)
        print(c_velocity.vel.x)
        # c_velocity.vel.x = (
        #     c_velocity.vel.x
        #     * pygame.Vector2(boss_enemy_cfg["velocity"]["x"], 0).normalize()
        # ).x

        # c_transform.pos.x += c_velocity.vel.x

        # if c_transform.pos.x < screen_rect.left:
        #     c_transform.pos.x = screen_rect.right

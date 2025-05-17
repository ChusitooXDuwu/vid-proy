import pygame
import esper
from src.create.prefab_creator import create_enemy
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy


def system_boss_enemy_spawner(
    world: esper.World,
    screen_rect: pygame.Rect,
    boss_enemy_cfg: dict,
    enemies_killed: int,
    spawn_enemy_threshold: int,
):
    num_boss_enemies = boss_enemy_cfg["num_boss_enemies"]
    boss_enemies = world.get_component(CTagBossEnemy)
    if len(boss_enemies) >= num_boss_enemies:
        return

    if enemies_killed >= spawn_enemy_threshold:
        pos = pygame.Vector2(
            boss_enemy_cfg["spawn_position"]["x"],
            screen_rect.height / 2,
        )
        create_enemy(world, pos, boss_enemy_cfg, boss_enemy=True)

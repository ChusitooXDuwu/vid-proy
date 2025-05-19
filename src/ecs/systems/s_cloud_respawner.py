import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy
from src.ecs.components.tags.c_tag_cloud import CTagCloud


def system_respawner(world: esper.World, screen: pygame.rect.Rect) -> None:
    components = world.get_components(CTransform, CSurface, CTagCloud)
    boss_enemy_components = world.get_components(CTransform, CSurface, CTagBossEnemy)

    for _, (c_t, c_s, _) in components:
        entity_hitbox = CSurface.get_area_relative(c_s.area, c_t.pos)
        width = entity_hitbox.width
        height = entity_hitbox.height

        # Wrap horizontally
        if entity_hitbox.right < 0:
            c_t.pos.x = screen.right
        elif entity_hitbox.left > screen.right:
            c_t.pos.x = -width / 2

        # Wrap vertically
        if entity_hitbox.bottom < 0:
            c_t.pos.y = screen.bottom
        elif entity_hitbox.top > screen.bottom:
            c_t.pos.y = -height / 2

    for _, (c_t, c_s, _) in boss_enemy_components:
        entity_hitbox = CSurface.get_area_relative(c_s.area, c_t.pos)
        width = entity_hitbox.width
        height = entity_hitbox.height

        # Wrap horizontally
        if entity_hitbox.right < 0:
            c_t.pos.x = screen.right
        elif entity_hitbox.left > screen.right:
            c_t.pos.x = -width / 2

        # Wrap vertically
        if entity_hitbox.bottom < 0:
            c_t.pos.y = screen.bottom
        elif entity_hitbox.top > screen.bottom:
            c_t.pos.y = -height / 2

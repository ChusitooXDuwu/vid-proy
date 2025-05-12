
import esper
import pygame
from src.create.prefab_creator import create_explosion, create_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_bullet_enemy_collision(world: esper.World, explosion: dict):
    bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)

    for bullet_entity, (b_t, b_s, _) in bullets:
        bullet_rect = pygame.Rect(b_t.pos.x, b_t.pos.y, b_s.area.width, b_s.area.height)

        for enemy_entity, (e_t, e_s, _) in enemies:
            enemy_rect = pygame.Rect(e_t.pos.x, e_t.pos.y, e_s.area.width, e_s.area.height)

            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
                create_explosion_sprite(world, b_t.pos, explosion)
                break
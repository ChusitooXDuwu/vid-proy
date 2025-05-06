
import esper
import pygame
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_bullet_enemy(world: esper.World, explosion_cfg: dict) -> None:
    
    bullet_components = world.get_components(CSurface, CTransform, CTagBullet)
    enemy_components = world.get_components(CSurface, CTransform, CTagEnemy)
    
    entities_to_delete = set()
    
    for bullet_entity, (bullet_s, bullet_t, _) in bullet_components:
        if bullet_entity in entities_to_delete:
            continue
            
        bullet_rect = pygame.Rect(
            bullet_t.pos.x, bullet_t.pos.y, 
            bullet_s.area.width, bullet_s.area.height
        )
        
        for enemy_entity, (enemy_s, enemy_t, _) in enemy_components:
            if enemy_entity in entities_to_delete:
                continue
                
            enemy_rect = pygame.Rect(
                enemy_t.pos.x, enemy_t.pos.y, 
                enemy_s.area.width, enemy_s.area.height
            )
            
            if bullet_rect.colliderect(enemy_rect):
                entities_to_delete.add(bullet_entity)
                entities_to_delete.add(enemy_entity)
                
                
                create_explosion(world, enemy_t.pos, explosion_cfg)
                break
    
    for entity in entities_to_delete:
        world.delete_entity(entity)
import pygame
import esper
from src.create.prefab_creator import create_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_points import CPlayerPoints
from src.engine.service_locator import ServiceLocator

def system_collision_enemy_player(world: esper.World, explosion: dict, lifes: list, player_entity: int) -> int:
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)
    boss_enemy = world.get_components(CTransform, CSurface, CTagBossEnemy)
    
    p_t = world.component_for_entity(player_entity, CTransform)
    p_s = world.component_for_entity(player_entity, CSurface)
    
    
    
    game_over = False
    player_killed = False

    for enemy_entity, (e_t, e_s, _) in enemies:
        enemy_rect = pygame.Rect(
            e_t.pos.x, e_t.pos.y, e_s.area.width, e_s.area.height
        )

        player_rect = pygame.Rect(
            p_t.pos.x, p_t.pos.y, p_s.area.width, p_s.area.height
        )

        if enemy_rect.colliderect(player_rect):
            create_explosion_sprite(world, e_t.pos, explosion["enemy"])
            create_explosion_sprite(world, p_t.pos, explosion["player"])
            world.delete_entity(enemy_entity)
            # world.delete_entity(player_entity)
            p_s.visible = False
            player_killed = True
            ()
            if len(lifes) > 0:
                life = lifes.pop()
                world.delete_entity(life)
            
            game_over = len(lifes) < 1
            break
    
    if game_over or player_killed:
        return game_over, lifes, player_killed
    
    for boss_enemy_entity, (b_t, b_s, _) in boss_enemy:
        boss_enemy_rect = pygame.Rect(
            b_t.pos.x, b_t.pos.y, b_s.area.width, b_s.area.height
        )
        
        player_rect = pygame.Rect(
            p_t.pos.x, p_t.pos.y, p_s.area.width, p_s.area.height
        )

        if boss_enemy_rect.colliderect(player_rect):
            create_explosion_sprite(world, p_t.pos, explosion["boss_enemy"])
            create_explosion_sprite(world, b_t.pos, explosion["player"])
            # world.delete_entity(player_entity)
            p_s.visible = False
            world.delete_entity(boss_enemy_entity)
            player_killed = True
            if len(lifes) > 0:
                life = lifes.pop()
                world.delete_entity(life)
            game_over = len(lifes) < 1
            break
    
    return game_over, lifes, player_killed
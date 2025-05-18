import pygame
import esper
from src.create.prefab_creator import create_explosion_sprite
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_boss_enemy import CTagBossEnemy
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player_points import CPlayerPoints
from src.engine.service_locator import ServiceLocator


def system_bullet_enemy_collision(world: esper.World, explosion: dict) -> int:
    bullets = world.get_components(CTransform, CSurface, CTagBullet)
    enemies = world.get_components(CTransform, CSurface, CTagEnemy)
    boss_enemy = world.get_components(CTransform, CSurface, CTagBossEnemy)
    game_over = False
    enemies_killed = 0
    for bullet_entity, (b_t, b_s, _) in bullets:
        bullet_rect = pygame.Rect(b_t.pos.x, b_t.pos.y, b_s.area.width, b_s.area.height)

        for enemy_entity, (e_t, e_s, enemy_tag) in enemies:
            enemy_rect = pygame.Rect(
                e_t.pos.x, e_t.pos.y, e_s.area.width, e_s.area.height
            )

            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)
                create_explosion_sprite(world, b_t.pos, explosion["enemy"])
                enemies_killed += 1

                player_points = world.get_components(CPlayerPoints, CSurface)
                for _, (c_player_points, c_surface) in player_points:
                    font = ServiceLocator.fonts_service.get(
                        "assets/fnt/PressStart2P.ttf", 8
                    )
                    ServiceLocator.game_state.points += enemy_tag.points
                    text = str(ServiceLocator.game_state.points)
                    c_surface.surf = font.render(text, True, (255, 255, 255))
                    c_surface.area = c_surface.surf.get_rect()
                break

        for boss_enemy_entity, (b_t, b_s, b_tag) in boss_enemy:
            boss_enemy_rect = pygame.Rect(
                b_t.pos.x, b_t.pos.y, b_s.area.width, b_s.area.height
            )
            if bullet_rect.colliderect(boss_enemy_rect):
                world.delete_entity(bullet_entity)
                b_tag.health -= 1
                if b_tag.health <= 0:
                    world.delete_entity(boss_enemy_entity)
                    create_explosion_sprite(world, b_t.pos, explosion["boss_enemy"])
                    enemies_killed += 1
                    player_points = world.get_components(CPlayerPoints, CSurface)
                    game_over = True
                break

    return enemies_killed, game_over

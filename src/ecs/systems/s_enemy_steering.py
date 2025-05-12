import math
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy



def system_enemy_steering(world, player_entity):
    player_pos = world.component_for_entity(player_entity, CTransform).pos

    for entity, (c_t, c_v, c_s, c_a, _) in world.get_components(CTransform, CVelocity, CSurface, CAnimation, CTagEnemy):
        direction = (player_pos - c_t.pos).normalize()
        desired_velocity = direction * 100
        steering = desired_velocity - c_v.vel
        c_v.vel += steering * 0.05
        c_t.pos += c_v.vel * (1 / 60)

        # Elegir frame según dirección
        angle = math.degrees(math.atan2(-direction.y, direction.x)) % 360
        frame_index = int(angle // 22.5) % 16
        c_a.current_frame = frame_index

        # Actualizar el área del sprite mostrado según el frame
        frame_width = 16
        frame_height = 16
        c_s.area = pygame.Rect(frame_index * frame_width, 0, frame_width, frame_height)

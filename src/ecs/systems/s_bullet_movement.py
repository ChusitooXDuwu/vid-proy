
import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_movement(world: esper.World, delta_time: float) -> None:
    
    components = world.get_components(CTransform, CVelocity, CTagBullet)
    
    for _, (c_t, c_v, _) in components:
        
        c_t.pos.x += c_v.vel.x * delta_time
        c_t.pos.y += c_v.vel.y * delta_time
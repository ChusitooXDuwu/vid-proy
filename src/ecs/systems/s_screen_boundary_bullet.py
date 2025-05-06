import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_screen_boundary_bullet(world: esper.World, screen_rect: pygame.Rect) -> None:
  
    components = world.get_components(CSurface, CTransform, CTagBullet)
    
    for entity, (c_s, c_t, _) in components:
        
        bullet_rect = pygame.Rect(
            c_t.pos.x, c_t.pos.y, 
            c_s.area.width, c_s.area.height
        )
        
       
        if (bullet_rect.right < 0 or 
            bullet_rect.left > screen_rect.width or 
            bullet_rect.bottom < 0 or 
            bullet_rect.top > screen_rect.height):
            world.delete_entity(entity)
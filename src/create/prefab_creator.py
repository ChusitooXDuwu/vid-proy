import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

def create_text(world:esper.World, text:str, font:pygame.font.Font, color:pygame.Color, pos:pygame.Vector2, center: bool = False) -> int:
    if center:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        pos = pygame.Vector2(pos.x - text_rect.width / 2, pos.y - text_rect.height / 2)
    
    text_entity = world.create_entity()
    world.add_component(text_entity, CTransform(pos))
    world.add_component(text_entity, CSurface.from_text(text, font, color))
    return text_entity

def create_text_interface(world:esper.World, interface_info:dict, type:str):
    font = ServiceLocator.texts_service.get(interface_info["font"], 
                                            interface_info[type]["size"])
    
    color = pygame.Color(interface_info[type]["color"]["r"],
                         interface_info[type]["color"]["g"],
                         interface_info[type]["color"]["b"])
    
    pos = pygame.Vector2(interface_info[type]["pos"]["x"], interface_info[type]["pos"]["y"])
    
    center = interface_info[type].get("center", False)
    
    return create_text(world, interface_info[type]["text"], font, color, pos, center)
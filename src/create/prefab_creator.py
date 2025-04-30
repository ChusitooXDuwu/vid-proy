import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
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

def create_sprite(ecs_world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2, surface: pygame.Surface, center: bool = False) -> int:
    if center:
        sprite_rect = surface.get_rect()
        pos = pygame.Vector2(pos.x - sprite_rect.width / 2, pos.y - sprite_rect.height / 2)
    
    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, 
                            CTransform(pos))
    ecs_world.add_component(sprite_entity, 
                            CVelocity(vel))
    ecs_world.add_component(sprite_entity, 
                            CSurface.from_surface(surface))
    return sprite_entity

def create_text_interface(world:esper.World, interface_info:dict, type:str) -> int:
    font = ServiceLocator.fonts_service.get(interface_info["font"], 
                                            interface_info[type]["size"])
    
    color = pygame.Color(interface_info[type]["color"]["r"],
                         interface_info[type]["color"]["g"],
                         interface_info[type]["color"]["b"])
    
    pos = pygame.Vector2(interface_info[type]["pos"]["x"], interface_info[type]["pos"]["y"])
    
    center = interface_info[type].get("center", False)
    
    return create_text(world, interface_info[type]["text"], font, color, pos, center)

def create_image(world:esper.World, interface_info:dict, type:str) -> int:
    surface = ServiceLocator.images_service.get(interface_info[type]["image"])
    pos = pygame.Vector2(interface_info[type]["pos"]["x"], interface_info[type]["pos"]["y"])
    vel = pygame.Vector2(0,0)
    center = interface_info[type].get("center", False)
    return create_sprite(world, pos, vel, surface, center)


def create_input_player(ecs_world:esper.World) :
    input_next = ecs_world.create_entity()
    
    
    ecs_world.add_component(input_next, CInputCommand("NEXT_SCREEN", pygame.K_RETURN))
    
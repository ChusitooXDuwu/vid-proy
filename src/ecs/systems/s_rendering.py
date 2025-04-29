import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(world:esper.World, screen:pygame.Surface) -> None:
    components = world.get_components(CTransform, CSurface)

    c_transform: CTransform
    c_surface: CSurface

    for _, (c_transform, c_surface) in components:
        screen.blit(c_surface.surf, c_transform.pos, area=c_surface.area)


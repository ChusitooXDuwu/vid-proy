# src/ecs/systems/s_rendering.py
import pygame
import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_render_priority import CRenderPriority
from src.ecs.components.tags.c_tag_pause_text import CTagPauseText


def system_rendering(
    world: esper.World, screen: pygame.Surface, game_paused: bool = False
) -> None:
    renderables = []

    components = world.get_components(CTransform, CSurface)
    for entity, (c_transform, c_surface) in components:

        if world.has_component(entity, CTagPauseText) and not game_paused:
            continue
        
        if not getattr(c_surface, "visible", True):
            continue

        priority = 0
        if world.has_component(entity, CRenderPriority):
            priority = world.component_for_entity(entity, CRenderPriority).priority

        renderables.append((entity, c_transform, c_surface, priority))
    renderables.sort(key=lambda x: x[3])

    for _, c_transform, c_surface, _ in renderables:
        screen.blit(c_surface.surf, c_transform.pos, area=c_surface.area)

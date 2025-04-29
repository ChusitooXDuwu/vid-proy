import pygame
import esper

from typing import Callable

from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player (ecs_world: esper.World, events: pygame.event.Event, do_action: Callable[[CInputCommand], None]):
    """
    System to handle player input events and trigger actions based on them.
    """
    
    components = ecs_world.get_component(CInputCommand)
    
    for _, c_input in components:
        if events.type == pygame.KEYDOWN and c_input.key == events.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif events.type == pygame.KEYUP and c_input.key == events.key:
            c_input.phase = CommandPhase.END
            do_action(c_input)
            
        if events.type == pygame.MOUSEBUTTONDOWN and c_input.key == events.button:
            c_input.phase = CommandPhase.START
            c_input.mouse_pos.xy = pygame.mouse.get_pos()
            do_action(c_input)
        elif events.type == pygame.MOUSEBUTTONUP and c_input.key == events.button:
            c_input.phase = CommandPhase.END
            c_input.mouse_pos.xy = pygame.mouse.get_pos()
            do_action(c_input)
            
    
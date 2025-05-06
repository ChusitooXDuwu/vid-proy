import esper

from src.ecs.components.c_reveal import CReveal


def system_reveal_animation(world: esper.World, current_tick: int):
    components = world.get_component(CReveal)

    for _, c_r in components:
        if not c_r.revealed and c_r.delay <= current_tick:
            c_r.revealed = True

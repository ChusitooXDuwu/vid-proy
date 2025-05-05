import esper

from src.ecs.components.c_color_cycle import CColorCycle
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


def system_color_cycle(world: esper.World, delta_time: float, interface: dict, text: dict) -> None:
    components = world.get_components(CColorCycle, CTransform, CSurface)

    for ent, (c_c_c, c_t, c_s) in components:
            c_c_c.timer += delta_time
            if c_c_c.timer >= c_c_c.interval:
                c_c_c.timer -= c_c_c.interval
                c_c_c.index = (c_c_c.index + 1) % len(c_c_c.colors)
                new_color = c_c_c.colors[c_c_c.index]

                font = ServiceLocator.fonts_service.get(interface["font"], text["size"])
                c_s.surf = font.render(text["text"], True, new_color)
                c_s.area = c_s.surf.get_rect()
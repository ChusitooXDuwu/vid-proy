import esper
import pygame

from src.ecs.components.c_pixel import CPixel
from src.ecs.components.c_reveal import CReveal
from src.ecs.components.c_transform import CTransform


def system_render_pixels(world: esper.World, screen: pygame.Surface, padding_top=20, padding_bottom=10):
    screen_height = screen.get_height()
    components = world.get_components(CTransform, CPixel, CReveal)

    for _, (c_t, c_p, c_r) in components:
        if c_r.revealed:
            y_position = c_t.pos.y + padding_top

            max_y = screen_height - padding_bottom - c_p.size
            if y_position > max_y:
                y_position = max_y

            rect = pygame.Rect(c_t.pos.x, y_position, c_p.size, c_p.size)
            pygame.draw.rect(screen, c_p.color, rect)
import pygame
import esper
import math

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_color_cycle import CColorCycle
from src.ecs.components.c_pixel import CPixel
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_reveal import CReveal
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_text(
    world: esper.World,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    pos: pygame.Vector2,
    center: bool = False,
) -> int:
    if center:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        pos = pygame.Vector2(pos.x - text_rect.width / 2, pos.y - text_rect.height / 2)

    text_entity = world.create_entity()
    world.add_component(text_entity, CTransform(pos))
    world.add_component(text_entity, CSurface.from_text(text, font, color))
    return text_entity


def create_sprite(
    ecs_world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
    center: bool = False,
) -> int:
    if center:
        sprite_rect = surface.get_rect()
        pos = pygame.Vector2(
            pos.x - sprite_rect.width / 2, pos.y - sprite_rect.height / 2
        )

    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity


def create_text_interface(
    world: esper.World, interface_info: dict, interface_type: str
) -> int:
    font = ServiceLocator.fonts_service.get(
        interface_info["font"], interface_info[interface_type]["size"]
    )

    color = pygame.Color(
        interface_info[interface_type]["color"]["r"],
        interface_info[interface_type]["color"]["g"],
        interface_info[interface_type]["color"]["b"],
    )

    pos = pygame.Vector2(
        interface_info[interface_type]["pos"]["x"],
        interface_info[interface_type]["pos"]["y"],
    )

    center = interface_info[interface_type].get("center", False)

    return create_text(
        world, interface_info[interface_type]["text"], font, color, pos, center
    )


def create_text_interface_with_color_cycle(
    world: esper.World, interface_info: dict, interface_type: str
) -> int:
    entity = create_text_interface(world, interface_info, interface_type)

    colors = [
        pygame.Color(255, 255, 255),
        pygame.Color(255, 0, 0),
        pygame.Color(0, 0, 255),
    ]
    world.add_component(entity, CColorCycle(colors, 0.3))

    return entity


def create_image(world: esper.World, interface_info: dict, image_type: str) -> int:
    surface = ServiceLocator.images_service.get(interface_info[image_type]["image"])
    pos = pygame.Vector2(
        interface_info[image_type]["pos"]["x"], interface_info[image_type]["pos"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    center = interface_info[image_type].get("center", False)
    return create_sprite(world, pos, vel, surface, center)


def create_ship(
    world: esper.World, player_cfg: dict, level_info: dict, player_rotations: int
) -> int:
    player_sprite = ServiceLocator.images_service.get(player_cfg["image"])
    width, height = player_sprite.get_size()
    # Need adjustment for the number of frames
    size = pygame.Vector2(width / player_cfg["animations"]["number_frames"], height)
    pos = pygame.Vector2(
        (level_info["position"]["x"] - size.x / 2),
        (level_info["position"]["y"] - size.y / 2),
    )
    vel = pygame.Vector2(0, 0)
    player_entity = create_sprite(
        world,
        pos,
        vel,
        player_sprite,
    )
    directions = [
        pygame.Vector2(
            math.cos(2 * math.pi * i / player_rotations),
            math.sin(2 * math.pi * i / player_rotations),
        )
        for i in range(player_rotations)
    ]
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_cfg["animations"]))
    world.add_component(
        player_entity,
        CRotation(directions, level_info["rotation_delay"]),
    )
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_logo(world: esper.World, logo_info: dict) -> int:
    surface = ServiceLocator.images_service.get(logo_info["image"])
    pos = pygame.Vector2(logo_info["pos"]["x"], logo_info["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    center = logo_info.get("center", False)
    return create_sprite(world, pos, vel, surface, center)


def create_clouds(
    ecs_world: esper.World, cloud_info: dict, padding_top=30, padding_bottom=10
) -> int:
    cloud_sprite = ServiceLocator.images_service.get(cloud_info["image"])
    width, height = cloud_sprite.get_size()
    size = pygame.Vector2(width / cloud_info["animations"]["number_frames"], height)

    screen_height = pygame.display.get_surface().get_height()
    min_y = padding_top
    max_y = screen_height - padding_bottom

    for cloud_pos in cloud_info["clouds"]:
        x = cloud_pos["x"]
        y = cloud_pos["y"]

        y = max(min_y, min(y, max_y))

        vel = pygame.Vector2(cloud_info["speed"], cloud_info["speed"])
        pos = pygame.Vector2(
            x - size.x / 2,
            y - size.y / 2,
        )
        cloud_entity = create_sprite(ecs_world, pos, vel, cloud_sprite, vel)
        ecs_world.add_component(cloud_entity, CAnimation(cloud_info["animations"]))
        ecs_world.add_component(cloud_entity, CTagCloud())
        ecs_world.add_component(cloud_entity, CSpeed(-cloud_info["speed"]))


def create_pixel_grid(
    ecs_world: esper.World,
    width: int,
    height: int,
    pixel_size: int,
    color: pygame.Color,
):
    center_x = width // 2
    center_y = height // 2
    delay_per_degree = 0.8
    for row in range(0, height, pixel_size):
        for col in range(0, width, pixel_size):
            dx = col + pixel_size // 2 - center_x
            dy = row + pixel_size // 2 - center_y

            angle_rad = math.atan2(-dy, dx)
            angle_deg = (math.degrees(angle_rad) + 360) % 360

            angle_from_top = (angle_deg - 90 + 360) % 360

            delay = int(angle_from_top * delay_per_degree)

            ecs_world.create_entity(
                CTransform(pygame.Vector2(col, row)),
                CPixel(pixel_size, color),
                CReveal(delay),
            )

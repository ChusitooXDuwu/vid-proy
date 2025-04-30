import pygame
import esper

from src.ecs.components.c_animation import CAnimation
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


def create_image(world: esper.World, interface_info: dict, image_type: str) -> int:
    surface = ServiceLocator.images_service.get(interface_info[image_type]["image"])
    pos = pygame.Vector2(
        interface_info[image_type]["pos"]["x"], interface_info[image_type]["pos"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    center = interface_info[image_type].get("center", False)
    return create_sprite(world, pos, vel, surface, center)


def create_ship(world: esper.World, player_cfg: dict, level_info: dict) -> int:
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
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_cfg["animations"]))
    # world.add_component(player_entity, CPlayerState()) TODO: Implement player state
    return player_entity


def create_logo(world: esper.World, logo_info: dict) -> int:
    surface = ServiceLocator.images_service.get(logo_info["image"])
    pos = pygame.Vector2(logo_info["pos"]["x"], logo_info["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    center = logo_info.get("center", False)
    return create_sprite(world, pos, vel, surface, center)


def create_clouds(
    ecs_world: esper.World,
    cloud_info: dict,
) -> int:
    cloud_sprite = ServiceLocator.images_service.get(cloud_info["image"])
    for cloud_pos in cloud_info["clouds"]:
        vel = pygame.Vector2(cloud_info["speed"], cloud_info["speed"])
        pos = pygame.Vector2(
            cloud_pos["x"],
            cloud_pos["y"],
        )
        cloud_entity = create_sprite(ecs_world, pos, vel, cloud_sprite, vel)
        ecs_world.add_component(cloud_entity, CTagCloud())
        ecs_world.add_component(cloud_entity, CSpeed(cloud_info["speed"]))

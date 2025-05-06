import pygame
import esper
import math

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_bullet_type import BulletType, CBulletType
from src.ecs.components.c_color_cycle import CColorCycle
from src.ecs.components.c_pixel import CPixel
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_reveal import CReveal
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
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


def create_info_bar(world: esper.World, width: int, height: int = 40, pos: pygame.Vector2 = pygame.Vector2(0, 0)) -> int:
    
    bar_entity = world.create_entity()
    color = pygame.Color(0, 0, 0)  
    
    surface = pygame.Surface((width, height))
    surface.fill(color)
    
    world.add_component(bar_entity, CTransform(pos))
    world.add_component(bar_entity, CSurface.from_surface(surface))
    
    return bar_entity

def create_top_info_bar(world: esper.World, width: int, height: int = 35) -> int:
    
    return create_info_bar(world, width, height, pygame.Vector2(0, 0))


def create_life_icon(
    world: esper.World,
    player_cfg: dict,
    pos: pygame.Vector2,
) -> int:
    player_sprite = ServiceLocator.images_service.get(player_cfg["image"])
    width, height = player_sprite.get_size()
    size = pygame.Vector2(width / player_cfg["animations"]["number_frames"], height)
    
    life_entity = world.create_entity()
 
    scale = 1
    scaled_width = int(size.x * scale)
    scaled_height = int(size.y * scale)
    

    frame_rect = pygame.Rect(
        0, 0, int(size.x), int(size.y)
    )
    

    try:
        frame = player_sprite.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
        
    
        world.add_component(life_entity, CTransform(pos))
        world.add_component(life_entity, CSurface.from_surface(scaled_frame))
    except ValueError as e:
        print(f"Error creating life icon: {e}")
    
    return life_entity


def create_enemy_counter(
    world: esper.World,
    image_path: str,
    base_pos: pygame.Vector2,
    count: int = 6,
    spacing: int = 20
) -> list[int]:
    counter_entities = []
    
    
    counter_sprite = ServiceLocator.images_service.get(image_path)
    
    for i in range(count):
        
        pos = pygame.Vector2(base_pos.x + (i * spacing), base_pos.y)
        
       
        counter_entity = world.create_entity()
        world.add_component(counter_entity, CTransform(pos))
        world.add_component(counter_entity, CSurface.from_surface(counter_sprite))
        
        counter_entities.append(counter_entity)
    
    return counter_entities



def create_bullet(
    world: esper.World,
    direction: pygame.Vector2,
    player_entity: int,
    bullet_cfg: dict,
    bullet_type: int = 1
) -> int:
    
    c_transform = world.component_for_entity(player_entity, CTransform)
    c_surface = world.component_for_entity(player_entity, CSurface)
    
   
    bullet_image = "assets/img/bullet_01_02_03.png"
    
   
    bullet_surface = ServiceLocator.images_service.get(bullet_image)
    
    
    bullet_width = bullet_surface.get_width() // 3  
    bullet_height = bullet_surface.get_height()
    

    bullet_type_index = (bullet_type - 1) % 3  
    bullet_rect = pygame.Rect(
        bullet_type_index * bullet_width, 0, 
        bullet_width, bullet_height
    )

    bullet_img = pygame.Surface((bullet_width, bullet_height), pygame.SRCALPHA)
    bullet_img.blit(bullet_surface, (0, 0), bullet_rect)
    
   
    player_size = pygame.Vector2(c_surface.area.width, c_surface.area.height)
    player_center_x = c_transform.pos.x + player_size.x / 2
    player_center_y = c_transform.pos.y + player_size.y / 2
    

    pos = pygame.Vector2(
        player_center_x - bullet_width / 2,
        player_center_y - bullet_height / 2
    )
    

    if direction.length_squared() > 0:
        direction = direction.normalize()
    vel = direction * bullet_cfg["velocity"]
    
  
    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CTransform(pos))
    world.add_component(bullet_entity, CVelocity(vel))
    
    
    bullet_surface_component = CSurface.from_surface(bullet_img)
    world.add_component(bullet_entity, bullet_surface_component)
    
    world.add_component(bullet_entity, CTagBullet())
    
    
    ServiceLocator.sounds_service.play(bullet_cfg["sound"])
    
    return bullet_entity



def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_cfg: dict) -> int:
    explosion_surface = ServiceLocator.images_service.get(explosion_cfg["image"])
    
    vel = pygame.Vector2(0, 0)
    explosion_entity = world.create_entity()
    world.add_component(explosion_entity, CTransform(pos))
    world.add_component(explosion_entity, CVelocity(vel))
    world.add_component(explosion_entity, CSurface.from_surface(explosion_surface))
    world.add_component(explosion_entity, CAnimation(explosion_cfg["animations"]))
    world.add_component(explosion_entity, CTagExplosion())

    ServiceLocator.sounds_service.play(explosion_cfg["sound"])
    return explosion_entity
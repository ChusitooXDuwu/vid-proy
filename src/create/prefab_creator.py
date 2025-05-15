import random
import pygame
import esper
import math

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_bullet_type import BulletType, CBulletType
from src.ecs.components.c_color_cycle import CColorCycle
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_path_change import CPathChange
from src.ecs.components.c_pixel import CPixel
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_render_priority import CRenderPriority
from src.ecs.components.c_reveal import CReveal
from src.ecs.components.c_rotation import CRotation
from src.ecs.components.c_speed import CSpeed
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_cloud import CTagCloud
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_pause_text import CTagPauseText
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_points import CPlayerPoints
from src.engine.service_locator import ServiceLocator


def create_text(
    world: esper.World,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    pos: pygame.Vector2,
    center: bool = False,
) -> int:
    """
    Creates a text entity in the given ECS world with specified properties.
    Args:
        world (esper.World): The ECS world where the entity will be created.
        text (str): The text to be rendered.
        font (pygame.font.Font): The font to be used for rendering the text.
        color (pygame.Color): The color of the text.
        pos (pygame.Vector2): The position of the text in the world.
        center (bool, optional): If True, the text will be centered at the given position.
            Defaults to False.
    Returns:
        int: The ID of the created text entity.
    """
    if center:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        pos = pygame.Vector2(pos.x - text_rect.width / 2, pos.y - text_rect.height / 2)

    text_entity = world.create_entity()
    world.add_component(text_entity, CTransform(pos))
    world.add_component(text_entity, CSurface.from_text(text, font, color))
    world.add_component(text_entity, CRenderPriority(100))
    return text_entity


def create_sprite(
    ecs_world: esper.World,
    pos: pygame.Vector2,
    vel: pygame.Vector2,
    surface: pygame.Surface,
    priority,
    center: bool = False,
) -> int:
    """
    Creates a sprite entity in the ECS world with the specified position, velocity,
    and surface. Optionally centers the sprite's position based on its dimensions.
    Args:
        ecs_world (esper.World): The ECS world where the entity will be created.
        pos (pygame.Vector2): The initial position of the sprite.
        vel (pygame.Vector2): The velocity of the sprite.
        surface (pygame.Surface): The surface representing the sprite's appearance.
        priority: The priority of the sprite.
        center (bool, optional): If True, adjusts the position to center the sprite
            based on its dimensions. Defaults to False.
    Returns:
        int: The ID of the created sprite entity.
    """

    if center:
        sprite_rect = surface.get_rect()
        pos = pygame.Vector2(
            pos.x - sprite_rect.width / 2, pos.y - sprite_rect.height / 2
        )

    sprite_entity = ecs_world.create_entity()
    ecs_world.add_component(sprite_entity, CTransform(pos))
    ecs_world.add_component(sprite_entity, CVelocity(vel))
    ecs_world.add_component(sprite_entity, CSurface.from_surface(surface))
    ecs_world.add_component(sprite_entity, CRenderPriority(priority))

    return sprite_entity


def create_text_interface(
    world: esper.World, interface_info: dict, interface_type: str
) -> int:
    """
    Creates a text interface entity in the game world.
    Args:
        world (esper.World): The ECS (Entity Component System) world where the entity will be created.
        interface_info (dict): A dictionary containing configuration details for the text interface.
            Expected keys:
                - "font": The name of the font to be used.
                - <interface_type>: A dictionary with the following keys:
                    - "size" (int): The font size.
                    - "color" (dict): A dictionary with "r", "g", and "b" keys for the RGB color values.
                    - "pos" (dict): A dictionary with "x" and "y" keys for the position.
                    - "text" (str): The text content to display.
                    - "center" (bool, optional): Whether to center the text. Defaults to False.
        interface_type (str): The type of interface to create, used as a key to access specific configuration
            details in the `interface_info` dictionary.
    Returns:
        int: The ID of the created entity in the ECS world.
    """

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
    
def create_text_interface_player_points(
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
    
    text = create_text(
        world, interface_info[interface_type]["text"], font, color, pos, center
    )
    
    world.add_component(text, CPlayerPoints())
    
    return text


def create_pause_text(
    world: esper.World, interface_info: dict, interface_type: str
) -> int:
    """
    Creates a pause text entity in the game world.
    """
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

    pause_text_entity = create_text(
        world, interface_info[interface_type]["text"], font, color, pos, center
    )

    colors_values = interface_info[interface_type]["color_cycle"]["colors"]
    colors = [
        pygame.Color(color["r"], color["g"], color["b"]) for color in colors_values
    ]

    cycle_time = interface_info[interface_type]["color_cycle"]["cycle_time"]
    world.add_component(pause_text_entity, CTagPauseText())
    world.add_component(pause_text_entity, CColorCycle(colors, cycle_time))
    return pause_text_entity


def create_text_interface_with_color_cycle(
    world: esper.World, interface_info: dict, interface_type: str
) -> int:
    """
    Creates a text interface entity with a color cycling effect.
    This function creates a text interface entity using the provided world,
    interface information, and interface type. It then adds a color cycling
    component to the entity, which cycles through a predefined list of colors.
    Args:
        world (esper.World): The ECS (Entity Component System) world where the
            entity will be created.
        interface_info (dict): A dictionary containing information about the
            text interface to be created.
        interface_type (str): A string specifying the type of the text interface.
    Returns:
        int: The ID of the created entity.
    """

    entity = create_text_interface(world, interface_info, interface_type)

    colors = [
        pygame.Color(255, 255, 255),
        pygame.Color(255, 0, 0),
        pygame.Color(0, 0, 255),
    ]
    world.add_component(entity, CColorCycle(colors, 0.3))

    return entity


def create_image(
    world: esper.World, interface_info: dict, priority: int, image_type: str
) -> int:
    """
    Creates a sprite entity in the given ECS world using the specified image type
    and interface information.

    Args:
        world (esper.World): The ECS world where the sprite entity will be created.
        interface_info (dict): A dictionary containing configuration data for the
            sprite, including position and image details.
            Expected keys:
                - <interface_type>: A dictionary with the following keys:
                    - "image" (str): The path of the image to be used.
                    - "pos" (dict): A dictionary with "x" and "y" keys for the position.
                    - "center" (bool, optional): Whether to center the text. Defaults to False.
        image_type (str): The key to access specific image and position data
            within the interface_info dictionary.

    Returns:
        int: The ID of the created sprite entity.
    """

    surface = ServiceLocator.images_service.get(interface_info[image_type]["image"])
    pos = pygame.Vector2(
        interface_info[image_type]["pos"]["x"], interface_info[image_type]["pos"]["y"]
    )
    vel = pygame.Vector2(0, 0)
    center = interface_info[image_type].get("center", False)
    return create_sprite(world, pos, vel, surface, 100, center)


def create_ship(
    world: esper.World, player_cfg: dict, level_info: dict, player_rotations: int, priority: int = 34
) -> int:
    """
    Creates a player ship entity in the game world with the specified configuration.

    Args:
        world (esper.World): The ECS (Entity Component System) world where the entity will be created.
        player_cfg (dict): Configuration dictionary for the player, including image and animation details.
        level_info (dict): Information about the level, including the initial position and rotation delay.
        player_rotations (int): Number of rotation directions for the player.

    Returns:
        int: The ID of the created player entity.
    """

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
        100,
    )
    directions = [
        pygame.Vector2(
            math.cos(2 * math.pi * i / player_rotations),
            math.sin(2 * math.pi * i / player_rotations),
        )
        for i in range(player_rotations)
    ]
    fire_action_z = world.create_entity()
    world.add_component(fire_action_z, CInputCommand("PLAYER_FIRE", pygame.K_z))
    left_action = world.create_entity()
    world.add_component(left_action, CInputCommand("PLAYER_LEFT", pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT))
    up_action = world.create_entity()
    world.add_component(up_action, CInputCommand("PLAYER_UP", pygame.K_UP))
    down_action = world.create_entity()
    world.add_component(down_action, CInputCommand("PLAYER_DOWN", pygame.K_DOWN))
    pause_action = world.create_entity()
    world.add_component(pause_action, CInputCommand("PLAYER_PAUSE", pygame.K_p))
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_cfg["animations"]))
    world.add_component(
        player_entity,
        CRotation(directions, level_info["rotation_delay"]),
    )
    world.add_component(player_entity, CPlayerState())
    world.add_component(player_entity, CRenderPriority(priority))
    return player_entity


def create_logo(world: esper.World, logo_info: dict) -> int:
    surface = ServiceLocator.images_service.get(logo_info["image"])
    pos = pygame.Vector2(logo_info["pos"]["x"], logo_info["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    center = logo_info.get("center", False)
    return create_sprite(world, pos, vel, surface, 100, center)


def create_clouds(
    ecs_world: esper.World,
    cloud_info: dict,
    priority: int,
    padding_top=30,
    padding_bottom=10,
) -> int:
    """
    Creates cloud entities in the ECS world based on the provided cloud information.
    Args:
        ecs_world (esper.World): The ECS world where the cloud entities will be created.
        cloud_info (dict): A dictionary containing information about the clouds, including:
            - "image" (str): The key for the cloud sprite image.
            - "animations" (dict): Animation details, including "number_frames".
            - "clouds" (list): A list of dictionaries with cloud positions, each containing:
                - "x" (float): The x-coordinate of the cloud.
                - "y" (float): The y-coordinate of the cloud.
            - "speed" (float): The speed of the clouds.
        padding_top (int, optional): The minimum distance from the top of the screen. Defaults to 30.
        padding_bottom (int, optional): The minimum distance from the bottom of the screen. Defaults to 10.
    Returns:
        int: The number of cloud entities created.
    """

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
        cloud_entity = create_sprite(ecs_world, pos, vel, cloud_sprite, priority, vel)
        ecs_world.add_component(cloud_entity, CAnimation(cloud_info["animations"]))
        ecs_world.add_component(cloud_entity, CTagCloud())
        ecs_world.add_component(cloud_entity, CSpeed(-cloud_info["speed"]))


def create_pixel_grid(
    ecs_world: esper.World,
    width: int,
    height: int,
    pixel_size: int,
    color: pygame.Color,
) -> None:
    """
    Creates a grid of pixel entities in the ECS world, with each pixel having a delay
    for its reveal animation based on its angular position relative to the center.
    Args:
        ecs_world (esper.World): The ECS world where the pixel entities will be created.
        width (int): The width of the grid in pixels.
        height (int): The height of the grid in pixels.
        pixel_size (int): The size of each pixel in the grid.
        color (pygame.Color): The color of the pixels.
    Each pixel entity is positioned in a grid layout and assigned a delay for its reveal
    animation based on its angular distance from the top of the grid's center.
    """

    center_x = width // 2
    center_y = height // 2
    delay_per_degree = 0.8
    for row in range(10, height, pixel_size):
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


def create_info_bar(
    world: esper.World,
    width: int,
    height: int = 40,
    pos: pygame.Vector2 = pygame.Vector2(0, 0),
) -> int:
    """
    Creates an information bar entity in the given ECS world.
    Args:
        world (esper.World): The ECS world where the entity will be created.
        width (int): The width of the information bar.
        height (int, optional): The height of the information bar. Defaults to 40.
        pos (pygame.Vector2, optional): The position of the information bar. Defaults to (0, 0).
    Returns:
        int: The ID of the created entity.
    """

    bar_entity = world.create_entity()
    color = pygame.Color(0, 0, 0)

    surface = pygame.Surface((width, height))
    surface.fill(color)

    world.add_component(bar_entity, CTransform(pos))
    world.add_component(bar_entity, CSurface.from_surface(surface))
    world.add_component(bar_entity, CRenderPriority(90))

    return bar_entity


def create_top_info_bar(world: esper.World, width: int, height: int = 35) -> int:

    return create_info_bar(world, width, height, pygame.Vector2(0, 0))


def create_life_icon(
    world: esper.World,
    player_cfg: dict,
    pos: pygame.Vector2,
) -> int:
    """
    Creates a life icon entity in the game world.
    This function generates a life icon entity using the player's sprite and configuration.
    The icon is scaled and positioned based on the provided parameters.
    Args:
        world (esper.World): The ECS (Entity Component System) world where the entity will be created.
        player_cfg (dict): A dictionary containing the player's configuration, including the sprite image
            and animation details. Expected keys:
            - "image": Path or identifier for the player's sprite image.
            - "animations": A dictionary with animation details, including "number_frames".
        pos (pygame.Vector2): The position where the life icon should be placed.
    Returns:
        int: The ID of the created life icon entity.
    Raises:
        ValueError: If there is an issue creating the subsurface for the life icon.
    """

    player_sprite = ServiceLocator.images_service.get(player_cfg["image"])
    width, height = player_sprite.get_size()
    size = pygame.Vector2(width / player_cfg["animations"]["number_frames"], height)

    life_entity = world.create_entity()

    scale = 1

    scaled_width = int(size.x * scale)
    scaled_height = int(size.y * scale)

    frame_rect = pygame.Rect(0, 0, int(size.x), int(size.y))

    try:
        frame = player_sprite.subsurface(frame_rect)
        scaled_frame = pygame.transform.scale(frame, (scaled_width, scaled_height))

        world.add_component(life_entity, CTransform(pos))
        world.add_component(life_entity, CSurface.from_surface(scaled_frame))
        world.add_component(life_entity, CRenderPriority(100))
    except ValueError as e:
        print(f"Error creating life icon: {e}")

    return life_entity


def create_enemy_counter(
    world: esper.World,
    image_path: str,
    base_pos: pygame.Vector2,
    count: int = 6,
    spacing: int = 20,
) -> list[int]:
    """
    Creates a series of enemy counter entities in the game world.
    Args:
        world (esper.World): The ECS (Entity Component System) world where the entities will be created.
        image_path (str): The file path to the image used for the counter sprites.
        base_pos (pygame.Vector2): The base position where the first counter entity will be placed.
        count (int, optional): The number of counter entities to create. Defaults to 6.
        spacing (int, optional): The horizontal spacing between consecutive counter entities. Defaults to 20.
    Returns:
        list[int]: A list of entity IDs for the created counter entities.
    """

    counter_entities = []

    counter_sprite = ServiceLocator.images_service.get(image_path)

    for i in range(count):

        pos = pygame.Vector2(base_pos.x + (i * spacing), base_pos.y)

        counter_entity = world.create_entity()
        world.add_component(counter_entity, CTransform(pos))
        world.add_component(counter_entity, CSurface.from_surface(counter_sprite))
        world.add_component(counter_entity, CRenderPriority(90))

        counter_entities.append(counter_entity)

    return counter_entities


def create_enemy_progress_bar(
    world: esper.World,
    base_pos: pygame.Vector2,
    enemy_icon_count: int,
    enemy_icon_spacing: int,
    enemies_killed: int,
    enemies_total: int,
    height: int,
    priority: int,
) -> int:
    """
    Creates a progress bar entity in the game world to represent the number of enemies killed.
    Args:
        world (esper.World): The ECS world where the entity will be created.
        base_pos (pygame.Vector2): The base position where the progress bar will be placed.
        enemy_icon_width (int): The width of each enemy icon.
        enemy_icon_count (int): The total number of enemy icons in the progress bar.
        enemy_icon_spacing (int): The horizontal spacing between enemy icons.
        enemies_killed (int): The number of enemies killed so far.
        height (int): The height of the progress bar.
        priority (int): The render priority for the progress bar entity.
    """

    total_width = enemy_icon_count * enemy_icon_spacing
    # Calcula la proporción de enemigos eliminados
    progress_ratio = min(enemies_killed / enemies_total, 1.0)
    covered_width = int(progress_ratio * total_width)
    cover_x = base_pos.x + total_width - covered_width

    surface = pygame.Surface((covered_width, height))
    color = pygame.Color(0, 0, 0)
    surface.fill(color)

    progress_bar_entity = world.create_entity()
    world.add_component(progress_bar_entity, CTransform(pygame.Vector2(cover_x, base_pos.y)))
    world.add_component(progress_bar_entity, CSurface.from_surface(surface))
    world.add_component(progress_bar_entity, CRenderPriority(priority))

    return progress_bar_entity
    

def create_bullet(
    world: esper.World,
    direction: pygame.Vector2,
    player_entity: int,
    bullet_cfg: dict,
    bullet_type: int = 1,
) -> int:

    c_transform = world.component_for_entity(player_entity, CTransform)
    c_surface = world.component_for_entity(player_entity, CSurface)

    c_rotation = world.component_for_entity(player_entity, CRotation)

    direction = c_rotation.directions[c_rotation.index]

    bullet_width = 1.5
    bullet_height = 1.5
    bullet_img = pygame.Surface((bullet_width, bullet_height))
    bullet_img.fill(pygame.Color(255, 255, 255))

    player_size = pygame.Vector2(c_surface.area.width, c_surface.area.height)
    player_center_x = c_transform.pos.x + player_size.x / 2
    player_center_y = c_transform.pos.y + player_size.y / 2

    pos = pygame.Vector2(
        player_center_x - bullet_width / 2, player_center_y - bullet_height / 2
    )

    if direction.length_squared() > 0:
        direction = direction.normalize()

    velocity = direction * bullet_cfg["velocity"]

    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CTransform(pos))
    world.add_component(bullet_entity, CVelocity(velocity))
    world.add_component(bullet_entity, CSurface.from_surface(bullet_img))
    world.add_component(bullet_entity, CTagBullet())
    world.add_component(bullet_entity, CRenderPriority(30))

    ServiceLocator.sounds_service.play(bullet_cfg["sound"])

    return bullet_entity


def create_explosion(
    world: esper.World, pos: pygame.Vector2, explosion_cfg: dict
) -> int:
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

def create_enemy(world: esper.World, pos: pygame.Vector2, enemies_info: dict):
    enemy_entity = world.create_entity()

    sprite_sheet = pygame.image.load(enemies_info['image']).convert_alpha()

    surface = CSurface.from_surface(sprite_sheet)
    surface.area = pygame.Rect(0, 0, 16, 16)
    world.add_component(enemy_entity, surface)
    world.add_component(enemy_entity, CTransform(pos))
    world.add_component(enemy_entity, CVelocity(pygame.Vector2(0, 0)))
    world.add_component(enemy_entity, CTagEnemy(enemies_info['points']))
    world.add_component(enemy_entity, CAnimation(enemies_info['animations']))
    world.add_component(enemy_entity, CPathChange())

    return enemy_entity

def spawn_enemy_random(world: esper.World, screen_rect: pygame.Rect, enemies_info: dict):
    side = random.choice(['top', 'bottom', 'left', 'right'])

    if side == 'top':
        x = random.uniform(0, screen_rect.width)
        y = 0 - 16  # Un poco fuera de pantalla
    elif side == 'bottom':
        x = random.uniform(0, screen_rect.width)
        y = screen_rect.height + 16
    elif side == 'left':
        x = 0 - 16
        y = random.uniform(0, screen_rect.height)
    elif side == 'right':
        x = screen_rect.width + 16
        y = random.uniform(0, screen_rect.height)

    pos = pygame.Vector2(x, y)

    center = pygame.Vector2(screen_rect.center)
    speed = random.uniform(30, 50)
    direction = (center - pos).normalize() * speed

    enemy_entity = create_enemy(world, pos, enemies_info)
    world.component_for_entity(enemy_entity, CVelocity).velocity = direction

def create_explosion_sprite(world: esper.World, pos: pygame.Vector2, explosion: dict) -> int:
    full_surface = ServiceLocator.images_service.get(explosion['image']).convert_alpha()
    number_frames = explosion["animations"]["number_frames"]
    frame_width = full_surface.get_width() // number_frames
    frame_height = full_surface.get_height()

    centered_pos = pygame.Vector2(
        pos.x - frame_width // 2,
        pos.y - frame_height // 2
    )

    vel = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, centered_pos, vel, full_surface, 80)

    c_surface = world.component_for_entity(explosion_entity, CSurface)
    c_surface.area = pygame.Rect(0, 0, frame_width, frame_height)

    world.add_component(explosion_entity, CAnimation(explosion["animations"]))
    world.add_component(explosion_entity, CTagExplosion())

    ServiceLocator.sounds_service.play(explosion["sound"])
    return explosion_entity

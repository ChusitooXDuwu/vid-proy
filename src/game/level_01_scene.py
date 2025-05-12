import json
import pygame
import src
from src.create.prefab_creator import (
    create_bullet,
    create_clouds,
    create_enemy_counter,
    create_image,
    create_info_bar,
    create_life_icon,
    create_pause_text,
    create_ship,
    create_text_interface,
    create_text_interface_with_color_cycle,
    create_top_info_bar,
)
import random
from numpy import spacing
import pygame
import src
from src.create.prefab_creator import create_clouds, create_enemy, create_enemy_counter, create_image, create_info_bar, create_life_icon, create_ship, create_text_interface, create_text_interface_with_color_cycle, spawn_enemy_random
from src.create.prefab_creator import create_bullet, create_clouds, create_enemy_counter, create_image, create_info_bar, create_life_icon, create_ship, create_text_interface, create_top_info_bar
from src.ecs.components.c_bullet_type import BulletType
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_rotation import CRotation, RotationEnum
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_movement import system_bullet_movement
from src.ecs.systems.s_cloud_respawner import system_cloud_respawner
from src.ecs.systems.s_collision_bullet_enemy import system_bullet_enemy_collision
from src.ecs.systems.s_color_cycle import system_color_cycle
from src.ecs.systems.s_enemy_movement_no_rebound import system_enemy_movement_no_rebound
from src.ecs.systems.s_enemy_steering import system_enemy_steering
from src.ecs.systems.s_explosion_animation_end import system_explosion_animation_end
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_remove_explosion_animation import system_remove_explosion_animation
from src.ecs.systems.s_rotation_update import system_rotation_update
from src.ecs.systems.s_screen_boundary_bullet import system_screen_boundary_bullet
from src.engine.scenes.scene import Scene


class Level01Scene(Scene):
    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_intro.json", encoding="utf-8") as intro_file:
            self.level_01_intro_cfg = json.load(intro_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as file:
            self.enemies_cfg = json.load(file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as file:
            self.explosion_cfg = json.load(file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as file:
            self.bullet_cfg = json.load(file)

        self._player_rotations = self.level_info["player_spawn"]["player_rotations"]

        self.player_entity = None
        self._bg_color = pygame.Color(
            self.level_info["bg"]["color"]["r"],
            self.level_info["bg"]["color"]["g"],
            self.level_info["bg"]["color"]["b"],
        )
        self.bullet_timer = None
        self.bullet_cooldown = None
        self.can_shoot = None
        self.enemy_counters = None
        self.a_d_1910 = None
        self.stage_1 = None
        self.player_1 = None

        self.intro_level_countdown_time = 4.0
        self.intro_level_elapsed_time = 0.0
        self._game_paused = False
        self._pause_text_entity = None

        self.total_enemigos = 40
        self.enemigos_creados = 0
        self.enemigos_activos = []

        self.total_spawned = 0

    def do_draw(self, screen):
        screen.fill(self._bg_color)
        return super().do_draw(screen, self._game_paused)

    def do_create(self):
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_back"],
            25,
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_middle"],
            30,
        )
        self.player_entity = create_ship(
            self.ecs_world,
            self.player_cfg,
            self.level_info["player_spawn"],
            self._player_rotations,
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_front"],
            35,
        )

        self.bullet_timer = 0.0  # TODO: Use game config
        self.bullet_cooldown = 0.0001  # TODO: Use game config
        self.can_shoot = True
        create_top_info_bar(self.ecs_world, self.screen_rect.width)

        bottom_bar_height = 10  # TODO: Use game config
        bottom_bar_pos = pygame.Vector2(0, self.screen_rect.height - bottom_bar_height)
        create_info_bar(
            self.ecs_world, self.screen_rect.width, bottom_bar_height, bottom_bar_pos
        )

        create_image(
            self.ecs_world, self.level_01_intro_cfg, 100, "small_level_counter"
        )

        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "high_score")
        create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "high_score_10000"
        )
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP_00")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "2-UP")

        base_x = 30  # TODO: Use game config
        life_pos_y = 20  # TODO: Use game config

        create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(base_x - 10, life_pos_y),  # TODO: Use game config
        )
        create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(base_x + 10, life_pos_y),  # TODO: Use game config
        )

        self._pause_text_entity = create_pause_text(
            self.ecs_world, self.level_info, "pause_text"
        )

        enemy_counter_base_pos = pygame.Vector2(
            10, self.screen_rect.height - 10
        )  # TODO: Use game config
        self.enemy_counters = create_enemy_counter(
            self.ecs_world,
            "assets/img/plane_counter_01.png",
            enemy_counter_base_pos,
            count=6,
            spacing=20,
        )

        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit_00")

        self.a_d_1910 = create_text_interface_with_color_cycle(
            self.ecs_world, self.level_01_intro_cfg, "a_d_1910"
        )
        self.stage_1 = create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "stage_1"
        )
        self.player_1 = create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "player_1"
        )

    def do_action(self, action: CInputCommand):
        if action.name == "PLAYER_PAUSE" and action.phase == CommandPhase.START:
            self._game_paused = not self._game_paused
            return

        if self._game_paused:
            return

        c_rotation = self.ecs_world.component_for_entity(self.player_entity, CRotation)

        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                c_rotation.current_horizontal = RotationEnum.LEFT
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_horizontal == RotationEnum.LEFT
            ):
                c_rotation.current_horizontal = RotationEnum.NONE

        elif action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                c_rotation.current_horizontal = RotationEnum.RIGHT
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_horizontal == RotationEnum.RIGHT
            ):
                c_rotation.current_horizontal = RotationEnum.NONE

        elif action.name == "PLAYER_UP":
            if action.phase == CommandPhase.START:
                c_rotation.current_vertical = RotationEnum.UP
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_vertical == RotationEnum.UP
            ):
                c_rotation.current_vertical = RotationEnum.NONE

        elif action.name == "PLAYER_DOWN":
            if action.phase == CommandPhase.START:
                c_rotation.current_vertical = RotationEnum.DOWN
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_vertical == RotationEnum.DOWN
            ):
                c_rotation.current_vertical = RotationEnum.NONE

        elif action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                if (
                    self.can_shoot
                    and self.intro_level_elapsed_time >= self.intro_level_countdown_time
                ):
                    c_rotation = self.ecs_world.component_for_entity(
                        self.player_entity, CRotation
                    )
                    direction = c_rotation.directions[c_rotation.index]

                    create_bullet(
                        self.ecs_world,
                        direction,
                        self.player_entity,
                        self.bullet_cfg,
                        1,
                    )

                    self.can_shoot = False
                    self.bullet_timer = 0.0

    def do_update(self, delta_time: float):
        self.intro_level_elapsed_time += delta_time
        if self.intro_level_elapsed_time >= self.intro_level_countdown_time:
            if self.ecs_world.entity_exists(self.a_d_1910):
                self.ecs_world.delete_entity(self.a_d_1910)
            if self.ecs_world.entity_exists(self.stage_1):
                self.ecs_world.delete_entity(self.stage_1)
            if self.ecs_world.entity_exists(self.player_1):
                self.ecs_world.delete_entity(self.player_1)

        system_color_cycle(
            self.ecs_world,
            delta_time,
            self.level_01_intro_cfg,
        )

        if not self._game_paused:
            system_animation(self.ecs_world, delta_time)
            system_cloud_respawner(self.ecs_world, self.screen_rect)
            system_movement(self.ecs_world, delta_time, self.player_entity)
            system_rotation_update(self.ecs_world, delta_time)
            system_player_state(self.ecs_world)
            system_bullet_movement(self.ecs_world, delta_time)
            system_screen_boundary_bullet(self.ecs_world, self.screen_rect)
            system_bullet_enemy_collision(self.ecs_world, self.explosion_cfg['enemy'])
            system_explosion_animation_end(self.ecs_world)

            if not self.can_shoot:
                self.bullet_timer += delta_time
                if self.bullet_timer >= self.bullet_cooldown:
                    self.can_shoot = True

        system_color_cycle(self.ecs_world, delta_time, self.level_01_intro_cfg, self.level_01_intro_cfg["a_d_1910"])
        system_animation(self.ecs_world, delta_time)
        system_cloud_respawner(self.ecs_world, self.screen_rect)
        system_movement(self.ecs_world, delta_time, self.player_entity)
        system_rotation_update(self.ecs_world, delta_time, self._pending_direction)
        system_player_state(self.ecs_world)
        system_bullet_movement(self.ecs_world, delta_time)
        system_screen_boundary_bullet(self.ecs_world, self.screen_rect)
        system_bullet_enemy_collision(self.ecs_world, self.explosion_cfg['enemy'])

        if not self.can_shoot:
            self.bullet_timer += delta_time
            if self.bullet_timer >= self.bullet_cooldown:
                self.can_shoot = True

        if self.intro_level_elapsed_time >= self.intro_level_countdown_time:
            system_enemy_movement_no_rebound(self.ecs_world, self.screen_rect, self.enemies_cfg, self.total_spawned, delta_time)

        system_remove_explosion_animation(self.ecs_world)


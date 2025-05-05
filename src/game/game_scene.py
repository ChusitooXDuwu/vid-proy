import json
import pygame
from src.create.prefab_creator import create_clouds, create_ship, create_text_interface
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_rotation import RotationEnum
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_cloud_respawner import system_cloud_respawner
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rotation_update import system_rotation_update
from src.engine.scenes.scene import Scene


class GameScene(Scene):
    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_intro.json") as intro_file:
            self.level_01_intro_cfg = json.load(intro_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)
        self._player_rotations = self.level_info["player_spawn"]["player_rotations"]

        self._pending_direction = RotationEnum.NONE
        self.player_entity = None
        self._bg_color = pygame.Color(
            self.level_info["bg"]["color"]["r"],
            self.level_info["bg"]["color"]["g"],
            self.level_info["bg"]["color"]["b"],
        )

    def do_draw(self, screen):
        screen.fill(self._bg_color)
        return super().do_draw(screen)

    def do_create(self):
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_back"],
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_middle"],
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
        )

        left_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            left_action, CInputCommand("PLAYER_LEFT", pygame.K_LEFT)
        )

        right_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            right_action, CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT)
        )
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "high_score")
        create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "high_score_10000"
        )
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP_00")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "2-UP")

    def do_action(self, action: CInputCommand):
        if action.phase == CommandPhase.START:
            if action.name == "PLAYER_LEFT":
                self._pending_direction = RotationEnum.LEFT
            elif action.name == "PLAYER_RIGHT":
                self._pending_direction = RotationEnum.RIGHT
        elif action.phase == CommandPhase.END:
            self._pending_direction = RotationEnum.NONE

    def do_update(self, delta_time: float):
        system_animation(self.ecs_world, delta_time)
        system_cloud_respawner(self.ecs_world, self.screen_rect)
        system_movement(self.ecs_world, delta_time, self.player_entity)
        system_rotation_update(self.ecs_world, delta_time, self._pending_direction)
        system_player_state(self.ecs_world)

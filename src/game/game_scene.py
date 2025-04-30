import math
import json
import pygame
from src.create.prefab_creator import create_clouds, create_ship
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_cloud_respawner import system_cloud_respawner
from src.ecs.systems.s_movement import system_movement
from src.engine.scenes.scene import Scene


class GameScene(Scene):
    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)
        self._player_rotations = self.level_info["player_spawn"]["player_rotations"]
        self._directions = [
            pygame.Vector2(
                math.cos(2 * math.pi * i / self._player_rotations),
                math.sin(2 * math.pi * i / self._player_rotations),
            )
            for i in range(self._player_rotations)
        ]
        self._current_dir_index = 0
        self._global_velocity_direction = self._directions[self._current_dir_index]

    def do_create(self):
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_back"],
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_middle"],
        )
        create_ship(
            self.ecs_world,
            self.player_cfg,
            self.level_info["player_spawn"],
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

    def do_action(self, action: CInputCommand):
        if action.phase == CommandPhase.START:
            if action.name == "PLAYER_LEFT":
                self._current_dir_index = (
                    self._current_dir_index - 1
                ) % self._player_rotations
            elif action.name == "PLAYER_RIGHT":
                self._current_dir_index = (
                    self._current_dir_index + 1
                ) % self._player_rotations
            self._global_velocity_direction = self._directions[self._current_dir_index]

    def do_update(self, delta_time: float):
        system_animation(self.ecs_world, delta_time)
        system_cloud_respawner(self.ecs_world, self.screen_rect)
        system_movement(self.ecs_world, delta_time, self._global_velocity_direction)

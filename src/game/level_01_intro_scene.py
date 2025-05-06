import json
import src
from src.create.prefab_creator import create_clouds, create_ship, create_text_interface, create_text_interface_with_color_cycle
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_rotation import RotationEnum
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_cloud_respawner import system_cloud_respawner
from src.ecs.systems.s_color_cycle import system_color_cycle
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rotation_update import system_rotation_update
from src.engine.scenes.scene import Scene


class Level01IntroScene(Scene):

    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_intro.json") as intro_file:
            self.level_01_intro_cfg = json.load(intro_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)

        self._pending_direction = RotationEnum.NONE
        self._player_rotations = self.level_info["player_spawn"]["player_rotations"]

        self.countdown_time = 4.0
        self.elapsed_time = 0.0


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
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "player_1")
        create_text_interface_with_color_cycle(self.ecs_world, self.level_01_intro_cfg, 'a_d_1910')
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "stage_1")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "high_score")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, 'high_score_10000')
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, '1-UP_00')
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "2-UP")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit_00")

    def do_update(self, delta_time: float):
        self.elapsed_time += delta_time

        if self.elapsed_time >= self.countdown_time:
            self.switch_scene("GAME_SCENE")

        system_color_cycle(self.ecs_world, delta_time, self.level_01_intro_cfg, self.level_01_intro_cfg["a_d_1910"])
        system_animation(self.ecs_world, delta_time)
        system_cloud_respawner(self.ecs_world, self.screen_rect)
        system_movement(self.ecs_world, delta_time, self.player_entity)
        system_rotation_update(self.ecs_world, delta_time, self._pending_direction)

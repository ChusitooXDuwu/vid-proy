import json
import pygame

from src.create.prefab_creator import create_image, create_text_interface
from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand

import src.engine.game_engine


class Level01MenuScene(Scene):

    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_menu.json") as paddle_file:
            self.level_01_menu_cfg = json.load(paddle_file)

        self.countdown_time = 4.0
        self.elapsed_time = 0.0

    def do_create(self):

        self.elapsed_time = 0.0

        create_image(self.ecs_world, self.level_01_menu_cfg, "logo")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "play_prompt")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "copyright")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "push_button")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "one_player")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "1st_bonus")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "and_pts")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "high_score")
        create_text_interface(
            self.ecs_world, self.level_01_menu_cfg, "high_score_10000"
        )
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "1-UP_00")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "2-UP")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "credit")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "credit_00")

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            start_game_action, CInputCommand("START_GAME", pygame.K_RETURN)
        )

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("MENU_SCENE")

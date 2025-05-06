import json
import pygame

import src
from src.create.prefab_creator import create_image, create_text_interface
from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand


class MenuScene(Scene):

    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/menu.json", encoding="utf-8") as paddle_file:
            self.menu_cfg = json.load(paddle_file)

    def do_create(self):

        create_image(self.ecs_world, self.menu_cfg, "logo")
        create_image(self.ecs_world, self.menu_cfg, "small_level_counter")
        create_text_interface(self.ecs_world, self.menu_cfg, "play_prompt")
        create_text_interface(self.ecs_world, self.menu_cfg, "copyright")
        create_text_interface(self.ecs_world, self.menu_cfg, "insert_coin")
        create_text_interface(self.ecs_world, self.menu_cfg, "try_game")
        create_text_interface(self.ecs_world, self.menu_cfg, "high_score")
        create_text_interface(self.ecs_world, self.menu_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.menu_cfg, "2-UP")
        create_text_interface(self.ecs_world, self.menu_cfg, "credit")
        create_text_interface(self.ecs_world, self.menu_cfg, "credit_00")
        create_text_interface(self.ecs_world, self.menu_cfg, "1-UP_00")
        create_text_interface(self.ecs_world, self.menu_cfg, "high_score_10000")


        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            start_game_action, CInputCommand("SCORE_TABLE", pygame.K_RETURN)
        )

    def do_action(self, action: CInputCommand):
        if action.name == "SCORE_TABLE":
            self.switch_scene("SCORE_TABLE_SCENE")

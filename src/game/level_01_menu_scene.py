import json
import pygame

from src.create.prefab_creator import create_image, create_pixel_grid, create_text_interface
from src.ecs.systems.s_render_pixels import system_render_pixels
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_reveal_animation import system_reveal_animation
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

        self.showing_transition = False
        self.transition_elapsed = 0.0
        self.transition_duration = 2.03  # Igual que ScoreTableScene

    def do_create(self):
        self.elapsed_time = 0.0

        create_image(self.ecs_world, self.level_01_menu_cfg, 100, "logo")
        create_image(self.ecs_world, self.level_01_menu_cfg, 100, "small_level_counter")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "play_prompt")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "copyright")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "push_button")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "move_ship")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "shoot")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "pause")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "1st_bonus")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "and_pts")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "high_score")
        create_text_interface(self.ecs_world, self.level_01_menu_cfg, "high_score_10000")
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
        if action.name == "START_GAME" and not self.showing_transition:
            self.showing_transition = True
            self.transition_elapsed = 0.0
            create_pixel_grid(
                self.ecs_world,
                self._game_engine.screen.get_width(),
                self._game_engine.screen.get_height(),
                10,
                pygame.Color(16, 4, 116),
            )

    def do_update(self, delta_time: float):
        self.elapsed_time += delta_time

        if self.showing_transition:
            self.transition_elapsed += delta_time
            self.tick = int(self.transition_elapsed * 150)
            system_reveal_animation(self.ecs_world, self.tick)

            if self.transition_elapsed >= self.transition_duration:
                self.switch_scene("LEVEL_01_SCENE")

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
        system_render_pixels(self.ecs_world, screen)


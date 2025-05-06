import json

import pygame

import src
from src.create.prefab_creator import (
    create_image,
    create_pixel_grid,
    create_text_interface,
)
from src.ecs.systems.s_render_pixels import system_render_pixels
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_reveal_animation import system_reveal_animation
from src.engine.scenes.scene import Scene


class ScoreTableScene(Scene):

    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/score_table.json", encoding="utf-8") as paddle_file:
            self.score_table_cfg = json.load(paddle_file)

        self.countdown_time = 4.0
        self.elapsed_time = 0.0

        self.showing_transition = False
        self.transition_elapsed = 0.0
        self.transition_duration = 2.03

    def do_create(self):

        self.elapsed_time = 0.0

        create_image(self.ecs_world, self.score_table_cfg, "logo")
        create_image(self.ecs_world, self.score_table_cfg, "small_level_counter")
        create_text_interface(self.ecs_world, self.score_table_cfg, "play_prompt")
        create_text_interface(self.ecs_world, self.score_table_cfg, "copyright")
        create_text_interface(self.ecs_world, self.score_table_cfg, "score_table_label")
        create_text_interface(self.ecs_world, self.score_table_cfg, "leaderboard_1st")
        create_text_interface(self.ecs_world, self.score_table_cfg, "leaderboard_2nd")
        create_text_interface(self.ecs_world, self.score_table_cfg, "leaderboard_3rd")
        create_text_interface(self.ecs_world, self.score_table_cfg, "leaderboard_4th")
        create_text_interface(self.ecs_world, self.score_table_cfg, "leaderboard_5th")
        create_text_interface(self.ecs_world, self.score_table_cfg, "high_score")
        create_text_interface(self.ecs_world, self.score_table_cfg, "high_score_10000")
        create_text_interface(self.ecs_world, self.score_table_cfg, "1-UP")
        create_text_interface(self.ecs_world, self.score_table_cfg, "1-UP_00")
        create_text_interface(self.ecs_world, self.score_table_cfg, "2-UP")
        create_text_interface(self.ecs_world, self.score_table_cfg, "credit")
        create_text_interface(self.ecs_world, self.score_table_cfg, "credit_00")
        

    def do_update(self, delta_time: float):
        self.elapsed_time += delta_time

        if not self.showing_transition and self.elapsed_time >= self.countdown_time:
            self.showing_transition = True
            self.transition_elapsed = 0.0
            print("Transitioning to level 01 menu scene")
            print("Creating pixel grid")
            print("Screen size: ", self._game_engine.screen.get_width(), self._game_engine.screen.get_height())
            create_pixel_grid(
                self.ecs_world,
                self._game_engine.screen.get_width(),
                self._game_engine.screen.get_height(),
                10,
                pygame.Color(16, 4, 116),  # TODO: use color from config
            )

        if self.showing_transition:
            self.transition_elapsed += delta_time
            self.tick = int(self.transition_elapsed * 150)
            system_reveal_animation(self.ecs_world, self.tick)

            if self.transition_elapsed >= self.transition_duration:
                self.switch_scene("LEVEL_01_MENU_SCENE")

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
        system_render_pixels(self.ecs_world, screen)

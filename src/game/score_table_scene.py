import json
import pygame

from src.create.prefab_creator import create_image, create_text_interface
from src.engine.scenes.scene import Scene
from src.ecs.components.c_input_command import CInputCommand 

import src.engine.game_engine


class ScoreTableScene(Scene):
    
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        
        with open("assets/cfg/score_table.json") as paddle_file:
            self.score_table_cfg = json.load(paddle_file)
        
        self.countdown_time = 4.0
        self.elapsed_time = 0.0
        
    def do_create(self):
        
        self.elapsed_time = 0.0
        
        create_image(self.ecs_world, self.score_table_cfg, 'logo')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'play_prompt')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'copyright')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'score_table_label')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'leaderboard_1st')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'leaderboard_2nd')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'leaderboard_3rd')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'leaderboard_4th')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'leaderboard_5th')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'high_score')
        create_text_interface(self.ecs_world, self.score_table_cfg, '1-UP')
        create_text_interface(self.ecs_world, self.score_table_cfg, '2-UP')
        create_text_interface(self.ecs_world, self.score_table_cfg, 'credit')
        create_text_interface(self.ecs_world, self.score_table_cfg, '00')
                      
    def do_update(self, deltatime: float):
        self.elapsed_time += deltatime
        
        if self.elapsed_time >= self.countdown_time:
            self.switch_scene("MENU_SCENE")  # TODO: Change to the game scene


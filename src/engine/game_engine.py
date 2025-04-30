import json
import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand
from src.engine.scenes.scene import Scene
from src.game.menu_scene import MenuScene
from src.game.score_table_scene import ScoreTableScene


class GameEngine:
    def __init__(self) -> None:
        # Load configuration from JSON file
        with open("./assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)

        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode(
            (self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), pygame.SCALED
        )
        self._bg_color = pygame.Color(
            self.window_cfg["bg_color"]["r"],
            self.window_cfg["bg_color"]["g"],
            self.window_cfg["bg_color"]["b"],
        )

        # Initialize the clock
        self._clock = pygame.time.Clock()
        self._framerate = self.window_cfg["framerate"]
        self._delta_time = 0

        self.is_paused = False
        self.is_running = False

        # Initialize the world
        self.ecs_world = esper.World()
        
        # Scene management
        self._scenes:dict[str, Scene] = {}
        
        self._scenes["MENU_SCENE"] = MenuScene(self)
        self._scenes["SCORE_TABLE_SCENE"] = ScoreTableScene(self)
        
        self._current_scene:Scene = None
        self._scene_name_to_switch:str = None
        

    def run(self, start_scene_name:str) -> None:
        self.is_running = True
        self._current_scene = self._scenes[start_scene_name]
        self._create()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            self._handle_switch_scene()
        self._do_clean()
        
    def switch_scene(self, new_scene_name:str):
        self._scene_name_to_switch = new_scene_name
        
    def _create(self):
        self._current_scene.do_create()    
    
    def _calculate_time(self):
        self._clock.tick(self._framerate)
        self._delta_time = self._clock.get_time() / 1000.0
        
    def _process_events(self):
        for event in pygame.event.get():
            self._current_scene.do_process_events(event)
            if event.type == pygame.QUIT:
                self.is_running = False
                
    def _update(self):
        self._current_scene.simulate(self._delta_time)
        
    def _draw(self):
        self.screen.fill(self._bg_color)        
        self._current_scene.do_draw(self.screen)
        pygame.display.flip()    
        
    def _handle_switch_scene(self):
        if self._scene_name_to_switch is not None:
            self._current_scene.clean()
            self._current_scene = self._scenes[self._scene_name_to_switch]
            self._current_scene.do_create()
            self._scene_name_to_switch = None

    
    def _do_action(self, action:CInputCommand):        
        self._current_scene.do_action(action)
    
    
    def _do_clean(self):
        if self._current_scene is not None:
            self._current_scene.clean()
        pygame.quit()

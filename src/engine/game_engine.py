import pygame
import esper
import json

from src.create.prefab_creator import create_input_player, create_logo, create_text_interface
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_rendering import system_rendering


class GameEngine:
    def __init__(self) -> None:
        # Load configuration from JSON file
        self._load_json()
        
        # Initialize Pygame
        pygame.init()
        pygame.display.set_caption(self.window_cfg["title"])
        self.screen = pygame.display.set_mode((self.window_cfg["size"]["w"], self.window_cfg["size"]["h"]), 
                                              pygame.SCALED)
        self.bg_color = pygame.Color(self.window_cfg["bg_color"]["r"], 
                                     self.window_cfg["bg_color"]["g"], 
                                     self.window_cfg["bg_color"]["b"])
        
        # Initialize the clock
        self.clock = pygame.time.Clock()
        self.framerate = self.window_cfg["framerate"]
        self.delta_time = 0
        
        self.is_paused = False
        self.is_running = False
        self.mode = 'screen_1'
        
        # Initialize the world
        self.ecs_world = esper.World()

    def _load_json(self):
        with open("./assets/cfg/window.json", encoding="utf-8") as window_file:
            self.window_cfg = json.load(window_file)
        with open("./assets/cfg/interface.json", encoding="utf-8") as interface_file:
            self.interface_cfg = json.load(interface_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()


    def _create_multiple(self, interface_cfg:dict, type:str):
        entity_list = []
        for name in interface_cfg[type]:
            if "text" in interface_cfg[type][name]:
                entity_list.append(create_text_interface(self.ecs_world, self.interface_cfg[type][name]))
            elif "image" in interface_cfg[type][name]:
                entity_list.append(create_logo(self.ecs_world, self.interface_cfg[type][name]))
        
        return entity_list
    
    def _create(self):
        
        create_input_player(self.ecs_world)
        
        # Create constants
        self.constants_entities = self._create_multiple(self.interface_cfg, "constants")
        
        # Create screen 1
        self.screen_entities = self._create_multiple(self.interface_cfg, "screen_1")
    
    
    
    
    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for events in pygame.event.get():
            system_input_player(self.ecs_world, events, self._do_action)
            if events.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
    
    def _do_action(self, c_input:CInputCommand):
        if c_input.name == "NEXT_SCREEN":
            if c_input.phase == CommandPhase.START:
                if self.mode == "screen_1":
                    self.mode = "screen_2"
                    for entity in self.screen_entities:
                        self.ecs_world.delete_entity(entity)
                    self.screen_entities = self._create_multiple(self.interface_cfg, "screen_2")
                
                
        

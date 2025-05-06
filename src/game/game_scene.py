import json
from numpy import spacing
import pygame
from src.create.prefab_creator import create_bullet, create_clouds, create_enemy_counter, create_info_bar, create_life_icon, create_ship, create_text_interface, create_top_info_bar
from src.ecs.components.c_bullet_type import BulletType
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_rotation import CRotation, RotationEnum
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_cloud_respawner import system_cloud_respawner
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_explosion_animation_end import system_explosion_animation_end
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rotation_update import system_rotation_update
from src.ecs.systems.s_screen_boundary_bullet import system_screen_boundary_bullet
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class GameScene(Scene):
    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_intro.json") as intro_file:
            self.level_01_intro_cfg = json.load(intro_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)

        with open("assets/cfg/explosion.json", encoding="utf-8") as file:
            self.explosion_cfg = json.load(file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as file:
            self.bullet_cfg = json.load(file)

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

   
        create_top_info_bar(self.ecs_world, self.screen_rect.width)

        
        bottom_bar_height = 10
        bottom_bar_pos = pygame.Vector2(0, self.screen_rect.height - bottom_bar_height)
        create_info_bar(self.ecs_world, self.screen_rect.width, bottom_bar_height, bottom_bar_pos)

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

       
        base_x = 30  
        life_pos_y = 20  
        
        create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(base_x - 10, life_pos_y)
        )
        create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(base_x + 10, life_pos_y)
        )


        enemy_counter_base_pos = pygame.Vector2(10, self.screen_rect.height - 10)
        self.enemy_counters = create_enemy_counter(
            self.ecs_world,
            "assets/img/plane_counter_01.png",
            enemy_counter_base_pos,
            count=6,
            spacing=20
        )
       
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit_00")

        self.bullet_timer = 0.0
        self.bullet_cooldown = 0.2  
        self.can_shoot = True
        
        
        fire_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(
            fire_action, CInputCommand("PLAYER_FIRE", pygame.K_SPACE)
        )


    def do_action(self, action: CInputCommand):
        if action.phase == CommandPhase.START:
            if action.name == "PLAYER_LEFT":
                self._pending_direction = RotationEnum.LEFT
            elif action.name == "PLAYER_RIGHT":
                self._pending_direction = RotationEnum.RIGHT
            if action.name == "PLAYER_FIRE" and action.phase == CommandPhase.START:
               if self.can_shoot:
                   
                    c_rotation = self.ecs_world.component_for_entity(self.player_entity, CRotation)
                    direction = c_rotation.directions[c_rotation.index]
                    
                   
                    create_bullet(
                        self.ecs_world,        
                        direction,              
                        self.player_entity,     
                        self.bullet_cfg,        
                        1                       
                    )
                    
                    
                    self.can_shoot = False
                    self.bullet_timer = 0.0
        elif action.phase == CommandPhase.END:
            self._pending_direction = RotationEnum.NONE

    def do_update(self, delta_time: float):
        system_animation(self.ecs_world, delta_time)
        system_cloud_respawner(self.ecs_world, self.screen_rect)
        system_movement(self.ecs_world, delta_time, self.player_entity)
        system_rotation_update(self.ecs_world, delta_time, self._pending_direction)
        system_player_state(self.ecs_world)

        system_screen_boundary_bullet(self.ecs_world, self.screen_rect)
        system_collision_bullet_enemy(self.ecs_world, self.explosion_cfg)
        system_explosion_animation_end(self.ecs_world)
        
        if not self.can_shoot:
            self.bullet_timer += delta_time
            if self.bullet_timer >= self.bullet_cooldown:
                self.can_shoot = True

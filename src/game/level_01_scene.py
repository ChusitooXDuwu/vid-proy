import json
import pygame
import src
from src.create.prefab_creator import (
    create_bullet,
    create_clouds,
    create_enemy_counter,
    create_image,
    create_info_bar,
    create_life_icon,
    create_pause_text,
    create_ship,
    create_text_interface,
    create_text_interface_player_points,
    create_text_interface_with_color_cycle,
    create_top_info_bar,
    create_enemy_progress_bar,
    delete_all_clouds,
    delete_all_enemies,
)
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_rotation import CRotation, RotationEnum
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_boss_enemy_spawner import system_boss_enemy_spawner
from src.ecs.systems.s_bullet_movement import system_bullet_movement
from src.ecs.systems.s_cloud_respawner import system_respawner
from src.ecs.systems.s_collision_bullet_enemy import system_bullet_enemy_collision
from src.ecs.systems.s_color_cycle import system_color_cycle
from src.ecs.systems.s_enemy_movement_no_rebound import system_enemy_movement_no_rebound
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_remove_explosion_animation import (
    system_remove_explosion_animation,
)
from src.ecs.systems.s_rotation_update import system_rotation_update
from src.ecs.systems.s_screen_boundary_bullet import system_screen_boundary_bullet
from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator


class Level01Scene(Scene):
    def __init__(self, engine: "src.engine.game_engine.GameEngine") -> None:
        super().__init__(engine)

        with open("assets/cfg/level_01_intro.json", encoding="utf-8") as intro_file:
            self.level_01_intro_cfg = json.load(intro_file)
        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)
        with open("assets/cfg/enemies.json", encoding="utf-8") as file:
            self.enemies_cfg = json.load(file)
        with open("assets/cfg/explosion.json", encoding="utf-8") as file:
            self.explosion_cfg = json.load(file)
        with open("assets/cfg/bullet.json", encoding="utf-8") as file:
            self.bullet_cfg = json.load(file)

        self._player_rotations = self.level_info["player_spawn"]["player_rotations"]

        self.player_entity = None
        self._bg_color = pygame.Color(
            self.level_info["bg"]["color"]["r"],
            self.level_info["bg"]["color"]["g"],
            self.level_info["bg"]["color"]["b"],
        )
        
        self.bullet_timer = 0.0  # TODO: Use game config
        self.bullet_cooldown = 0.0001  # TODO: Use game config
        self.can_shoot = True
        
        # self.bullet_timer = None
        # self.bullet_cooldown = None
        # self.can_shoot = None
        
        self.enemy_counters = None
        self.a_d_1910 = None
        self.stage_1 = None
        self.player_1 = None

        self.intro_level_countdown_time = 3.0
        self.intro_level_elapsed_time = 0.0
        self._game_paused = False
        self._pause_text_entity = None

        self.enemies_killed = 0
        self.enemies_total = self.enemies_cfg["total_minion_enemies"]

        self.total_spawned = 0
        self.player_points = 0

        self._game_over = False
        self._game_over_timer = 0.0
        self._game_over_delay = 3.0
        self._waiting_to_switch = False
        
        self.game_over_countdown_time = 0.0
        self.game_over_time_to_appear = 2.5

        self.enemy_progress_bar = None

        self.player_points_text = None
        self.enemy_counter_base_pos = None
        self.enemy_icon_count = None
        self.enemy_icon_spacing = None
        
        self.lifes = []
        
        

    def _set_entities_visibility(self, visible: bool):
        # Player
        if self.player_entity is not None and self.ecs_world.entity_exists(
            self.player_entity
        ):
            if self.ecs_world.has_component(self.player_entity, CSurface):
                self.ecs_world.component_for_entity(
                    self.player_entity, CSurface
                ).visible = visible

        # Intro elements
        if self.player_1 is not None and self.ecs_world.entity_exists(self.player_1):
            if self.ecs_world.has_component(self.player_1, CSurface):
                self.ecs_world.component_for_entity(self.player_1, CSurface).visible = (
                    visible
                )

        if self.stage_1 is not None and self.ecs_world.entity_exists(self.stage_1):
            if self.ecs_world.has_component(self.stage_1, CSurface):
                self.ecs_world.component_for_entity(self.stage_1, CSurface).visible = (
                    visible
                )

        if self.a_d_1910 is not None and self.ecs_world.entity_exists(self.a_d_1910):
            if self.ecs_world.has_component(self.a_d_1910, CSurface):
                self.ecs_world.component_for_entity(self.a_d_1910, CSurface).visible = (
                    visible
                )

        # Enemies and bullets
        for ent, c_surf in self.ecs_world.get_component(CSurface):
            # Bullets
            if self.ecs_world.has_component(
                ent, CTagBullet
            ) or self.ecs_world.has_component(ent, CTagEnemy):
                c_surf.visible = visible


    def do_draw(self, screen, _: bool = False):
        screen.fill(self._bg_color)
        return super().do_draw(screen, self._game_paused)

    def do_create(self):
        # Background Clouds
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_back"],
            25,
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_middle"],
            30,
        )
        create_clouds(
            self.ecs_world,
            self.level_info["clouds"]["clouds_front"],
            35,
        )
        
        # Player Ship
        self.player_entity = create_ship(
            self.ecs_world,
            self.player_cfg,
            self.level_info["player_spawn"],
            self._player_rotations,
        )

        # Top Bar Elements
        create_top_info_bar(self.ecs_world, self.screen_rect.width)
        
        create_image(
            self.ecs_world, self.level_01_intro_cfg, 100, "small_level_counter"
        )

        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "high_score")
        create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "high_score_10000"
        )
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "1-UP")
        self.player_points_text = create_text_interface_player_points(
            self.ecs_world, self.level_01_intro_cfg, "1-UP_00"
        )

        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "2-UP")
        
        # Bottom Bar Elements
        bottom_bar_height = 10  # TODO: Use game config
        bottom_bar_pos = pygame.Vector2(0, self.screen_rect.height - bottom_bar_height)
        
        create_info_bar(
            self.ecs_world, self.screen_rect.width, bottom_bar_height, bottom_bar_pos
        )

        

        self.lifes.append(create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(10, 20),  
        ))
        self.lifes.append(create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(25, 20),  
        ))
        self.lifes.append( create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(40, 20),  
        ))
        self.lifes.append( create_life_icon(
            self.ecs_world,
            self.player_cfg,
            pygame.Vector2(55, 20),  
        ))
        
        self.enemy_counter_base_pos = pygame.Vector2(
            10, self.screen_rect.height - 10
        )  # TODO: Use game config
        self.enemy_icon_count = 6
        self.enemy_icon_spacing = 20
        self.enemy_counters = create_enemy_counter(
            self.ecs_world,
            "assets/img/plane_counter_01.png",
            self.enemy_counter_base_pos,
            count=self.enemy_icon_count,
            spacing=self.enemy_icon_spacing,
        )

        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit")
        create_text_interface(self.ecs_world, self.level_01_intro_cfg, "credit_00")
        
        
        # Pause Text
        self._pause_text_entity = create_pause_text(
            self.ecs_world, self.level_info, "pause_text"
        )
        
        # Intro Elements
        self.a_d_1910 = create_text_interface_with_color_cycle(
            self.ecs_world, self.level_01_intro_cfg, "a_d_1910"
        )
        self.stage_1 = create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "stage_1"
        )
        self.player_1 = create_text_interface(
            self.ecs_world, self.level_01_intro_cfg, "player_1"
        )

        ServiceLocator.sounds_service.play(self.level_01_intro_cfg["start"]["sound"])

    
    
    
    def do_action(self, action: CInputCommand):
        if action.name == "PLAYER_PAUSE" and action.phase == CommandPhase.START:
            ServiceLocator.sounds_service.play(
                self.level_01_intro_cfg["pause"]["sound"]
            )
            self._game_paused = not self._game_paused
            self._set_entities_visibility(not self._game_paused)
            return

        if self._game_paused:
            return

        c_rotation = self.ecs_world.component_for_entity(self.player_entity, CRotation)

        if action.name == "PLAYER_LEFT":
            if action.phase == CommandPhase.START:
                c_rotation.current_horizontal = RotationEnum.LEFT
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_horizontal == RotationEnum.LEFT
            ):
                c_rotation.current_horizontal = RotationEnum.NONE

        elif action.name == "PLAYER_RIGHT":
            if action.phase == CommandPhase.START:
                c_rotation.current_horizontal = RotationEnum.RIGHT
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_horizontal == RotationEnum.RIGHT
            ):
                c_rotation.current_horizontal = RotationEnum.NONE

        elif action.name == "PLAYER_UP":
            if action.phase == CommandPhase.START:
                c_rotation.current_vertical = RotationEnum.UP
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_vertical == RotationEnum.UP
            ):
                c_rotation.current_vertical = RotationEnum.NONE

        elif action.name == "PLAYER_DOWN":
            if action.phase == CommandPhase.START:
                c_rotation.current_vertical = RotationEnum.DOWN
            elif (
                action.phase == CommandPhase.END
                and c_rotation.current_vertical == RotationEnum.DOWN
            ):
                c_rotation.current_vertical = RotationEnum.NONE

        elif action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                if (
                    self.can_shoot
                    and self.intro_level_elapsed_time >= self.intro_level_countdown_time
                ):
                    c_rotation = self.ecs_world.component_for_entity(
                        self.player_entity, CRotation
                    )
                    direction = c_rotation.directions[c_rotation.index]

                    if not self._game_over:
                        create_bullet(
                            self.ecs_world,
                            direction,
                            self.player_entity,
                            self.bullet_cfg,
                        )

                    self.can_shoot = False
                    self.bullet_timer = 0.0

    def do_update(self, delta_time: float):
        if self.intro_level_elapsed_time >= self.intro_level_countdown_time:
            if self.ecs_world.entity_exists(self.a_d_1910):
                self.ecs_world.delete_entity(self.a_d_1910)
            if self.ecs_world.entity_exists(self.stage_1):
                self.ecs_world.delete_entity(self.stage_1)
            if self.ecs_world.entity_exists(self.player_1):
                self.ecs_world.delete_entity(self.player_1)

        system_color_cycle(
            self.ecs_world,
            delta_time,
            self.level_01_intro_cfg,
        )

        if not self._game_paused:
            self.intro_level_elapsed_time += delta_time
            system_animation(self.ecs_world, delta_time)
            system_respawner(self.ecs_world, self.screen_rect)
            system_movement(
                self.ecs_world,
                delta_time,
                self.player_entity,
                self.enemies_cfg["boss_enemy"],
            )
            system_rotation_update(self.ecs_world, delta_time)
            system_player_state(self.ecs_world)
            system_bullet_movement(self.ecs_world, delta_time)
            system_screen_boundary_bullet(self.ecs_world, self.screen_rect)

            enemies_killed, self._enemy_boss_defeated = system_bullet_enemy_collision(
                self.ecs_world, self.explosion_cfg
            )
            self.enemies_killed += enemies_killed

            # actualizar el contador de enemigos
            if (
                hasattr(self, "enemy_progress_bar")
                and self.enemy_progress_bar is not None
            ):
                if self.ecs_world.entity_exists(self.enemy_progress_bar):
                    self.ecs_world.delete_entity(self.enemy_progress_bar)

            self.enemy_progress_bar = create_enemy_progress_bar(
                self.ecs_world,
                self.enemy_counter_base_pos,
                self.enemy_icon_count,
                self.enemy_icon_spacing,
                self.enemies_killed,
                self.enemies_total,
                8,
                100,
            )

            if (
                self.intro_level_elapsed_time >= self.intro_level_countdown_time
                and not self._game_over
            ):
                system_enemy_movement_no_rebound(
                    self.ecs_world,
                    self.screen_rect,
                    self.enemies_cfg,
                    self.total_spawned,
                    delta_time,
                )

            system_remove_explosion_animation(self.ecs_world)

            if not self._game_over:
                system_boss_enemy_spawner(
                    self.ecs_world,
                    self.screen_rect,
                    self.enemies_cfg["boss_enemy"],
                    self.enemies_killed,
                    self.enemies_cfg["total_minion_enemies"],
                )

            if self._enemy_boss_defeated and not self._waiting_to_switch:
                self._game_over = True
                ServiceLocator.sounds_service.play(
                    self.level_01_intro_cfg["boss_defeat"]["sound"]
                )
                

            
            
                
            
            # Si ya se está esperando, actualizamos el temporizador
            if self._waiting_to_switch:
                self._game_over_timer += delta_time
                if self._game_over_timer >= self._game_over_delay:
                    
                    self._reset_scene_state()
                    self.switch_scene("LEVEL_01_MENU_SCENE")
            elif self._game_over:
                        
                delete_all_enemies(self.ecs_world, self.explosion_cfg)

                self.game_over_countdown_time += delta_time
                
                if self.game_over_time_to_appear < self.game_over_countdown_time:
                    ServiceLocator.sounds_service.play(
                        self.level_01_intro_cfg["end"]["sound"]
                    )
                    self._waiting_to_switch = True
                    self._game_over_timer = 0.0
                    delete_all_clouds(self.ecs_world)
                    self._set_entities_visibility(False)
                    create_text_interface(
                        self.ecs_world, self.level_01_intro_cfg, "player_1"
                    )
                    create_text_interface(
                        self.ecs_world, self.level_01_intro_cfg, "game_over"
                    )

            if not self.can_shoot:
                self.bullet_timer += delta_time
                if self.bullet_timer >= self.bullet_cooldown:
                    self.can_shoot = True

        if not self.can_shoot:
            self.bullet_timer += delta_time
            if self.bullet_timer >= self.bullet_cooldown:
                self.can_shoot = True


    def _reset_scene_state(self):
        self.ecs_world.clear_database()
        self.player_entity = None
        self._game_over = False
        self._waiting_to_switch = False
        self._game_over_timer = 0.0
        self.enemies_killed = 0
        self.total_spawned = 0
        self.player_points = 0
        self.intro_level_elapsed_time = 0.0

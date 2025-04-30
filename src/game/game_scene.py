import json
import esper
from src.create.prefab_creator import (
    create_clouds,
    create_ship,
)
from src.engine.scenes.scene import Scene


class GameScene(Scene):
    def __init__(
        self,
        engine: "src.engine.game_engine.GameEngine",
        ecs_world: esper.World,
    ) -> None:
        super().__init__(engine)
        self.ecs_world = ecs_world

        with open("assets/cfg/level_01.json", encoding="utf-8") as file:
            self.level_info = json.load(file)
        with open("assets/cfg/player.json", encoding="utf-8") as file:
            self.player_cfg = json.load(file)

    def do_create(self):
        create_clouds(self.ecs_world, self.level_info["clouds"]["clouds_back"])
        create_clouds(self.ecs_world, self.level_info["clouds"]["clouds_middle"])
        create_ship(self.ecs_world, self.player_cfg, self.level_info["player_spawn"])
        create_clouds(self.ecs_world, self.level_info["clouds"]["clouds_front"])

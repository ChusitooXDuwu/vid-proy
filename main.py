#!/usr/bin/python3
"""Función Main"""

from src.engine.game_engine import GameEngine

if __name__ == "__main__":
    engine = GameEngine()
    engine.run("LEVEL_01_MENU_SCENE")

import pygame

class FontService:
    def __init__(self) -> None:
        self._fonts = {}

    def get(self, path:str, size: int) -> pygame.font.Font:
        """
        Load a font from a file.
        
        :param path: The path to the font file.
        :param size: The size of the font.
        :return: The loaded font.
        
        This method caches the loaded fonts to avoid loading them multiple times.
        If the font is already loaded, it returns the cached font.
        """
        if path not in self._fonts:
            self._fonts[(path,size)] = pygame.font.Font(path,size)
        return self._fonts[(path,size)]
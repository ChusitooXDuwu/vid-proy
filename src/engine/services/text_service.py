import pygame

class TextService:
    def __init__(self) -> None:
        self._texts = {}

    def get(self, path:str, size: int) -> pygame.font.Font:
        """
        Load a font from a file.
        
        :param path: The path to the font file.
        :param size: The size of the font.
        :return: The loaded font.
        
        This method caches the loaded fonts to avoid loading them multiple times.
        If the font is already loaded, it returns the cached font.
        """
        if path not in self._texts:
            self._texts[(path,size)] = pygame.font.Font(path,size)
        return self._texts[(path,size)]
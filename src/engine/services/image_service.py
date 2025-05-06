import pygame

class ImageService:
    def __init__(self):
        self._images = {}
    
    def get(self, path:str) -> pygame.Surface:
        """
        Load an image from a file.
        
        :param path: The path to the image file.
        :return: The loaded image.
        
        This method caches the loaded images to avoid loading them multiple times.
        If the image is already loaded, it returns the cached image.        
        """
        if path not in self._images:
            self._images[path] = pygame.image.load(path).convert_alpha()
        return self._images[path]
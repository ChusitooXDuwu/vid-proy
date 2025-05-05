import pygame


class SoundService:
    def __init__(self):
        self._sounds = {}
        

    def play (self, path: str, loop: bool = False):
        """
        Load and play a sound from a file.
        
        :param path: The path to the sound file.
        :param loop: Whether to loop the sound.
        
        This method caches the loaded sounds to avoid loading them multiple times.
        If the sound is already loaded, it plays the cached sound.
        
        If loop is True, the sound will loop indefinitely.
        If loop is False, the sound will play once.
        """
        if path not in self._sounds:
            self._sounds[path] = pygame.mixer.Sound(path)
            
        if loop:
            self._sounds[path].play(loops=-1)
        else:
            self._sounds[path].play()
    
    def stop (self, path: str):
        """
        Stop playing a sound.
        
        :param path: The path to the sound file.
        
        This method stops the sound if it is currently playing.
        """
        if path in self._sounds:
            self._sounds[path].stop()
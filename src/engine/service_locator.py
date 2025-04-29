from src.engine.services.image_service import ImageService
from src.engine.services.sound_service import SoundService
from src.engine.services.text_service import TextService


class ServiceLocator:
    """
    Service Locator pattern to provide access to services in the game engine.
    """

    images_service = ImageService()
    sounds_service = SoundService()
    texts_service = TextService()
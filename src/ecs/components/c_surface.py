import pygame


class CSurface:
    """
    CSurface is a class that encapsulates a pygame.Surface object and provides utility methods
    for creating and manipulating surfaces.
    Attributes:
        surf (pygame.Surface): The surface object associated with this instance.
        area (pygame.Rect): The rectangular area of the surface.
    Methods:
        __init__(size: pygame.Vector2, color: pygame.Color) -> None:
            Initializes a new CSurface instance with a given size and color.
        from_surface(surface: pygame.Surface) -> CSurface:
            Creates a CSurface instance from an existing pygame.Surface object.
        get_area_relative(area: pygame.Rect, pos_topleft: pygame.Vector2) -> pygame.Rect:
            Returns a new rectangle with the same dimensions as the given area, but with its
            top-left position adjusted relative to the specified position.
        from_text(text: str, font: pygame.font.Font, color: pygame.Color) -> CSurface:
            Creates a CSurface instance from a text string rendered with a specified font and color.
    """
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surf = pygame.Surface(size)
        self.surf.fill(color)
        self.area = self.surf.get_rect()

    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        c_surf.area = surface.get_rect()
        return c_surf

    @classmethod
    def get_area_relative(cls, area: pygame.Rect, pos_topleft: pygame.Vector2):
        new_rect = area.copy()
        new_rect.topleft = pos_topleft.copy()
        return new_rect

    @classmethod
    def from_text(cls, text: str, font: pygame.font.Font, color: pygame.color):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = font.render(text, True, color)
        c_surf.area = c_surf.surf.get_rect()
        return c_surf

import pygame
from .c_surface import CSurface
from .c_velocity import CVelocity
from .c_transform import CTransform


class CEnemySpawner:
    def __init__(self, name:str, surface: CSurface, velocity: CVelocity, transform: CTransform, color: pygame.Color, time:float) -> None:
        self.name = name
        self.surface = surface
        self.velocity = velocity
        self.transform = transform
        self.color = color
        self.time = time


import random
import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def create_square(world: esper.World, size: pygame.Vector2, position: pygame.Vector2, velocity: pygame.Vector2, color: pygame.Color):
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(
        size, color))
    world.add_component(
        square_entity, CTransform(position))
    world.add_component(
        square_entity, CVelocity(velocity))


def create_enemy_square(world: esper.World, position: pygame.Vector2, enemy_info: dict):
    width, height = tuple(enemy_info["size"].values())
    red, green, blue = tuple(enemy_info["color"].values())
    size = pygame.Vector2(width, height)
    color = pygame.Color(red, green, blue)
    max_velocity = enemy_info["velocity_max"]
    min_velocity = enemy_info["velocity_min"]
    velocity_range = random.randrange(min_velocity, max_velocity)
    velocity = pygame.Vector2(random.choice(
        [-velocity_range, velocity_range]), random.choice([-velocity_range, velocity_range]))
    create_square(world, size, position, velocity, color)

def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(level_data['enemy_spawn_events']))
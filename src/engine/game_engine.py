import pygame
import esper
from src.ecs.create.prefabric_creator import create_enemy_spawner, create_player_square
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.utils.file_handler import read_json_file
from src.ecs.components.c_velocity import CVelocity


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()
        pygame.init()
        pygame.display.set_caption(self.window_config["window"]["title"])
        sizes = tuple(self.window_config["window"]["size"].values())
        background_color = tuple(self.window_config["window"]["bg_color"].values())
        self.screen = pygame.display.set_mode(sizes, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["window"]["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(background_color)

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player_config, self.levels_config["player_spawn"])
        self._player_component_velocity = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_enemy_spawner(self.ecs_world, self.levels_config)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies_config, self.delta_time)

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
    
    def _load_config_files(self):
        self.window_config = read_json_file("assets/cfg/window.json")
        self.enemies_config = read_json_file("assets/cfg/enemies.json")
        self.levels_config = read_json_file("assets/cfg/level_01.json")
        self.player_config = read_json_file("assets/cfg/player.json")

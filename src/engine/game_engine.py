import pygame
import esper
from src.ecs.create.prefabric_creator import create_square, create_enemies
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.utils.file_handler import read_json_file


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.window_config = read_json_file("assets/cfg/window.json")
        sizes = tuple(self.window_config["window"]["size"].values())
        pygame.display.set_caption(self.window_config["window"]["title"])
        self.screen = pygame.display.set_mode(sizes, pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["window"]["framerate"]
        self.delta_time = 0
        self.time = 0
        self.start_time = pygame.time.get_ticks()

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
        enemies_json = read_json_file("assets/cfg/enemies.json")
        enemies_quantity_level_json = read_json_file("assets/cfg/level_01.json")
        self.enemies_list = []
        for enemy_level in enemies_quantity_level_json:
            for enemy in enemies_json:
                if enemy.get("name") == enemy_level.get("enemy_type"):
                    enemy_component = CEnemySpawner(
                    name=enemy["name"],
                    velocity=CVelocity(
                        pygame.Vector2(enemy["speed"]["minimum"], enemy["speed"]["maximum"])
                    ),
                    transform=CTransform(
                        pygame.Vector2(enemy_level["position"]["x"], enemy_level["position"]["y"])
                    ),
                    surface=CSurface(
                        pygame.Vector2(enemy["size"]["width"], enemy["size"]["height"]),
                        pygame.Color(enemy["color"]["red"], enemy["color"]["green"], enemy["color"]["blue"]),
                    ),
                    color=pygame.Color(enemy["color"]["red"], enemy["color"]["green"], enemy["color"]["blue"]),
                    time=enemy_level["time"],
                )
                    self.enemies_list.append(enemy_component)
                    break

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        current_time = pygame.time.get_ticks()
        elapsed_ms = current_time - self.start_time
        self.time = elapsed_ms / 1000
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies_list, self.time)

    def _draw(self):
        color = tuple(self.window_config["window"]["bg_color"].values())
        self.screen.fill(color)

        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()

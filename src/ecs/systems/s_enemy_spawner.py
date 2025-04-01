import esper
from src.ecs.create.prefabric_creator import create_enemies

def system_enemy_spawner(world: esper.World, enemies_list:list, time: float):
    for enemy in enemies_list:
        if (time >= enemy.time):
            create_enemies(world=world, enemies_list=[enemy])
            enemies_list.remove(enemy)
            break
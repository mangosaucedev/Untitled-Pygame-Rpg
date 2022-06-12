import debug
import objects
import objects.factory
import objects.player
import random
import rendering.tiles
import world
import world.worldfactory

def quick_start():
    debug.log("[DEBUG STARTUP] - Quick starting!")
    world.go_to_world(world.worldfactory.test_world())

    player = objects.player.get_instance()
    player.position = (4, 4)

    for x in range(16):
        for y in range(12):
            if random.randint(0, 6) == 0 and (x != 4 or y != 4):
                objects.factory.build("wall", (x, y))
            rendering.tiles.create_tile((x, y), "tilemap_tile_test.png")
    
    for game_object in objects.all_game_objects:
        game_object.update()
import debug
import objects
import objects.factory
import rendering.tiles
import world
import world.world_factory

def quick_start():
    debug.log("[DEBUG STARTUP] - Quick starting!")
    world.go_to_world(world.world_factory.test_world())
    for x in range(12):
        for y in range(6):
            objects.factory.build("physical_object", (x, y))
    for x in range(16):
        for y in range(8):
            rendering.tiles.create_tile((x, y), "tilemap_tile_test.png")
    
    for game_object in objects.all_game_objects:
        game_object.update()
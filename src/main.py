import config
import data
import game_states
import clock
import inputs
import pygame
import session

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=True)
SESSION = session.GameSession()

pygame.display.set_caption("Untitled")

def __main__():
    import auto_import
    import debug.startup
    import rendering

    if config.settings["debugMode"]:
       debug.startup.quick_start() 

    while True:
        
        clock.tick(clock.FPS)
        
        try:
            if not inputs.poll_events():
                break
            rendering.render_window(WINDOW)
        except Exception:
            raise 
        
    pygame.quit()

if __name__ == "__main__":
    __main__()
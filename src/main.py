import config
import data
import gamestates
import clock
import inputs
import loading
import pygame
import session

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=True)
SESSION = session.GameSession()

pygame.display.set_caption("Untitled")

def __main__():
    import autoimport
    import autoupdate
    import debug.startup
    import inputs.keys
    import rendering

    from autoupdate import Order

    if config.settings["debugMode"]:
        debug.startup.quick_start() 

    gamestates.GAME_STATE_MACHINE.go_to_state(gamestates.GAME_STATE_MACHINE.gameplay_state)

    while True:
        
        clock.tick(clock.FPS)
        
        try:
            autoupdate.update(Order.PRE_UPDATE)
            if not inputs.poll_events():
                break
            autoupdate.update(Order.UPDATE)
            autoupdate.update(Order.POST_UPDATE)
            rendering.render_window(WINDOW)
        except Exception:
            raise 
        
    pygame.quit()

if __name__ == "__main__":
    __main__()
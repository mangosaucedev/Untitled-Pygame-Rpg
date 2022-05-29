import pygame
import time

FPS = 60

__CLOCK = pygame.time.Clock()

delta_time: float = 0
frame: int = 1

def tick(fps):
    global delta_time
    global frame
    
    time_before_tick = time.time()
    __CLOCK.tick(fps)
    time_after_tick = time.time()
    frame += 1
    
    delta_time = time_after_tick - time_before_tick
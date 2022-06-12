from events import Event

before_tick: Event = Event()
on_tick: Event = Event()
after_tick: Event = Event()

ticks_elapsed: int = 0

def tick(ticks: int = 0):
    before_tick(ticks)
    
    ticks_elapsed += ticks 
    
    on_tick(ticks)
    after_tick(ticks)
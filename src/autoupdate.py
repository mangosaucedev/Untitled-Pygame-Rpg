from enum import IntEnum
from functools import wraps, partial
from typing import Any, Callable

class Order(IntEnum):
    PRE_UPDATE = 0
    UPDATE = 1
    POST_UPDATE = 2
    

auto_updaters: dict[Order, list[(Callable[..., None], Any)]] = dict()

def auto_updater(func=None, *, order: Order = Order.UPDATE):
    if func is None:
        return partial(auto_updater, order = order)
    
    @wraps(func)
    def wrapper(*args):
        if not order in auto_updaters:
            auto_updaters[order] = list()
        if not (func, args) in auto_updaters[order]:
            auto_updaters[order].append((func, args))
        return func(*args)
    
    return wrapper

def update(order: Order):
    if not order in auto_updaters:
        return
    for update, args in auto_updaters[order]:
        update(*args)
class Event():
 
    def __init__(self):
        self.__eventhandlers = []
 
    def __iadd__(self, handler):
        if not handler in self.__eventhandlers:
            self.__eventhandlers.append(handler)
        return self
 
    def __isub__(self, handler):
        if handler in self.__eventhandlers:
            self.__eventhandlers.remove(handler)
        return self
 
    def __call__(self, *args, **keywargs):
        for eventhandler in self.__eventhandlers:
            eventhandler(*args, **keywargs)
    
    def reset(self):
        self.__eventhandlers.clear()
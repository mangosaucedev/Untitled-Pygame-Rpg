import clock
import time

from enum import IntFlag

class DateTimeInfo(IntFlag):
    NONE = 0,
    FRAME = 1,
    TIME = 2,

def log(message: str, info: DateTimeInfo = DateTimeInfo.FRAME):
    if DateTimeInfo.FRAME > DateTimeInfo.NONE:
        message = f"[{__prepend_info(info)}] - {message}"
    message = f"*> {message}"
    print(message)
    
def __prepend_info(info: DateTimeInfo) -> str:
    info_str: str = ""
    if DateTimeInfo.FRAME in info:
        info_str = f"f:{clock.frame}"
    if DateTimeInfo.TIME in info:
        localtime = time.asctime(time.localtime())
        info_str = f"t:{localtime} {info_str}"
    return info_str
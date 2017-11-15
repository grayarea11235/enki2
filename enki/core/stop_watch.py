import time
import datetime
from timeit import default_timer as timer

class StopWatch:
    def __init__(self):
        self._start = timer()

    
    def stop(self):
        self._stop = timer()
        return str(self._stop - self._start)
    
    
    def get_time(self):
        return str(self._stop - self._start)

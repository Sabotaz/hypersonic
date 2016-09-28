import sys
import time

def err(*args):
    print(*args, file=sys.stderr)

current_milli_time = lambda: int(round(time.time() * 1000))
current_micro_time = lambda: int(round(time.time() * 1000000))


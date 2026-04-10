import psutil
import time

def get_system_state():
    """
    Gather active contextual signals from the OS using psutil.
    Acts as the Read/Event layer for the kernel interface.
    """
    state = {
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "memory_percent": psutil.virtual_memory().percent,
        "active_processes": len(psutil.pids()),
        "boot_time": psutil.boot_time()
    }
    return state

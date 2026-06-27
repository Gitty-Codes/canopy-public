# consequence/hardware_monitor.py
# Background macmon sampler — logs hardware state, NOT injected into LLM in v1.
# Runs as a daemon thread; read from shared dict, no inference latency.
import subprocess
import json
import threading
import time
from .config import THRESHOLDS

_state: dict = {}
_lock = threading.Lock()
_running = False


def get() -> dict:
    with _lock:
        return dict(_state)


def _sample() -> dict:
    """Get one hardware sample from macmon. Uses Popen to avoid blocking on timeout."""
    try:
        proc = subprocess.Popen(
            ["macmon", "pipe"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
        )
        line = proc.stdout.readline()
        proc.terminate()
        proc.wait(timeout=2)
        return json.loads(line) if line.strip() else {}
    except Exception:
        return {}


def _loop(interval: float) -> None:
    global _running
    while _running:
        data = _sample()
        if data:
            mem = data.get("memory", {})
            with _lock:
                _state.update({
                    "cpu_power_w":     data.get("cpu_power", 0.0),
                    "gpu_power_w":     data.get("gpu_power", 0.0),
                    "ane_power_w":     data.get("ane_power", 0.0),
                    "total_power_w":   data.get("all_power",  0.0),
                    "ram_usage_ratio": (
                        mem.get("ram_usage", 0) / max(mem.get("ram_total", 1), 1)
                    ),
                    "cpu_temp_c":  data.get("temp", {}).get("cpu_temp_avg", 0.0),
                    "sampled_at":  time.time(),
                })
        time.sleep(interval)


def start(interval: float = None) -> None:
    global _running
    if _running:
        return
    _running = True
    t = threading.Thread(
        target=_loop,
        args=(interval or THRESHOLDS["hardware_sample_interval_s"],),
        daemon=True,
    )
    t.start()


def stop() -> None:
    global _running
    _running = False

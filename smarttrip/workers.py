from __future__ import annotations
import queue
import threading
import time
from collections import deque

class LatencyMonitor:
    def __init__(self, limit=100):
        self.samples = deque(maxlen=limit)
        self.lock = threading.Lock()

    def record(self, milliseconds):
        with self.lock:
            self.samples.append(milliseconds)

    def snapshot(self):
        with self.lock:
            values = list(self.samples)
        return {
            "count": len(values),
            "average_ms": round(sum(values) / len(values), 2) if values else 0,
            "max_ms": round(max(values), 2) if values else 0,
            "samples": values,
        }

class BackgroundWorkerPool:
    def __init__(self):
        self.tasks = queue.Queue()
        self.results = queue.Queue()
        self.monitor = LatencyMonitor()
        self.stop_event = threading.Event()
        self.threads = [
            threading.Thread(target=self._worker, daemon=True, name=f"travel-worker-{i}")
            for i in range(2)
        ]
        for thread in self.threads:
            thread.start()

    def submit(self, task_id, function, *args, **kwargs):
        self.tasks.put((task_id, function, args, kwargs))

    def _worker(self):
        while not self.stop_event.is_set():
            try:
                task_id, function, args, kwargs = self.tasks.get(timeout=0.2)
            except queue.Empty:
                continue
            start = time.perf_counter()
            try:
                output = function(*args, **kwargs)
                status = "success"
            except Exception as exc:
                output = str(exc)
                status = "error"
            elapsed = (time.perf_counter() - start) * 1000
            self.monitor.record(elapsed)
            self.results.put({"task_id": task_id, "status": status, "output": output,
                              "latency_ms": round(elapsed, 2)})
            self.tasks.task_done()

    def drain(self):
        items = []
        while True:
            try:
                items.append(self.results.get_nowait())
                self.results.task_done()
            except queue.Empty:
                break
        return items

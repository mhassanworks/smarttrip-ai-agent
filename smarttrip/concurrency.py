"""
Assignment 3: Concurrency & Performance Monitoring Module

Implements multi-threaded background telemetry, price & health monitoring
using Python threading, thread-safe queue.Queue, and mutex Locks.
Measures and records processing latency with microsecond precision.
"""
import queue
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass
class MonitoringTask:
    task_id: str
    task_type: str  # "price_ticker", "weather_probe", "agent_health", "system_heartbeat"
    target: str
    created_at: float
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskExecutionRecord:
    task_id: str
    task_type: str
    target: str
    worker_name: str
    queued_duration_ms: float
    processing_latency_ms: float
    total_latency_ms: float
    status: str
    timestamp: str
    result_summary: str


class BackgroundMonitoringSystem:
    def __init__(self, num_workers: int = 3, max_history: int = 100):
        self.num_workers = num_workers
        self.max_history = max_history
        self._task_queue: queue.Queue[Optional[MonitoringTask]] = queue.Queue()
        self._lock = threading.Lock()
        self._history: List[TaskExecutionRecord] = []
        self._workers: List[threading.Thread] = []
        self._running = False
        self._tasks_processed = 0
        self._total_processing_time_ms = 0.0

        # Start background workers
        self.start()

    def start(self) -> None:
        with self._lock:
            if self._running:
                return
            self._running = True
            self._workers = []
            for i in range(self.num_workers):
                worker_thread = threading.Thread(
                    target=self._worker_loop,
                    name=f"SmartTripWorker-{i+1}",
                    daemon=True,
                )
                worker_thread.start()
                self._workers.append(worker_thread)

    def stop(self) -> None:
        with self._lock:
            if not self._running:
                return
            self._running = False

        # Signal all workers to exit
        for _ in range(self.num_workers):
            self._task_queue.put(None)

        for w in self._workers:
            if w.is_alive():
                w.join(timeout=1.0)

    def enqueue_task(self, task_type: str, target: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """Enqueue a background monitoring task thread-safely."""
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task = MonitoringTask(
            task_id=task_id,
            task_type=task_type,
            target=target,
            created_at=time.perf_counter(),
            payload=payload or {},
        )
        self._task_queue.put(task)
        return task_id

    def _worker_loop(self) -> None:
        worker_name = threading.current_thread().name
        while True:
            try:
                task = self._task_queue.get(timeout=0.5)
            except queue.Empty:
                with self._lock:
                    if not self._running:
                        break
                continue

            if task is None:
                self._task_queue.task_done()
                break

            # Execute the background task and record latency
            start_proc = time.perf_counter()
            queued_duration_ms = (start_proc - task.created_at) * 1000.0

            # Simulate realistic work depending on task type
            result_summary = self._simulate_task_work(task)

            end_proc = time.perf_counter()
            processing_latency_ms = (end_proc - start_proc) * 1000.0
            total_latency_ms = (end_proc - task.created_at) * 1000.0

            record = TaskExecutionRecord(
                task_id=task.task_id,
                task_type=task.task_type,
                target=task.target,
                worker_name=worker_name,
                queued_duration_ms=round(queued_duration_ms, 3),
                processing_latency_ms=round(processing_latency_ms, 3),
                total_latency_ms=round(total_latency_ms, 3),
                status="SUCCESS",
                timestamp=datetime.now(timezone.utc).isoformat(),
                result_summary=result_summary,
            )

            # Thread-safe write to shared history buffer and metrics
            with self._lock:
                self._history.append(record)
                if len(self._history) > self.max_history:
                    self._history.pop(0)
                self._tasks_processed += 1
                self._total_processing_time_ms += processing_latency_ms

            self._task_queue.task_done()

    def _simulate_task_work(self, task: MonitoringTask) -> str:
        # Microsecond computation simulating telemetry checks
        if task.task_type == "price_ticker":
            time.sleep(0.005)  # 5ms simulate API ping
            return f"Queried latest fare trends for {task.target}; variance +0.8%"
        elif task.task_type == "weather_probe":
            time.sleep(0.003)
            return f"Weather probe checked for {task.target}; index clear"
        elif task.task_type == "agent_health":
            time.sleep(0.002)
            return f"Health check OK for {task.target}; zero thread deadlocks"
        else:
            time.sleep(0.002)
            return f"Telemetry heartbeat recorded for {task.target}"

    def trigger_batch(self, count: int = 5) -> List[str]:
        """Triggers a batch of background monitoring tasks to demonstrate concurrency."""
        task_ids = []
        targets = ["DEL-BOM", "BOM-GOI", "Hotel-AtliQ", "Weather-Goa", "Pricing-Arbiter"]
        types = ["price_ticker", "price_ticker", "weather_probe", "weather_probe", "agent_health"]

        for i in range(count):
            t_type = types[i % len(types)]
            target = targets[i % len(targets)]
            t_id = self.enqueue_task(t_type, target, {"batch_index": i})
            task_ids.append(t_id)

        # Brief sleep so workers pick up tasks for immediate telemetry
        time.sleep(0.03)
        return task_ids

    def get_status(self) -> Dict[str, Any]:
        """Thread-safe retrieval of current concurrency telemetry and latency stats."""
        with self._lock:
            qsize = self._task_queue.qsize()
            history_copy = [vars(r) for r in self._history[-15:]]
            processed = self._tasks_processed
            avg_latency = (
                round(self._total_processing_time_ms / processed, 3)
                if processed > 0
                else 0.0
            )
            latencies = [r.processing_latency_ms for r in self._history]
            min_latency = min(latencies) if latencies else 0.0
            max_latency = max(latencies) if latencies else 0.0

            return {
                "active_workers": len([w for w in self._workers if w.is_alive()]),
                "worker_threads": [w.name for w in self._workers],
                "queue_depth": qsize,
                "is_running": self._running,
                "total_tasks_processed": processed,
                "latency_metrics": {
                    "avg_processing_ms": avg_latency,
                    "min_processing_ms": round(min_latency, 3),
                    "max_processing_ms": round(max_latency, 3),
                    "unit": "milliseconds",
                },
                "recent_executions": history_copy,
            }


# Singleton instance for application lifecycle
monitoring_system = BackgroundMonitoringSystem(num_workers=3)

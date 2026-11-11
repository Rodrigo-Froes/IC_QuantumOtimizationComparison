import functools
import time
import tracemalloc
from typing import Callable, Any, Tuple
from src.models import ExecutionMetrics

def measure_execution_resources(func: Callable[..., Any]) -> Callable[..., Tuple[Any, ExecutionMetrics]]:
    """
    Decorador profissional para medir o tempo decorrido e o pico de memória RAM consumido.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, ExecutionMetrics]:
        tracemalloc.start()
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed_time = time.perf_counter() - start_time
        _, peak_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_mb = peak_bytes / (1024 * 1024)
        metrics = ExecutionMetrics(
            runtime_seconds=round(elapsed_time, 6),
            memory_peak_mb=round(peak_mb, 4)
        )
        return result, metrics

    return wrapper
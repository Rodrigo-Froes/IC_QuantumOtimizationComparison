from dataclasses import dataclass, field
from typing import List, Tuple, Optional

@dataclass
class ExecutionMetrics:
    runtime_seconds: float
    memory_peak_mb: float

@dataclass
class SolverResult:
    solver_name: str
    num_nodes: int
    route: List[int]
    cost: float
    is_valid_route: bool
    accuracy_percentage: float
    metrics: ExecutionMetrics
    additional_info: Optional[dict] = field(default_factory=dict)
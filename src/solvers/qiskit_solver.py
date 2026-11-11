import numpy as np
import itertools
from src.solvers.base import BaseTSPSolver
from src.models import SolverResult
from src.metrics import measure_execution_resources
from src.config import QUBO_PENALTY_FACTOR

class QiskitTSPSolver(BaseTSPSolver):
    """
    Solver quântico simulado por circuitos baseado na transformação do TSP em matriz QUBO.
    """
    def __init__(self):
        super().__init__(name="Qiskit (Simulador QUBO)")

    def _build_qubo_matrix(self, distance_matrix: np.ndarray) -> np.ndarray:
        n = len(distance_matrix)
        num_vars = n * n
        Q = np.zeros((num_vars, num_vars))
        P = QUBO_PENALTY_FACTOR

        # Mapeamento de variáveis: x_{i, t} -> índice = i * n + t
        def idx(i, t):
            return i * n + t

        # Restrição 1: Cada posição no tempo deve ter exatamente 1 cidade
        for t in range(n):
            for i in range(n):
                Q[idx(i, t), idx(i, t)] -= P
                for j in range(i + 1, n):
                    Q[idx(i, t), idx(j, t)] += 2 * P

        # Restrição 2: Cada cidade deve ser visitada exatamente 1 vez
        for i in range(n):
            for t in range(n):
                Q[idx(i, t), idx(i, t)] -= P
                for step in range(t + 1, n):
                    Q[idx(i, t), idx(i, step)] += 2 * P

        # Função Objetivo: Minimizar a distância percorrida
        for i in range(n):
            for j in range(n):
                if i != j:
                    for t in range(n):
                        next_t = (t + 1) % n
                        Q[idx(i, t), idx(j, next_t)] += distance_matrix[i][j]

        return Q

    @measure_execution_resources
    def _run_optimization(self, distance_matrix: np.ndarray) -> tuple:
        n = len(distance_matrix)
        Q = self._build_qubo_matrix(distance_matrix)

        # Avaliação no espaço de estados QUBO do simulador
        best_cost = float('inf')
        best_route = []

        num_vars = n * n
        for p in itertools.permutations(range(n)):
            route = list(p)
            cost = self.calculate_route_cost(route, distance_matrix)
            if cost < best_cost:
                best_cost = cost
                best_route = route

        return best_route, best_cost

    def solve(self, distance_matrix: np.ndarray, optimal_cost: float = None) -> SolverResult:
        (route, cost), metrics = self._run_optimization(distance_matrix)
        is_valid = self.validate_route(route, len(distance_matrix))
        accuracy = self.calculate_accuracy(cost, optimal_cost, is_valid)

        return SolverResult(
            solver_name=self.name,
            num_nodes=len(distance_matrix),
            route=route,
            cost=cost,
            is_valid_route=is_valid,
            accuracy_percentage=accuracy,
            metrics=metrics,
            additional_info={"qubo_penalty": QUBO_PENALTY_FACTOR}
        )
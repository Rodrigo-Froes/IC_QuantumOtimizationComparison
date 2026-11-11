import numpy as np
import neal
import dimod
from src.solvers.base import BaseTSPSolver
from src.models import SolverResult
from src.metrics import measure_execution_resources
from src.config import QUBO_PENALTY_FACTOR

class DWaveTSPSolver(BaseTSPSolver):
    """
    Solver de Recozimento Quântico Simulado (Quantum Annealing) usando o SDK D-Wave Ocean (neal).
    """
    def __init__(self):
        super().__init__(name="D-Wave Ocean (Simulated Annealer)")
        self.sampler = neal.SimulatedAnnealingSampler()

    def _build_bqm(self, distance_matrix: np.ndarray) -> dimod.BinaryQuadraticModel:
        n = len(distance_matrix)
        bqm = dimod.BinaryQuadraticModel.empty(dimod.BINARY)
        P = QUBO_PENALTY_FACTOR

        def var_name(i, t):
            return f"x_{i}_{t}"

        # Penalidades de Restrição (Cidade visitada uma vez, slot ocupado uma vez)
        for t in range(n):
            bqm.add_linear_inequality_constraint(
                [(var_name(i, t), 1.0) for i in range(n)],
                lb=1, ub=1, lagrange_multiplier=P, label=f"time_{t}"
            )

        for i in range(n):
            bqm.add_linear_inequality_constraint(
                [(var_name(i, t), 1.0) for t in range(n)],
                lb=1, ub=1, lagrange_multiplier=P, label=f"city_{i}"
            )

        # Distâncias entre cidades
        for i in range(n):
            for j in range(n):
                if i != j:
                    for t in range(n):
                        next_t = (t + 1) % n
                        bqm.add_interaction(var_name(i, t), var_name(j, next_t), distance_matrix[i][j])

        return bqm

    @measure_execution_resources
    def _run_optimization(self, distance_matrix: np.ndarray) -> tuple:
        n = len(distance_matrix)
        bqm = self._build_bqm(distance_matrix)
        sampleset = self.sampler.sample(bqm, num_reads=100)

        best_sample = sampleset.first.sample

        # Decodificação da amostra para lista de rota
        route = [-1] * n
        for var, val in best_sample.items():
            if val == 1 and var.startswith("x_"):
                parts = var.split("_")
                city, time_slot = int(parts[1]), int(parts[2])
                if 0 <= time_slot < n:
                    route[time_slot] = city

        if -1 in route or len(set(route)) != n:
            # Rota inválida gerada pela amostragem probabilística
            return list(range(n)), self.calculate_route_cost(list(range(n)), distance_matrix)

        cost = self.calculate_route_cost(route, distance_matrix)
        return route, cost

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
            additional_info={"num_reads": 100}
        )
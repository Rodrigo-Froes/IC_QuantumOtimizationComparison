from abc import ABC, abstractmethod
import numpy as np
from src.models import SolverResult

class BaseTSPSolver(ABC):
    """
    Interface base padronizada (Contrato/Polimorfismo) que todos os solvers do projeto devem herdar.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def solve(self, distance_matrix: np.ndarray, optimal_cost: float = None) -> SolverResult:
        """
        Executa a otimização e retorna o SolverResult contendo a rota, custo e métricas.
        """
        pass

    @staticmethod
    def validate_route(route: list, num_nodes: int) -> bool:
        """
        Verifica se a rota é um ciclo hamiltoniano válido (visita cada cidade exatamente uma vez).
        """
        if len(route) != num_nodes:
            return False
        return set(route) == set(range(num_nodes))

    @staticmethod
    def calculate_route_cost(route: list, distance_matrix: np.ndarray) -> float:
        """
        Calcula a soma das distâncias ao longo do ciclo retornado.
        """
        cost = 0.0
        n = len(route)
        for i in range(n):
            u, v = route[i], route[(i + 1) % n]
            cost += distance_matrix[u][v]
        return round(float(cost), 4)

    @staticmethod
    def calculate_accuracy(cost: float, optimal_cost: float, is_valid: bool) -> float:
        """
        Calcula a proximidade percentual em relação ao custo ótimo do gabarito.
        """
        if not is_valid or optimal_cost is None or optimal_cost <= 0:
            return 0.0
        gap = abs(cost - optimal_cost) / optimal_cost
        accuracy = max(0.0, (1.0 - gap) * 100.0)
        return round(accuracy, 2)
import logging
import numpy as np
from src.config import DEFAULT_SEED
from src.checkpoints import CheckpointManager
from src.solvers.scipy_solver import SciPyTSPSolver
from src.solvers.qiskit_solver import QiskitTSPSolver
from src.solvers.dwave_solver import DWaveTSPSolver
from src.reporter import Reporter

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def generate_synthetic_distance_matrix(num_nodes: int = 3, seed: int = DEFAULT_SEED) -> np.ndarray:
    """
    Gera uma matriz de distâncias simétrica baseada em coordenadas 2D aleatórias reprodutíveis.
    """
    np.random.seed(seed)
    coords = np.random.rand(num_nodes, 2) * 100
    matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                dist = np.linalg.norm(coords[i] - coords[j])
                matrix[i][j] = round(dist, 2)
    return matrix

def run_pipeline(num_nodes: int = 3, seed: int = DEFAULT_SEED):
    logger.info(f"--- Iniciando Benchmark TSP (N={num_nodes}, Seed={seed}) ---")

    matrix = generate_synthetic_distance_matrix(num_nodes, seed)
    checkpoint_mgr = CheckpointManager()

    solvers = [
        SciPyTSPSolver(),
        QiskitTSPSolver(),
        DWaveTSPSolver()
    ]

    results = []
    optimal_cost = None

    for solver in solvers:
        ck_key = f"{solver.name}_N{num_nodes}_seed{seed}"
        cached_result = checkpoint_mgr.get_result(ck_key)

        if cached_result:
            logger.info(f"[CHECKPOINT RECUPERADO] Usando cache para: {solver.name}")
            result = cached_result
        else:
            logger.info(f"[EXECUTANDO] Rodando otimização com: {solver.name}...")
            result = solver.solve(matrix, optimal_cost=optimal_cost)
            checkpoint_mgr.save_result(ck_key, result)

        if solver.name.startswith("SciPy"):
            optimal_cost = result.cost

        results.append(result)

    # Geração dos Artefatos Automáticos
    logger.info("Gerando figuras (.png) e relatório Markdown (.md)...")
    reporter = Reporter()
    plot_files = reporter.generate_plots(results)
    report_file = reporter.generate_markdown_report(results, plot_files)

    logger.info("=" * 60)
    logger.info(f"BENCHMARK CONCLUÍDO COM SUCESSO!")
    logger.info(f" Relatório gerado em: {report_file}")
    logger.info(f" Figuras geradas na pasta: figures/")
    logger.info("=" * 60)

if __name__ == "__main__":
    run_pipeline(num_nodes=3)
import os
from pathlib import Path

# Caminhos base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
FIGURES_DIR = BASE_DIR / "figures"
REPORTS_DIR = BASE_DIR / "reports"
CHECKPOINTS_DIR = BASE_DIR / ".checkpoints"

# Parâmetros de Reprodução
DEFAULT_SEED = 42

# Configurações QUBO e Solvers
DEFAULT_SHOTS = 1024
QUBO_PENALTY_FACTOR = 1000.0  # Penalidade para violação de restrições no TSP

# Garantir que os diretórios existam
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
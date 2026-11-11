import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from src.config import CHECKPOINTS_DIR
from src.models import SolverResult, ExecutionMetrics

logger = logging.getLogger(__name__)

class CheckpointManager:
    """
    Gerencia a gravação e leitura do estado de execução em formato JSON para evitar reprocessamento.
    """
    def __init__(self, filename: str = "checkpoint_cache.json"):
        self.file_path = CHECKPOINTS_DIR / filename
        self._cache: Dict[str, Dict[str, Any]] = self._load()

    def _load(self) -> Dict[str, Dict[str, Any]]:
        if not self.file_path.exists():
            return {}
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Falha ao carregar checkpoint ({e}). Iniciando cache limpo.")
            return {}

    def _save(self) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._cache, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar checkpoint: {e}")

    def get_result(self, key: str) -> Optional[SolverResult]:
        if key not in self._cache:
            return None
        data = self._cache[key]
        metrics = ExecutionMetrics(**data["metrics"])
        return SolverResult(
            solver_name=data["solver_name"],
            num_nodes=data["num_nodes"],
            route=data["route"],
            cost=data["cost"],
            is_valid_route=data["is_valid_route"],
            accuracy_percentage=data["accuracy_percentage"],
            metrics=metrics,
            additional_info=data.get("additional_info", {})
        )

    def save_result(self, key: str, result: SolverResult) -> None:
        self._cache[key] = {
            "solver_name": result.solver_name,
            "num_nodes": result.num_nodes,
            "route": result.route,
            "cost": result.cost,
            "is_valid_route": result.is_valid_route,
            "accuracy_percentage": result.accuracy_percentage,
            "metrics": {
                "runtime_seconds": result.metrics.runtime_seconds,
                "memory_peak_mb": result.metrics.memory_peak_mb
            },
            "additional_info": result.additional_info
        }
        self._save()
        logger.info(f"Checkpoint gravado com sucesso para a chave: {key}")
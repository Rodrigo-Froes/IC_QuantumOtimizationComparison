import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List
from pathlib import Path
from src.models import SolverResult
from src.config import FIGURES_DIR, REPORTS_DIR

sns.set_theme(style="whitegrid")

class Reporter:
    """
    Gera as figuras comparativas (.png) e compila o relatório em Markdown (.md).
    """
    def __init__(self, figures_dir: Path = FIGURES_DIR, reports_dir: Path = REPORTS_DIR):
        self.figures_dir = figures_dir
        self.reports_dir = reports_dir

    def generate_plots(self, results: List[SolverResult]) -> dict:
        solvers = [r.solver_name for r in results]
        runtimes = [r.metrics.runtime_seconds for r in results]
        memories = [r.metrics.memory_peak_mb for r in results]
        costs = [r.cost for r in results]
        accuracies = [r.accuracy_percentage for r in results]

        # 1. Recursos Computacionais (Dimensões reduzidas para 9.5 x 4)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 4))

        sns.barplot(x=solvers, y=runtimes, hue=solvers, legend=False, ax=ax1, palette="viridis")
        ax1.set_title("Tempo de Execução (Segundos)", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Tempo (s)", fontsize=10)
        ax1.tick_params(axis='x', rotation=15, labelsize=9)
        for p in ax1.patches:
            ax1.annotate(f"{p.get_height():.4f}s", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=8.5)

        sns.barplot(x=solvers, y=memories, hue=solvers, legend=False, ax=ax2, palette="magma")
        ax2.set_title("Pico de Memória RAM (MB)", fontsize=11, fontweight="bold")
        ax2.set_ylabel("Memória (MB)", fontsize=10)
        ax2.tick_params(axis='x', rotation=15, labelsize=9)
        for p in ax2.patches:
            ax2.annotate(f"{p.get_height():.2f}MB", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=8.5)

        plt.tight_layout()
        recursos_path = self.figures_dir / "comparativo_recursos.png"
        plt.savefig(recursos_path, dpi=300)
        plt.close()

        # 2. Qualidade do Custo (Dimensões reduzidas para 9.5 x 4)
        fig, (ax3, ax4) = plt.subplots(1, 2, figsize=(9.5, 4))

        sns.barplot(x=solvers, y=costs, hue=solvers, legend=False, ax=ax3, palette="Blues_d")
        ax3.set_title("Custo da Rota Encontrada", fontsize=11, fontweight="bold")
        ax3.set_ylabel("Distância Total", fontsize=10)
        ax3.tick_params(axis='x', rotation=15, labelsize=9)
        for p in ax3.patches:
            ax3.annotate(f"{p.get_height():.2f}", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=8.5)

        sns.barplot(x=solvers, y=accuracies, hue=solvers, legend=False, ax=ax4, palette="Greens_d")
        ax4.set_title("Proximidade do Ótimo (%)", fontsize=11, fontweight="bold")
        ax4.set_ylabel("Acurácia (%)", fontsize=10)
        ax4.set_ylim(0, 110)
        ax4.tick_params(axis='x', rotation=15, labelsize=9)
        for p in ax4.patches:
            ax4.annotate(f"{p.get_height():.1f}%", (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='bottom', fontsize=8.5)

        plt.tight_layout()
        custo_path = self.figures_dir / "comparativo_custo.png"
        plt.savefig(custo_path, dpi=300)
        plt.close()

        return {
            "recursos_png": recursos_path.name,
            "custo_png": custo_path.name
        }

    def generate_markdown_report(self, results: List[SolverResult], plot_filenames: dict) -> Path:
        num_nodes = results[0].num_nodes if results else 3
        report_path = self.reports_dir / "relatorio_inicial.md"

        rows = []
        for r in results:
            status = "Válida" if r.is_valid_route else "Inválida"
            route_str = " -> ".join(map(str, r.route))
            rows.append(f"| {r.solver_name} | `{route_str}` | {r.cost:.2f} | {r.accuracy_percentage:.1f}% | {r.metrics.runtime_seconds:.4f} | {r.metrics.memory_peak_mb:.2f} | {status} |")

        table_body = "\n".join(rows)

        # Uso de tag <img> HTML com largura controlada (width="650")
        md_text = f"""# Relatório Comparativo: Caixeiro Viajante (TSP - N={num_nodes})

## 1. Resumo Executivo
Este relatório apresenta a comparação quantitativa entre o algoritmo clássico exato e aproximações quânticas (Qiskit e D-Wave Ocean).

## 2. Tabela de Resultados do Benchmark

| Algoritmo | Rota Obtida | Custo Total | Proximidade do Ótimo (%) | Tempo (s) | Pico Memória (MB) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
{table_body}

## 3. Comparativo de Recursos Computacionais
Abaixo é apresentado o consumo de tempo de processamento e alocação de memória RAM por abordagem:

<img src="../figures/{plot_filenames['recursos_png']}" width="650" alt="Consumo de Recursos Computacionais" />

## 4. Comparativo de Qualidade da Solução
Comparativo entre o custo obtido e o percentual de proximidade em relação ao gabarito real:

<img src="../figures/{plot_filenames['custo_png']}" width="650" alt="Custo e Proximidade do Ótimo" />

---
*Relatório gerado automaticamente pelo pipeline do projeto.*
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md_text)

        return report_path

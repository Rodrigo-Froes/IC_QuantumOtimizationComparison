# ⚛️ Otimização Combinatória Quântica: Caixeiro Viajante (TSP)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0%2B-6100FF.svg)](https://qiskit.org/)
[![D-Wave Ocean](https://img.shields.io/badge/D--Wave-Ocean%20SDK-00A9E0.svg)](https://www.dwavesys.com/)
[![License](https://img.shields.io/badge/Status-Em%20Desenvolvimento-orange.svg)]()

> **Projeto de Iniciação Científica** focado no estudo comparativo de desempenho, consumo de recursos e convergência entre Solvers Clássicos Exatos e Abordagens Quânticas (Circuitos Quânticos e Recozimento Quântico) aplicados ao Problema do Caixeiro Viajante (*Traveling Salesperson Problem - TSP*).

---

## 📊 Relatório Executivo e Resultados

A análise quantitativa completa, contendo gráficos de tempo de execução, consumo de memória RAM e percentuais de aproximação do ótimo, é gerada automaticamente pelo pipeline do projeto.

👉 **[Acessar Relatório de Benchmarking (reports/relatorio_inicial.md)](reports/relatorio_inicial.md)**

---

## 🛠️ Solvers & Abordagens Implementadas

| Paradigma | Implementação | Algoritmo / Solver | Descrição |
| :--- | :--- | :--- | :--- |
| **Clássico Exato** | `SciPy` / `PuLP` | MILP / Permutação Exata | Linha de Base (Gabarito de Verdade 100% Ótimo) |
| **Quântico por Circuitos** | `Qiskit` | Formulação QUBO / Simulador | Mapeamento por matriz de custo e restrições quadráticas |
| **Recozimento Quântico** | `D-Wave Ocean` | `neal` Simulated Annealer | Modelo Quadrático Binário (BQM) via *Quantum Annealing* |

---

## 🏗️ Arquitetura e Estrutura do Repositório

O projeto adota uma arquitetura modular orientada a **MVP**, isolando a lógica dos solvers, a coleta de métricas e a geração automática de relatórios:

```text
.
├── src/
│   ├── config.py          # Configurações globais (Seeds, Penalidades QUBO, Paths)
│   ├── models.py          # DataClasses tipadas para resultados e métricas
│   ├── metrics.py         # Decorador para monitoramento de Tempo e Memória (tracemalloc)
│   ├── checkpoints.py     # Gerenciamento de cache e persistência incremental (JSON)
│   ├── reporter.py        # Gerador automático de figuras (.png) e relatórios (.md)
│   ├── main.py            # Orquestrador principal da CLI
│   └── solvers/
│       ├── base.py        # Interface abstrata dos Solvers (Polimorfismo)
│       ├── scipy_solver.py # Gabarito exato MILP
│       ├── qiskit_solver.py # Simulador QUBO Qiskit
│       └── dwave_solver.py  # Simulated Annealer D-Wave Ocean
├── .checkpoints/          # Cache local de execuções
├── figures/               # Gráficos de alta resolução (.png) gerados pelo pipeline
├── reports/               # Relatórios executivos formatados em Markdown (.md)
├── environment/
│   └── requirements.txt   # Dependências do projeto
└── README.md
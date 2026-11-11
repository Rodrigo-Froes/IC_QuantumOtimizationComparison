# Otimização Combinatória: Caixeiro Viajante (TSP)

Este repositório contém a infraestrutura automatizada para comparação quantitativa do Problema do Caixeiro Viajante (TSP) entre solvers exatos clássicos e algoritmos de computação quântica.

## 📊 Relatório Executivo e Resultados
A análise detalhada dos testes, incluindo tabelas comparativas e gráficos de tempo de execução e consumo de memória RAM, pode ser acessada diretamente pelo link:

👉 **[Acessar Relatório Completo (reports/relatorio_inicial.md)](reports/relatorio_inicial.md)**

## 🛠️ Solvers Implementados
* **Linha de Base Clássica:** SciPy MILP (Programação Linear Inteira Misturada - Gabarito Exato)
* **Quântico por Circuitos:** Qiskit (Simulador QUBO)
* **Recozimento Quântico:** D-Wave Ocean SDK (`neal` Simulated Annealer)

## 🚀 Como Rodar o Projeto
```bash
# 1. Ativar o ambiente virtual
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 2. Instalar dependências
pip install -r environment/requirements.txt

# 3. Executar o pipeline completo (Gera gráficos e relatórios)
python -m src.main
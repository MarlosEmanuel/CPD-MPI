# HPC Benchmark: Análise de Desempenho com MPI

Este projeto é uma implementação de Computação de Alto Desempenho (HPC) utilizando Python e o padrão MPI (*Message Passing Interface*). O objetivo é demonstrar e mensurar a escalabilidade de algoritmos paralelos frente à execução sequencial tradicional.

## 📋 Funcionalidades

* **Comparativo Sequencial vs. Paralelo:** Executa a mesma carga de trabalho em 1 núcleo e em $N$ núcleos para comparação direta.
* **Carga de Trabalho Intensiva (Compute Bound):** Utiliza operações de estresse de FPU (Seno, Cosseno, Raiz) para garantir que o ganho de processamento supere o custo de comunicação.
* **Métricas de HPC:** Calcula automaticamente o *Speedup* e a *Eficiência* do cluster.
* **Monitoramento de Hardware:**
    * Uso de RAM por processo.
    * Identificação de PIDs (Process IDs).
    * Leitura de sensores de temperatura da CPU (Linux).
* **Verificação de Integridade:** Garante que o resultado paralelo é matematicamente idêntico ao sequencial.

## 🛠️ Pré-requisitos

Para executar este projeto, você precisa de um ambiente Linux (recomendado) ou Windows com suporte a MPI.

### Dependências do Sistema (Linux / Ubuntu / Pop!_OS)
O Python precisa da biblioteca MPI escrita em C instalada no sistema operacional para funcionar.

```bash
sudo apt update
sudo apt install openmpi-bin libopenmpi-dev

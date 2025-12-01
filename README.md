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
````

### Bibliotecas Python

As seguintes bibliotecas são necessárias:

  * `mpi4py`: Interface Python para MPI.
  * `numpy`: Computação numérica de alta performance.
  * `psutil`: Acesso a métricas do sistema (RAM, CPU, Temperatura).

Instale via pip:

```bash
pip install mpi4py numpy psutil
```

-----

## 🚀 Como Executar

O script não deve ser executado com o comando `python` padrão. Deve-se utilizar o `mpiexec` (ou `mpirun`) para gerenciar os processos distribuídos.

### No Linux (Terminal)

Para rodar utilizando **4 núcleos** do processador:

```bash
mpiexec -n 4 python3 experimento.py
```

*Se quiser usar mais núcleos, altere o número após o `-n` (ex: `-n 8`).*

### No Windows (PowerShell / CMD)

1.  Certifique-se de ter instalado o [Microsoft MPI v10.0+](https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi).
2.  Execute o comando:

<!-- end list -->

```cmd
mpiexec -n 4 python experimento.py
```

-----

## 📊 Entendendo o Relatório

Ao final da execução, o programa exibirá:

1.  **Tabela de Processos:** Mostra que cada "Rank" (núcleo) é um processo independente no sistema operacional, com seu próprio uso de memória RAM.
2.  **Speedup:** Quantas vezes o código paralelo foi mais rápido que o sequencial.
      * *Fórmula:* $Speedup = T_{sequencial} / T_{paralelo}$
      * *Exemplo:* Um Speedup de **3.5x** em 4 núcleos é um resultado excelente.
3.  **Eficiência:** A porcentagem de utilização real dos núcleos.
      * *Exemplo:* 85% significa que 15% do tempo foi perdido em comunicação ou espera.
4.  **Variação Térmica:** Diferença de temperatura da CPU causada pelo esforço computacional (funcionalidade dependente de sensores Linux compatíveis).

## ⚠️ Solução de Problemas Comuns

  * **Erro `cannot load MPI library`:**
      * Significa que você esqueceu de rodar o `sudo apt install libopenmpi-dev`. O `pip` instala apenas a ponte Python, não o motor MPI.
  * **Temperatura "N/A":**
      * Pode ocorrer em Máquinas Virtuais (VirtualBox/WSL) ou Windows, onde o acesso direto aos sensores de hardware é bloqueado pelo hospedeiro.
  * **Speedup baixo (\< 1.0x):**
      * Significa que a comunicação demorou mais que o cálculo. Aumente a variável `COMPLEXIDADE` no código para forçar mais trabalho de CPU.

-----

**Autor:** Marlos Emanuel da Silveira Fontes
**Disciplina:** Programação Paralela / HPC

from mpi4py import MPI
import numpy as np
import time
import os
import psutil
import sys

# Configurações do Experimento
TAMANHO_VETOR = 1_000_000 
COMPLEXIDADE = 500 

def get_temp():
    try:
        temps = psutil.sensors_temperatures()
        if not temps: return "N/A"
        
        # Sensores comuns em Linux
        sensores = ['coretemp', 'k10temp', 'acpitz', 'thinkpad', 'zenpower']
        for name in sensores:
            if name in temps:
                return f"{temps[name][0].current}°C"
        return "N/A"
    except:
        return "N/A"

def kernel_processamento(dados):
    res = dados.copy()
    # Carga matemática intensiva para estresse de FPU
    for _ in range(COMPLEXIDADE):
        res = np.sin(res) * np.cos(res) + np.sqrt(np.abs(res))
    return np.sum(res)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    name = MPI.Get_processor_name()

    # Leitura inicial de temperatura (apenas Rank 0)
    temp_inicial = "N/A"
    if rank == 0:
        temp_inicial = get_temp()

    comm.Barrier()

    dados_full = None
    tempo_seq = 0.0
    res_seq = 0.0

    # --- Execução Sequencial ---
    if rank == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{'='*80}")
        print(f"   HPC BENCHMARK - SPEEDUP & ANÁLISE TÉRMICA")
        print(f"{'='*80}")
        print(f"Nós: {size} | Elementos: {TAMANHO_VETOR} | Ciclos: {COMPLEXIDADE}")
        print(f"Temp. Inicial: {temp_inicial}")
        print("-" * 80)
        
        dados_full = np.random.rand(TAMANHO_VETOR).astype('float64')

        print(f"[*] Iniciando processamento Sequencial...")
        t_ini = time.time()
        res_seq = kernel_processamento(dados_full)
        t_fim = time.time()
        tempo_seq = t_fim - t_ini
        print(f"ok (Tempo: {tempo_seq:.4f}s)")
        print("-" * 80)

    comm.Barrier()

    # --- Execução Paralela ---
    if rank == 0:
        print(f"[*] Iniciando processamento Paralelo ({size} núcleos)...")

    t_par_ini = time.time()

    # Scatter
    n_local = TAMANHO_VETOR // size
    dados_locais = np.empty(n_local, dtype='float64')
    comm.Scatter(dados_full, dados_locais, root=0)

    # Processamento Local e Coleta de Métricas
    pid = os.getpid()
    proc = psutil.Process(pid)
    
    t_calc_ini = time.time()
    soma_local = kernel_processamento(dados_locais)
    t_calc_fim = time.time()
    
    ram_mb = proc.memory_info().rss / (1024 * 1024)
    stats = {
        'rank': rank, 'pid': pid, 'host': name,
        'ram': ram_mb, 'tempo': t_calc_fim - t_calc_ini
    }

    # Reduce e Gather
    soma_total = np.array(0.0, dtype='float64')
    soma_local_buf = np.array(soma_local, dtype='float64')
    comm.Reduce(soma_local_buf, soma_total, op=MPI.SUM, root=0)
    todos_stats = comm.gather(stats, root=0)

    t_par_fim = time.time()
    tempo_par = t_par_fim - t_par_ini

    # --- Relatório Final ---
    if rank == 0:
        temp_final = get_temp()
        
        print(f"ok (Tempo: {tempo_par:.4f}s)")
        print("\n" + "="*80)
        print("RELATÓRIO DE EXECUÇÃO")
        print("="*80)
        
        print(f"{'RANK':<5} | {'PID':<8} | {'HOST':<10} | {'RAM (MB)':<10} | {'CPU TIME (s)':<15}")
        print("-" * 80)
        total_ram = 0
        for s in todos_stats:
            print(f"{s['rank']:<5} | {s['pid']:<8} | {s['host']:<10} | {s['ram']:<10.2f} | {s['tempo']:.4f}")
            total_ram += s['ram']
        print("-" * 80)

        speedup = tempo_seq / tempo_par
        eficiencia = speedup / size
        
        print("MÉTRICAS DE DESEMPENHO:")
        print(f"1. Térmica:")
        print(f"   - Inicial: {temp_inicial} | Final: {temp_final}")

        print(f"\n2. Escalabilidade:")
        print(f"   - Sequencial: {tempo_seq:.4f}s")
        print(f"   - Paralelo:   {tempo_par:.4f}s")
        print(f"   - SPEEDUP:    {speedup:.2f}x")
        print(f"   - Eficiência: {eficiencia*100:.1f}%")

        print(f"\n3. Integridade:")
        erro = abs(res_seq - soma_total)
        status = "SUCESSO" if erro < 1e-4 else "ERRO"
        print(f"   - Erro: {erro:.6e} ({status})")
        print("="*80)

if __name__ == "__main__":
    main()
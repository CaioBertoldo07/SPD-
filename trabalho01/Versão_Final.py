"""
Trabalho Prático - Multithreading: Produtor x Consumidor
Disciplina: Sistemas Paralelos e Distribuídos
Alunos: Caio Bertoldo, Leonardo Abinader
Fontes:
    https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem
    https://realpython.com/intro-to-python-threading/
    https://docs.python.org/3/library/threading.html
    https://docs.python.org/3/library/queue.html
Semestre: 2025/2

Descrição:
Este programa implementa o problema clássico do Produtor x Consumidor utilizando multithreading em Python.
- O número de produtores (P), consumidores (C) e o tamanho do buffer (T) são configuráveis.
- A sincronização é feita com queue.Queue (thread-safe).
- São executados diferentes cenários (P=C, P=2C, C=2P) com T=1 e T=5.
- O programa coleta métricas de tempo de execução, quantidade de itens produzidos e itens restantes no buffer.
- Os resultados são salvos em CSV e visualizados em gráficos comparativos.
"""

import threading
import queue
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# Buffer compartilhado (recriado em cada experimento)
buffer = None

def producer(producerId, nItems):
    """Função executada por uma thread produtora"""
    for i in range(nItems):
        item = f"Item-{producerId}-{i}"
        time.sleep(random.uniform(0.05, 0.2))  # Simula tempo de produção
        buffer.put(item)  # Bloqueia se o buffer estiver cheio
        print(f"[Producer {producerId}] produced {item}")

def consumer(consumerId):
    """Função executada por uma thread consumidora"""
    while True:
        try:
            item = buffer.get(timeout=2)  # Espera até 2s por um item
            print(f"    [Consumer {consumerId}] consumed {item}")
            time.sleep(random.uniform(0.05, 0.3))  # Simula tempo de consumo
            buffer.task_done()
        except queue.Empty:
            break
    
def distribute_items(N, P):
    """
    Distribui N itens entre P produtores de forma justa.
    Exemplo: N=10, P=3 -> [4, 3, 3]
    """
    base = N // P
    remainder = N % P
    distribution = [base + (1 if i < remainder else 0) for i in range(P)]
    return distribution

def runExperiment(P, C, T, N):
    """Executa um experimento com P produtores, C consumidores e buffer de tamanho T"""
    global buffer
    buffer = queue.Queue(maxsize=T)

    threads = []
    distribution = distribute_items(N, P)

    start = time.time()

    for p in range(P):
        t = threading.Thread(target=producer, args=(p+1, distribution[p]))
        threads.append(t)
        t.start()
    
    for c in range(C):
        t = threading.Thread(target=consumer, args=(c+1,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.time()
    runtime = end - start
    remainingItems = buffer.qsize()

    return {
        "Producers": P,
        "Consumers": C,
        "Buffer": T,
        "Produced Items": sum(distribution),
        "Remaining Items": remainingItems,
        "Runtime (s)": round(runtime, 3)
    }

def main():
    N = 35  # total de itens a serem produzidos
    results = []

    # Conjuntos de configurações solicitadas no enunciado
    settings = [
        # P == C
        (2, 2, 1), (2, 2, 5),
        # P == 2C
        (4, 2, 1), (4, 2, 5),
        # C == 2P
        (2, 4, 1), (2, 4, 5),
    ]

    for P, C, T in settings:
        print(f"\n--- Running experiment P={P}, C={C}, T={T} ---\n")
        result = runExperiment(P, C, T, N)
        results.append(result)
    
    # DataFrame para análise
    df = pd.DataFrame(results)
    print("\n===== RESULTS =====")
    print(df)

    # Salvar em CSV
    df.to_csv("experiments_results.csv", index=False)

    # ---------- GRÁFICOS ----------
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    # Tempo de execução
    plt.figure(figsize=(9,6))
    for idx, T in enumerate(df["Buffer"].unique()):
        subset = df[df["Buffer"] == T]
        plt.plot(
            range(len(subset)),
            subset["Runtime (s)"],
            marker="o",
            label=f"Buffer={T}",
            color=colors[idx % len(colors)]
        )
        for i, val in enumerate(subset["Runtime (s)"]):
            plt.text(i, val+0.02, str(val), ha="center", fontsize=9)
    plt.xticks(
        range(len(df)),
        [f"P={r['Producers']}, C={r['Consumers']}, T={r['Buffer']}" for _, r in df.iterrows()],
        rotation=45, ha="right"
    )
    plt.ylabel("Runtime (s)")
    plt.title("Runtime per configuration")
    plt.legend()
    plt.tight_layout()
    plt.savefig("runtime_graph.png")
    plt.show()

    # Itens restantes (só gera gráfico se houver sobras)
    if df["Remaining Items"].sum() > 0:
        plt.figure(figsize=(9,6))
        bars = plt.bar(
            range(len(df)),
            df["Remaining Items"],
            tick_label=[f"P={r['Producers']}, C={r['Consumers']}, T={r['Buffer']}" for _, r in df.iterrows()],
            color=colors[:len(df)]
        )
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, height+0.05, str(height), ha="center", fontsize=9)
        plt.ylabel("Remaining items in the buffer")
        plt.title("Remaining items by configuration")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("remaining_items_graph.png")
        plt.show()
    else:
        print("\n[INFO] Nenhum item ficou sobrando em nenhuma configuração. Gráfico de 'Remaining Items' não foi gerado.")


if __name__ == "__main__":
    main()

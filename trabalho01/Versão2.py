import threading
import queue
import time
import random

# Buffer compartilhado (será recriado em cada experimento)
buffer = None

def producer(producerId, nItems):
    for i in range(nItems):
        item = f"Item -{producerId}-{i}"
        time.sleep(random.uniform(0.05, 0.2)) # Simula tempo de produção
        buffer.put(item) # Bloqueia se o buffer estiver cheio
        print(f"[Producer {producerId}] produced {item}")

def consumer(consumerId):
    while True:
        try:
            item = buffer.get(timeout=2) # Espera até 2s por um item
            print(f"    [Consumer {consumerId}] consumed {item}")
            time.sleep(random.uniform(0.05, 0.3)) # Simula tempo de consumo
            buffer.task_done()
        except queue.Empty:
            break
    
def runExperiment(P, C, T, N):
    global buffer
    buffer = queue.Queue(maxsize=T) # recria buffer para cada execução

    threads = []
    itemsByProducer = N // P

    start = time.time()

    for p in range(P):
        t = threading.Thread(target=producer, args=(p+1, itemsByProducer))
        threads.append(t)
        t.start()
    
    for c in range(C):
        t = threading.Thread(target=consumer, args=(c+1,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    end = time.time()
    executionTime = end - start
    remainingItems = buffer.qsize()

    return {
        "Producers": P,
        "Consumers": C,
        "Buffer": T,
        "Produced Items": P * itemsByProducer,
        "Items ramaining in the buffer": remainingItems,
        "Execution time (s)": round(executionTime, 3)
    }

def main():
    N = 40 # total de itens a serem produzidos
    results = []

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
    
    # Mostra a tabela final
    print("\n-~-~-~-~- RESULTS -~-~-~-~-")
    for r in results:
        print(r)

if __name__ == "__main__":
    main()
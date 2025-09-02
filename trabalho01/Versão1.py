import threading
import queue
import time
import random

# Configurações iniciais
P = 2 # Número de produtores
C = 2 # Número de consumidores
T = 5 # Tamanho do buffer
N = 20 # Quantidade total de itens a serem produzidos

# Buffer compartilhado
buffer = queue.Queue(maxsize=T)

def producer(producerId, nItems):
    for i in range(nItems):
        item = f"Item-{producerId}-{i}"
        time.sleep(random.uniform(0.1, 0.5)) # Simula o tempo de produção
        buffer.put(item) # Bloqueia se o buffer estiver cheio
        print(f"[Producer {producerId}] produced {item}")

def cosumer(consumerId):
    while True:
        try:
            item = buffer.get(timeout=3) # Espera até 3s por um item
            print(f"    [Consumer {consumerId}] cosumed {item}")
            time.sleep(random.uniform(0.2, 0.6)) # Simula tempo de consumo
            buffer.task_done()
        except queue.Empty:
            break

def main(P, C, T, N):
    global buffer
    buffer = queue.Queue(maxsize=T) # Recria o buffer

    threads = []

    # Divide itens igualmente entre produtores
    itemsByProducer = N // P

    for p in range(P):
        t = threading.Thread(target=producer, args=(p+1, itemsByProducer))
        threads.append(t)
        t.start()
    
    for c in range(C):
        t = threading.Thread(target=cosumer, args=(c+1,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("\nFinished Execution.\n")

if __name__ == "__main__":
    main(P, C, T, N)


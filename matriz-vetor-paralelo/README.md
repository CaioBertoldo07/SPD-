# 🧮 Multiplicação Paralela de Matriz × Vetor

Trabalho Prático -- Programação Paralela\
Disciplina: Sistemas Paralelos e Distribuídos\
Semestre: 2025.2

------------------------------------------------------------------------

## 🎯 Objetivo do Projeto

Implementar duas versões de um algoritmo de multiplicação **matriz ×
vetor**:

1.  **Versão Sequencial (sem paralelismo)**
2.  **Versão Paralela usando metade dos núcleos**
3.  **Versão Paralela usando todos os núcleos da máquina**

Ao final, comparar os tempos de execução entre as versões e analisar os
ganhos obtidos com paralelismo.

------------------------------------------------------------------------

## 🧠 Descrição da Tarefa

Dada uma matriz `A` de dimensão `N × M` e um vetor `v` de tamanho `M`, o
algoritmo calcula:

    resultado[i] = soma( A[i][j] * v[j] ) para j de 0 até M-1

A multiplicação será paralelizada dividindo as **linhas da matriz**
entre múltiplos processos, permitindo aproveitar múltiplos núcleos da
CPU.

------------------------------------------------------------------------

## 🚀 Tecnologias Utilizadas

-   **Python 3.10+**
-   `multiprocessing` para paralelismo real (CPU-bound, sem
    interferência do GIL)
-   `time` / `perf_counter` para medição de tempo
-   `json` para salvar matrizes e vetores
-   `matplotlib` (opcional) para gráficos de comparação

------------------------------------------------------------------------

## 📁 Estrutura do Projeto

    /matriz-vetor-paralelo
    │
    ├── src/
    │   ├── sequencial.py
    │   ├── paralelo.py
    │   ├── gerar_matriz.py
    │   ├── utils.py
    │   └── benchmark.py
    │
    ├── dados/
    │   └── matriz_10000x1000.json
    │
    ├── resultados/
    │   ├── tempos.txt
    │   └── grafico_comparacao.png
    │
    └── README.md

------------------------------------------------------------------------

## 📌 Planejamento do Projeto

### **1. Geração da Matriz e Vetor**

-   Criar um script que gera uma matriz grande, como:
    -   3000×3000\
    -   5000×1000\
    -   10000×1000\
-   Salvar em JSON ou binário (NumPy opcional).
-   Criar um vetor compatível.

### **2. Versão Sequencial**

Arquivo: `sequencial.py` - Implementar a multiplicação normal matriz ×
vetor. - Medir o tempo. - Salvar o resultado.

### **3. Versão Paralela**

Arquivo: `paralelo.py` - Utilizar `multiprocessing.Pool`. - Cada
processo recebe um conjunto de linhas. - Implementar: - Modo **half** →
metade dos núcleos - Modo **full** → todos os núcleos - Medir tempo de
execução de ambos os modos.

### **4. Benchmark**

Arquivo: `benchmark.py` - Executar sequencial, half e full
automaticamente. - Registrar tempos. - Calcular speedup:
`speedup = tempo_sequencial / tempo_paralelo` - Gerar arquivo de
resultados.

### **5. Gráfico (opcional, recomendado)**

-   Criar gráfico de barras mostrando o tempo de cada versão.
-   Salvar em `/resultados/grafico_comparacao.png`.

### **6. Vídeo Final**

Deve conter: 1. Nome dos integrantes 2. Explicação da abordagem
sequencial 3. Explicação da abordagem paralela 4. Execução de cada
versão 5. Análise dos resultados e conclusões

------------------------------------------------------------------------

## 📊 Exemplo de Resultados Esperados

    Tamanho: 10000 x 1000

    Tempo Sequencial:            8.52 segundos
    Tempo Paralelo (50% CPUs):   3.10 segundos
    Tempo Paralelo (100% CPUs):  1.79 segundos

    Speedup (50%):  2.74x
    Speedup (100%): 4.75x

------------------------------------------------------------------------

## 🧪 Como Executar

### **Gerar matriz**

``` bash
python src/gerar_matriz.py
```

### **Rodar versão sequencial**

``` bash
python src/sequencial.py
```

### **Rodar versão paralela**

Metade dos núcleos:

``` bash
python src/paralelo.py --modo half
```

Todos os núcleos:

``` bash
python src/paralelo.py --modo full
```

### **Benchmark completo**

``` bash
python src/benchmark.py
```

------------------------------------------------------------------------

## 📝 Créditos

Projeto desenvolvido por:\
**Caio Bertoldo Bezerra**, **Leonardo Abinader**\
Universidade do Estado do Amazonas\
Disciplina: Sistemas Paralelos e Distribuídos\
Professora: **Danielle Valente**

------------------------------------------------------------------------

## 📚 Referências

-   Documentação Python `multiprocessing`
-   Material da disciplina de SP&D
-   Padrões de Programação Paralela (distribuição de linhas)

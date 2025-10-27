# 🧮 Calculadora Distribuída com gRPC

**Trabalho Prático 2 - RPC**  
**Disciplina:** Sistemas Paralelos e Distribuídos  
**Professor:** Danielle Valente  
**Semestre:** 2025-02

---

## 📋 Descrição do Projeto

Implementação de uma **Calculadora Distribuída** utilizando gRPC em Python. O sistema oferece operações básicas (adição, subtração, multiplicação e divisão) através de chamadas RPC unárias, seguindo a arquitetura stateless.

### ✨ Funcionalidades Implementadas

#### Requisitos Básicos (Nível 0):
- ✅ Operações básicas: Add, Sub, Mul, Div
- ✅ Chamadas unárias gRPC
- ✅ Arquitetura stateless
- ✅ Código comentado e documentado

#### Extras Opcionais:
- ✅ **Interceptors de log** no servidor
- ✅ **Validação de entrada** (divisão por zero)
- ✅ **Testes com grpcurl**
- ✅ Cliente interativo com menu
- ✅ Suite de testes automatizados

---

## 📁 Estrutura do Projeto

```
calculadora-grpc/
│
├── calculator.proto              # Definição do serviço gRPC
├── server.py                     # Servidor gRPC com interceptors
├── client.py                     # Cliente interativo
├── requirements.txt              # Dependências Python
├── test_grpcurl.sh              # Script de testes com grpcurl
├── README.md                     # Este arquivo
│
├── calculator_pb2.py            # Gerado automaticamente
└── calculator_pb2_grpc.py       # Gerado automaticamente
```

---

## 🚀 Configuração e Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```bash
# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

### Passo 2: Gerar Código gRPC

O comando abaixo gera os arquivos Python a partir do arquivo `.proto`:

```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

**Arquivos gerados:**
- `calculator_pb2.py` - Classes para mensagens Protocol Buffer
- `calculator_pb2_grpc.py` - Classes para serviço gRPC

---

## 🎯 Executando o Projeto

### 1️⃣ Iniciar o Servidor

Em um terminal, execute:

```bash
python server.py
```

**Saída esperada:**
```
2025-10-27 10:00:00 - INFO - 🚀 Servidor gRPC iniciado na porta 50051
2025-10-27 10:00:00 - INFO - 📡 Aguardando requisições...
```

### 2️⃣ Executar o Cliente

Em outro terminal, execute:

```bash
python client.py
```

Você verá um menu interativo:

```
==================================================
🧮 CALCULADORA DISTRIBUÍDA - gRPC
==================================================
1. ➕ Adição
2. ➖ Subtração
3. ✖️  Multiplicação
4. ➗ Divisão
5. 🧪 Executar Testes Automatizados
0. 🚪 Sair
==================================================
```

### 3️⃣ Executar Testes com grpcurl (Opcional)

Primeiro, instale o grpcurl (se necessário):

```bash
# No Linux/Mac com Homebrew
brew install grpcurl

# Ou baixe do GitHub
# https://github.com/fullstorydev/grpcurl/releases
```

Depois execute o script de testes:

```bash
chmod +x test_grpcurl.sh
./test_grpcurl.sh
```

---

## 🧪 Casos de Teste

O cliente inclui uma suite automatizada de testes que valida:

1. ✅ **Adição básica** (10 + 5)
2. ✅ **Subtração básica** (10 - 5)
3. ✅ **Multiplicação básica** (10 × 5)
4. ✅ **Divisão básica** (10 ÷ 5)
5. ✅ **Operações com negativos** (-10 + 5)
6. ✅ **Subtração com negativos** (-10 - (-5))
7. ✅ **Multiplicação por zero** (10 × 0)
8. ⚠️ **Divisão por zero** (10 ÷ 0) - **DEVE FALHAR**
9. ✅ **Divisão com decimais** (7 ÷ 3)
10. ✅ **Números grandes** (999999 × 999999)

Para executar os testes automatizados, escolha a opção **5** no menu do cliente.

---

## 🔧 Testando com grpcurl

### Listar serviços disponíveis:
```bash
grpcurl -plaintext localhost:50051 list
```

### Listar métodos do Calculator:
```bash
grpcurl -plaintext localhost:50051 list calculator.Calculator
```

### Testar operação de adição:
```bash
grpcurl -plaintext -d '{"num1": 10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Add
```

### Testar divisão por zero (deve retornar erro):
```bash
grpcurl -plaintext -d '{"num1": 10, "num2": 0}' \
    localhost:50051 calculator.Calculator/Div
```

---

## 📊 Arquitetura e Estratégias de Projeto

### Arquitetura Stateless

O servidor **não mantém estado** entre requisições. Cada operação é independente:
- ✅ Permite escalabilidade horizontal
- ✅ Facilita tolerância a falhas
- ✅ Simplifica o design do sistema

### Interceptors de Log

Implementado um **interceptor de servidor** que:
- 📝 Registra todas as requisições recebidas
- ⏱️ Mede tempo de processamento
- 🔍 Auxilia no debug e monitoramento

### Validação de Entrada

A operação de **divisão** inclui validação:
- ⚠️ Detecta divisão por zero antes do cálculo
- 🚫 Retorna erro apropriado ao cliente
- 📋 Define código de status gRPC (INVALID_ARGUMENT)

### Tratamento de Erros

Todas as operações possuem:
- Try-catch para exceções
- Mensagens de erro descritivas
- Flag `success` na resposta
- Logging de erros no servidor

---

## 🎓 Conceitos gRPC Demonstrados

### 1. Protocol Buffers
- Definição de mensagens fortemente tipadas
- Serialização eficiente de dados
- Contrato de interface (`.proto`)

### 2. Chamadas Unárias
- Requisição → Resposta (1:1)
- Padrão request-response tradicional
- Todas as 4 operações implementadas assim

### 3. Interceptors
- Middleware para logging
- Processamento antes/depois das requisições
- Separação de concerns (logging vs lógica de negócio)

### 4. Códigos de Status
- `OK` para operações bem-sucedidas
- `INVALID_ARGUMENT` para divisão por zero
- Tratamento de erros padronizado

---

## 📝 Comandos Úteis

### Gerar novamente os arquivos gRPC:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

### Iniciar servidor em modo debug:
```bash
python -u server.py
```

### Verificar se a porta está aberta:
```bash
# Linux/Mac
lsof -i :50051

# Windows
netstat -ano | findstr :50051
```

### Parar o servidor:
```
Ctrl + C
```

---

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'calculator_pb2'"
**Solução:** Execute o comando de geração do código gRPC:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

### Erro: "failed to connect to all addresses"
**Solução:** Certifique-se de que o servidor está rodando:
```bash
python server.py
```

### Erro: "Address already in use"
**Solução:** A porta 50051 já está em uso. Mate o processo:
```bash
# Linux/Mac
lsof -ti:50051 | xargs kill -9

# Ou mude a porta no código
```

---

## 📚 Fontes de Consulta

- **gRPC Documentation:** https://grpc.io/docs/languages/python/
- **Protocol Buffers Guide:** https://protobuf.dev/
- **grpcurl GitHub:** https://github.com/fullstorydev/grpcurl
- **Python gRPC Tutorial:** https://grpc.io/docs/languages/python/basics/

---

## 👥 Autores

**[Caio Bertoldo e Leonardo Abinader]**  
Engenharia da Computação 
Sistemas Paralelos e Distribuídos - 2025-02

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de Sistemas Paralelos e Distribuídos.

---

**Data de Entrega:** 27/10/2025  
**Professor:** Danielle Valente
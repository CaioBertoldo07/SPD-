#!/bin/bash
# Script para testes com grpcurl (Extra opcional implementado)

echo "=================================================="
echo "🧪 TESTES COM GRPCURL - Calculadora Distribuída"
echo "=================================================="
echo ""

# Verifica se o servidor está rodando
echo "🔍 Verificando disponibilidade do servidor..."
if ! nc -z localhost 50051; then
    echo "❌ Servidor não encontrado na porta 50051"
    echo "💡 Inicie o servidor com: python server.py"
    exit 1
fi
echo "✅ Servidor disponível!"
echo ""

# Lista os serviços disponíveis
echo "📋 Listando serviços disponíveis:"
echo "--------------------------------------------------"
grpcurl -plaintext localhost:50051 list
echo ""

# Lista os métodos do serviço Calculator
echo "📋 Listando métodos do Calculator:"
echo "--------------------------------------------------"
grpcurl -plaintext localhost:50051 list calculator.Calculator
echo ""

# Descreve o serviço
echo "📖 Descrição do serviço Calculator:"
echo "--------------------------------------------------"
grpcurl -plaintext localhost:50051 describe calculator.Calculator
echo ""

# Testes de operações
echo "=================================================="
echo "🧪 EXECUTANDO TESTES"
echo "=================================================="
echo ""

# Teste 1: Adição
echo "➕ Teste 1: Adição (10 + 5)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Add
echo ""

# Teste 2: Subtração
echo "➖ Teste 2: Subtração (10 - 5)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Sub
echo ""

# Teste 3: Multiplicação
echo "✖️  Teste 3: Multiplicação (10 * 5)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Mul
echo ""

# Teste 4: Divisão válida
echo "➗ Teste 4: Divisão (10 / 5)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Div
echo ""

# Teste 5: Divisão por zero (deve falhar)
echo "⚠️  Teste 5: Divisão por zero (10 / 0) - DEVE FALHAR"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 10, "num2": 0}' \
    localhost:50051 calculator.Calculator/Div
echo ""

# Teste 6: Números negativos
echo "➖ Teste 6: Operação com negativos (-10 + 5)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": -10, "num2": 5}' \
    localhost:50051 calculator.Calculator/Add
echo ""

# Teste 7: Números decimais
echo "📊 Teste 7: Divisão com decimais (7 / 3)"
echo "--------------------------------------------------"
grpcurl -plaintext -d '{"num1": 7, "num2": 3}' \
    localhost:50051 calculator.Calculator/Div
echo ""

echo "=================================================="
echo "✅ TESTES CONCLUÍDOS"
echo "=================================================="
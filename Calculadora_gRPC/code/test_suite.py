import grpc
import calculator_pb2
import calculator_pb2_grpc
import time
from datetime import datetime


class TestRunner:
    """
    Executor de testes automatizados
    """
    
    def __init__(self, host='localhost', port='50051'):
        """Inicializa conexão com servidor"""
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = calculator_pb2_grpc.CalculatorStub(self.channel)
        self.results = []
    
    def run_test(self, name, operation, num1, num2, expected_result=None, should_fail=False):
        """
        Executa um teste individual
        
        Args:
            name: Nome do teste
            operation: Função de operação (Add, Sub, Mul, Div)
            num1: Primeiro número
            num2: Segundo número
            expected_result: Resultado esperado (opcional)
            should_fail: Se o teste deve falhar (para divisão por zero)
        """
        print(f"\n{'='*60}")
        print(f"📋 Teste: {name}")
        print(f"{'='*60}")
        print(f"Operação: {operation.__name__}")
        print(f"Entrada: num1={num1}, num2={num2}")
        
        try:
            request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
            start_time = time.time()
            response = operation(request)
            elapsed_time = time.time() - start_time
            
            success = response.success
            result = response.result
            error = response.error
            
            print(f"Tempo de resposta: {elapsed_time*1000:.2f}ms")
            print(f"Status: {'✅ SUCESSO' if success else '❌ ERRO'}")
            print(f"Resultado: {result}")
            
            if error:
                print(f"Mensagem de erro: {error}")
            
            # Verifica se o resultado é o esperado
            test_passed = False
            if should_fail:
                # Teste deve falhar
                test_passed = not success
                print(f"\n{'✅ PASS' if test_passed else '❌ FAIL'} - Erro capturado como esperado" if test_passed else "Deveria ter falhado mas não falhou")
            else:
                # Teste deve ter sucesso
                if expected_result is not None:
                    # Compara com resultado esperado (com tolerância para floats)
                    test_passed = success and abs(result - expected_result) < 0.0001
                    print(f"Resultado esperado: {expected_result}")
                    print(f"\n{'✅ PASS' if test_passed else '❌ FAIL'}")
                else:
                    test_passed = success
                    print(f"\n{'✅ PASS' if test_passed else '❌ FAIL'}")
            
            self.results.append({
                'name': name,
                'passed': test_passed,
                'time': elapsed_time,
                'result': result if success else error
            })
            
        except grpc.RpcError as e:
            print(f"❌ Erro RPC: {e.code()} - {e.details()}")
            self.results.append({
                'name': name,
                'passed': should_fail,  # Se deve falhar, RPC error é esperado
                'time': 0,
                'result': f"RPC Error: {e.details()}"
            })
    
    def print_summary(self):
        """
        Imprime resumo dos testes
        """
        print("\n" + "="*60)
        print("📊 RESUMO DOS TESTES")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['passed'])
        total = len(self.results)
        
        print(f"\n✅ Testes Aprovados: {passed}/{total}")
        print(f"❌ Testes Falhados: {total-passed}/{total}")
        print(f"📈 Taxa de Sucesso: {(passed/total*100):.1f}%")
        
        total_time = sum(r['time'] for r in self.results)
        print(f"⏱️  Tempo Total: {total_time*1000:.2f}ms")
        print(f"⚡ Tempo Médio: {(total_time/total)*1000:.2f}ms")
        
        print(f"\n{'='*60}")
        print("DETALHES DOS TESTES")
        print(f"{'='*60}\n")
        
        for i, result in enumerate(self.results, 1):
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"{i}. {status} - {result['name']}")
            print(f"   Tempo: {result['time']*1000:.2f}ms")
            print(f"   Resultado: {result['result']}\n")
    
    def close(self):
        """Fecha conexão"""
        self.channel.close()


def main():
    """
    Função principal - executa suite de testes
    """
    print("="*60)
    print("🧪 SUITE DE TESTES AUTOMATIZADOS")
    print("Calculadora Distribuída gRPC")
    print("="*60)
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    try:
        runner = TestRunner()
    except Exception as e:
        print(f"\n❌ Erro ao conectar ao servidor: {e}")
        print("💡 Certifique-se de que o servidor está rodando!")
        print("   Execute: python server.py")
        return
    
    print("\n🚀 Iniciando testes...\n")
    time.sleep(1)
    
    # Bateria de testes
    tests = [
        # Testes básicos
        ("Adição básica (10 + 5)", runner.stub.Add, 10, 5, 15),
        ("Subtração básica (10 - 5)", runner.stub.Sub, 10, 5, 5),
        ("Multiplicação básica (10 * 5)", runner.stub.Mul, 10, 5, 50),
        ("Divisão básica (10 / 5)", runner.stub.Div, 10, 5, 2.0),
        
        # Testes com negativos
        ("Adição com negativos (-10 + 5)", runner.stub.Add, -10, 5, -5),
        ("Subtração com negativos (-10 - -5)", runner.stub.Sub, -10, -5, -5),
        ("Multiplicação com negativos (-10 * 5)", runner.stub.Mul, -10, 5, -50),
        ("Divisão com negativos (-10 / 5)", runner.stub.Div, -10, 5, -2.0),
        
        # Testes com zero
        ("Multiplicação por zero (10 * 0)", runner.stub.Mul, 10, 0, 0),
        ("Adição com zero (10 + 0)", runner.stub.Add, 10, 0, 10),
        
        # Teste de divisão por zero (deve falhar)
        ("Divisão por zero - DEVE FALHAR (10 / 0)", runner.stub.Div, 10, 0, None, True),
        
        # Testes com decimais
        ("Divisão com decimais (7 / 3)", runner.stub.Div, 7, 3, 7/3),
        ("Divisão exata (15 / 3)", runner.stub.Div, 15, 3, 5.0),
        
        # Testes com números grandes
        ("Números grandes (999999 * 999999)", runner.stub.Mul, 999999, 999999, 999998000001),
        ("Números grandes na divisão (1000000 / 1000)", runner.stub.Div, 1000000, 1000, 1000.0),
        
        # Testes edge cases
        ("Subtração resultando em zero (5 - 5)", runner.stub.Sub, 5, 5, 0),
        ("Multiplicação de decimais (2.5 * 4.5)", runner.stub.Mul, 2.5, 4.5, 11.25),
        ("Divisão com resultado decimal (1 / 3)", runner.stub.Div, 1, 3, 1/3),
    ]
    
    # Executa todos os testes
    for test_params in tests:
        runner.run_test(*test_params)
        time.sleep(0.5)  # Pausa entre testes
    
    # Imprime resumo
    runner.print_summary()
    
    # Fecha conexão
    runner.close()
    
    print("\n" + "="*60)
    print("✅ TESTES CONCLUÍDOS")
    print("="*60)


if __name__ == '__main__':
    main()
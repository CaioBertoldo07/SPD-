import grpc
import calculator_pb2
import calculator_pb2_grpc
import sys


class CalculatorClient:
    """
    Cliente para comunicação com o serviço Calculator
    Implementa chamadas unárias
    """
    
    def __init__(self, host='localhost', port='50051'):
        """
        Inicializa o cliente gRPC
        
        Args:
            host: Endereço do servidor
            port: Porta do servidor
        """
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = calculator_pb2_grpc.CalculatorStub(self.channel)
        print(f"🔌 Conectado ao servidor {host}:{port}")
    
    def add(self, num1, num2):
        """
        Chamada RPC para operação de adição
        """
        request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
        try:
            response = self.stub.Add(request)
            return self._handle_response(response, "Adição")
        except grpc.RpcError as e:
            print(f"❌ Erro RPC: {e.details()}")
            return None
    
    def sub(self, num1, num2):
        """
        Chamada RPC para operação de subtração
        """
        request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
        try:
            response = self.stub.Sub(request)
            return self._handle_response(response, "Subtração")
        except grpc.RpcError as e:
            print(f"❌ Erro RPC: {e.details()}")
            return None
    
    def mul(self, num1, num2):
        """
        Chamada RPC para operação de multiplicação
        """
        request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
        try:
            response = self.stub.Mul(request)
            return self._handle_response(response, "Multiplicação")
        except grpc.RpcError as e:
            print(f"❌ Erro RPC: {e.details()}")
            return None
    
    def div(self, num1, num2):
        """
        Chamada RPC para operação de divisão
        Inclui validação de divisão por zero
        """
        request = calculator_pb2.OperationRequest(num1=num1, num2=num2)
        try:
            response = self.stub.Div(request)
            return self._handle_response(response, "Divisão")
        except grpc.RpcError as e:
            print(f"❌ Erro RPC: {e.details()}")
            return None
    
    def _handle_response(self, response, operation_name):
        """
        Processa a resposta do servidor
        
        Args:
            response: OperationResponse do servidor
            operation_name: Nome da operação para log
        Returns:
            Resultado se sucesso, None se erro
        """
        if response.success:
            print(f"✅ {operation_name} realizada com sucesso!")
            print(f"📊 Resultado: {response.result}")
            return response.result
        else:
            print(f"❌ Erro na {operation_name}: {response.error}")
            return None
    
    def close(self):
        """
        Fecha a conexão com o servidor
        """
        self.channel.close()
        print("🔌 Conexão encerrada")


def print_menu():
    """
    Exibe o menu interativo
    """
    print("\n" + "="*50)
    print("🧮 CALCULADORA DISTRIBUÍDA - gRPC")
    print("="*50)
    print("1. ➕ Adição")
    print("2. ➖ Subtração")
    print("3. ✖️  Multiplicação")
    print("4. ➗ Divisão")
    print("5. 🧪 Executar Testes Automatizados")
    print("0. 🚪 Sair")
    print("="*50)


def get_numbers():
    """
    Solicita entrada de dois números do usuário
    
    Returns:
        Tupla (num1, num2) ou None se entrada inválida
    """
    try:
        num1 = float(input("Digite o primeiro número: "))
        num2 = float(input("Digite o segundo número: "))
        return num1, num2
    except ValueError:
        print("❌ Entrada inválida! Digite números válidos.")
        return None


def run_tests(client):
    """
    Executa bateria de testes automatizados
    Casos de teste conforme especificação
    """
    print("\n" + "="*50)
    print("🧪 EXECUTANDO TESTES AUTOMATIZADOS")
    print("="*50)
    
    test_cases = [
        ("Adição básica", lambda: client.add(10, 5)),
        ("Subtração básica", lambda: client.sub(10, 5)),
        ("Multiplicação básica", lambda: client.mul(10, 5)),
        ("Divisão básica", lambda: client.div(10, 5)),
        ("Adição com negativos", lambda: client.add(-10, 5)),
        ("Subtração com negativos", lambda: client.sub(-10, -5)),
        ("Multiplicação por zero", lambda: client.mul(10, 0)),
        ("Divisão por zero (DEVE FALHAR)", lambda: client.div(10, 0)),
        ("Divisão com decimais", lambda: client.div(7, 3)),
        ("Operações com números grandes", lambda: client.mul(999999, 999999)),
    ]
    
    results = []
    for i, (test_name, test_func) in enumerate(test_cases, 1):
        print(f"\n📋 Teste {i}/{len(test_cases)}: {test_name}")
        print("-" * 50)
        result = test_func()
        results.append((test_name, result is not None))
        print("-" * 50)
    
    # Resumo dos testes
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"✅ Testes bem-sucedidos: {passed}/{total}")
    print(f"❌ Testes com erro esperado: {total - passed}/{total}")
    
    print("\nDetalhes:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print("="*50)


def main():
    """
    Função principal - menu interativo
    """
    print("🚀 Iniciando Cliente da Calculadora Distribuída")
    
    try:
        client = CalculatorClient()
    except Exception as e:
        print(f"❌ Erro ao conectar ao servidor: {e}")
        print("💡 Certifique-se de que o servidor está rodando!")
        sys.exit(1)
    
    try:
        while True:
            print_menu()
            choice = input("\n👉 Escolha uma opção: ")
            
            if choice == '0':
                print("\n👋 Encerrando cliente...")
                break
            
            elif choice == '5':
                run_tests(client)
            
            elif choice in ['1', '2', '3', '4']:
                numbers = get_numbers()
                if numbers is None:
                    continue
                
                num1, num2 = numbers
                print(f"\n🔄 Enviando requisição ao servidor...")
                
                if choice == '1':
                    client.add(num1, num2)
                elif choice == '2':
                    client.sub(num1, num2)
                elif choice == '3':
                    client.mul(num1, num2)
                elif choice == '4':
                    client.div(num1, num2)
            
            else:
                print("❌ Opção inválida! Tente novamente.")
            
            input("\n⏸️  Pressione ENTER para continuar...")
    
    except KeyboardInterrupt:
        print("\n\n👋 Cliente encerrado pelo usuário")
    
    finally:
        client.close()


if __name__ == '__main__':
    main()
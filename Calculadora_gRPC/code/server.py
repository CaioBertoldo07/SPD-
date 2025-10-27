import grpc
from concurrent import futures
import time
import logging
from datetime import datetime

import calculator_pb2
import calculator_pb2_grpc


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LoggingInterceptor(grpc.ServerInterceptor):
    """
    Interceptor para logging de todas as requisições
    Extra opcional
    """
    
    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method
        logger.info(f"📞 Requisição recebida: {method_name}")
        logger.info(f"   Cliente: {handler_call_details.invocation_metadata}")
        
        start_time = time.time()
        response = continuation(handler_call_details)
        elapsed_time = time.time() - start_time
        
        logger.info(f"✅ Requisição processada: {method_name} em {elapsed_time:.4f}s")
        return response


class CalculatorService(calculator_pb2_grpc.CalculatorServicer):
    """
    Implementação do serviço Calculator (stateless)
    Todas as operações são chamadas unárias
    """
    
    def Add(self, request, context):
        """
        Operação de Adição
        Args:
            request: OperationRequest com num1 e num2
            context: Contexto gRPC
        Returns:
            OperationResponse com resultado
        """
        try:
            result = request.num1 + request.num2
            logger.info(f"➕ ADD: {request.num1} + {request.num2} = {result}")
            
            return calculator_pb2.OperationResponse(
                result=result,
                success=True,
                error=""
            )
        except Exception as e:
            logger.error(f"❌ Erro na adição: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0,
                success=False,
                error=str(e)
            )
    
    def Sub(self, request, context):
        """
        Operação de Subtração
        Args:
            request: OperationRequest com num1 e num2
            context: Contexto gRPC
        Returns:
            OperationResponse com resultado
        """
        try:
            result = request.num1 - request.num2
            logger.info(f"➖ SUB: {request.num1} - {request.num2} = {result}")
            
            return calculator_pb2.OperationResponse(
                result=result,
                success=True,
                error=""
            )
        except Exception as e:
            logger.error(f"❌ Erro na subtração: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0,
                success=False,
                error=str(e)
            )
    
    def Mul(self, request, context):
        """
        Operação de Multiplicação
        Args:
            request: OperationRequest com num1 e num2
            context: Contexto gRPC
        Returns:
            OperationResponse com resultado
        """
        try:
            result = request.num1 * request.num2
            logger.info(f"✖️  MUL: {request.num1} * {request.num2} = {result}")
            
            return calculator_pb2.OperationResponse(
                result=result,
                success=True,
                error=""
            )
        except Exception as e:
            logger.error(f"❌ Erro na multiplicação: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0,
                success=False,
                error=str(e)
            )
    
    def Div(self, request, context):
        """
        Operação de Divisão com validação de divisão por zero
        Extra opcional
        
        Args:
            request: OperationRequest com num1 e num2
            context: Contexto gRPC
        Returns:
            OperationResponse com resultado ou erro
        """
        try:
            # Validação de entrada - divisão por zero
            if request.num2 == 0:
                error_msg = "Erro: Divisão por zero não permitida"
                logger.warning(f"⚠️  DIV: Tentativa de divisão por zero - {request.num1} / {request.num2}")
                
                # Define código de erro gRPC
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(error_msg)
                
                return calculator_pb2.OperationResponse(
                    result=0,
                    success=False,
                    error=error_msg
                )
            
            result = request.num1 / request.num2
            logger.info(f"➗ DIV: {request.num1} / {request.num2} = {result}")
            
            return calculator_pb2.OperationResponse(
                result=result,
                success=True,
                error=""
            )
        except Exception as e:
            logger.error(f"❌ Erro na divisão: {str(e)}")
            return calculator_pb2.OperationResponse(
                result=0,
                success=False,
                error=str(e)
            )


def serve():
    """
    Inicializa e executa o servidor gRPC
    """
    # Criação do servidor com interceptor de log
    interceptors = [LoggingInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors
    )
    
    # Registra o serviço
    calculator_pb2_grpc.add_CalculatorServicer_to_server(
        CalculatorService(), server
    )
    
    # Define porta
    port = '50051'
    server.add_insecure_port(f'[::]:{port}')
    
    # Inicia servidor
    server.start()
    logger.info(f"🚀 Servidor gRPC iniciado na porta {port}")
    logger.info(f"📡 Aguardando requisições...")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("\n🛑 Servidor encerrado pelo usuário")
        server.stop(0)


if __name__ == '__main__':
    serve()
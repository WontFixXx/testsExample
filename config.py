from dataclasses import dataclass

@dataclass
class ApiConfig:
    """Конфигурация для API подключений"""
    
    # gRPC API настройки
    grpc_host: str = "testHost"
    grpc_port: int = 443
    grpc_insecure: bool = False
    
    # HTTP REST API настройки
    http_host: str = "localhost"
    http_port: int = 10090
    
    @property
    def grpc_address(self) -> str:
        """Полный адрес gRPC сервера"""
        return f"{self.grpc_host}:{self.grpc_port}"
    
    @property
    def http_base_url(self) -> str:
        """Базовый URL для HTTP API"""
        return f"http://{self.http_host}:{self.http_port}/api/"


# Глобальная конфигурация по умолчанию
DEFAULT_CONFIG = ApiConfig()

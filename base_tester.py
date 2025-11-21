import json
import subprocess
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from config import DEFAULT_CONFIG, ApiConfig


@dataclass
class GrpcTestConfig:
    """Конфигурация для gRPC тестов (для обратной совместимости)"""
    host: str = DEFAULT_CONFIG.grpc_host
    port: int = DEFAULT_CONFIG.grpc_port
    insecure: bool = DEFAULT_CONFIG.grpc_insecure


@dataclass
class HttpTestConfig:
    """Конфигурация для HTTP тестов"""
    host: str = DEFAULT_CONFIG.http_host
    port: int = DEFAULT_CONFIG.http_port
    
    @property
    def base_url(self) -> str:
        """Базовый URL для HTTP API"""
        return f"http://{self.host}:{self.port}/api/"


class BaseGrpcTester:
    
    def __init__(self, config: GrpcTestConfig):
        self.config = config
        self.test_results = []
        self.http_config = HttpTestConfig(host=DEFAULT_CONFIG.http_host, port=DEFAULT_CONFIG.http_port)
    
    def run_grpcurl(self, service_method: str, payload: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
        
        cmd = [
            "grpcurl",
            "-emit-defaults",
            "-plaintext" if self.config.insecure else "",
            "-d", json.dumps(payload),
            f"{self.config.host}:{self.config.port}",
            service_method
        ]
        
        cmd = [arg for arg in cmd if arg]
        
        if verbose:
            print(f"🚀 Выполняем команду: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                if verbose:
                    print(f"❌ Ошибка выполнения grpcurl:")
                    print(f"   STDERR: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "stdout": result.stdout
                }
            
            try:
                response_data = json.loads(result.stdout)
                return {
                    "success": True,
                    "response": response_data,
                    "raw_stdout": result.stdout
                }
            except json.JSONDecodeError as e:
                if verbose:
                    print(f"❌ Ошибка парсинга JSON: {e}")
                    print(f"   Сырой ответ: {result.stdout}")
                return {
                    "success": False,
                    "error": f"JSON parse error: {e}",
                    "raw_stdout": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout: запрос выполнялся более 30 секунд"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Неожиданная ошибка: {e}"
            }
    
    def run_curl(self, method: str, url: str, payload: Dict[str, Any] = None, headers: Dict[str, str] = None, verbose: bool = True) -> Dict[str, Any]:
        """Выполняет HTTP запрос с помощью curl"""
        
        cmd = ["curl", "-s", "-X", method.upper()]
        
        # Добавляем заголовки
        if headers:
            for key, value in headers.items():
                cmd.extend(["-H", f"{key}: {value}"])
        
        # Добавляем Content-Type для JSON по умолчанию
        if payload and not (headers and any("content-type" in h.lower() for h in headers.keys())):
            cmd.extend(["-H", "Content-Type: application/json"])
        
        # Добавляем тело запроса
        if payload:
            cmd.extend(["-d", json.dumps(payload)])
        
        # Добавляем URL
        cmd.append(url)
        
        if verbose:
            print(f"🚀 Выполняем HTTP запрос: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                if verbose:
                    print(f"❌ Ошибка выполнения curl:")
                    print(f"   STDERR: {result.stderr}")
                return {
                    "success": False,
                    "error": result.stderr,
                    "stdout": result.stdout
                }
            
            # Проверяем, что ответ не пустой
            if not result.stdout.strip():
                if verbose:
                    print(f"❌ Пустой ответ от сервера")
                return {
                    "success": False,
                    "error": "Empty response from server",
                    "stdout": ""
                }
            
            try:
                response_data = json.loads(result.stdout)
                return {
                    "success": True,
                    "response": response_data,
                    "raw_stdout": result.stdout
                }
            except json.JSONDecodeError as e:
                if verbose:
                    print(f"❌ Ошибка парсинга JSON: {e}")
                    print(f"   Сырой ответ: {result.stdout}")
                return {
                    "success": False,
                    "error": f"JSON parse error: {e}",
                    "raw_stdout": result.stdout
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Timeout: запрос выполнялся более 30 секунд"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Неожиданная ошибка: {e}"
            }
    
    def assert_equal(self, actual: Any, expected: Any, message: str) -> bool:
        """Проверяет равенство значений"""
        if actual == expected:
            return True
        else:
            print(f"❌ {message}: {actual} != {expected}")
            self.test_results.append({
                "test": message, 
                "status": "FAIL", 
                "details": f"Ожидалось {expected}, получено {actual}"
            })
            return False
    
    def assert_has_property(self, obj: Dict[str, Any], prop: str, message: str) -> bool:
        if prop in obj:
            return True
        else:
            print(f"❌ {message}: свойство '{prop}' отсутствует")
            self.test_results.append({
                "test": message, 
                "status": "FAIL", 
                "details": f"Отсутствует свойство '{prop}'"
            })
            return False
    
    def assert_not_empty(self, value: Any, message: str) -> bool:
        if value and str(value).strip():
            return True
        else:
            print(f"❌ {message}: значение пустое")
            self.test_results.append({
                "test": message, 
                "status": "FAIL", 
                "details": "Значение пустое"
            })
            return False
    
    def assert_is_uuid(self, value: str, message: str) -> bool:
        import re
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        if uuid_pattern.match(value):
            return True
        else:
            print(f"❌ {message}: {value} не является UUID")
            self.test_results.append({
                "test": message, 
                "status": "FAIL", 
                "details": f"Значение {value} не является UUID"
            })
            return False
    
    def print_summary(self) -> bool:
        print("\n" + "=" * 60)
        print("📊 СВОДКА ПО ТЕСТАМ")
        print("=" * 60)
        
        passed = sum(1 for test in self.test_results if test["status"] == "PASS")
        failed = sum(1 for test in self.test_results if test["status"] == "FAIL")
        total = len(self.test_results)
        
        print(f"✅ Прошло: {passed}")
        print(f"❌ Провалено: {failed}")
        print(f"📊 Всего: {total}")
        
        if total > 0:
            success_rate = (passed / total) * 100
            print(f"🎯 Процент успеха: {success_rate:.1f}%")
        
        if failed > 0:
            print(f"\n❌ Провалившиеся тесты:")
            for test in self.test_results:
                if test["status"] == "FAIL":
                    print(f"   • {test['test']}: {test['details']}")
        
        return failed == 0


BaseOrdersApiTester = BaseGrpcTester
BaseOffersApiTester = BaseGrpcTester
BaseGrpcTester = BaseGrpcTester

OrdersApiTestConfig = GrpcTestConfig
OffersApiTestConfig = GrpcTestConfig
BlApiTestConfig = GrpcTestConfig

# Экспортируем новые классы
__all__ = [
    'BaseGrpcTester',
    'GrpcTestConfig', 
    'HttpTestConfig',
    'ApiConfig',
    'DEFAULT_CONFIG'
]
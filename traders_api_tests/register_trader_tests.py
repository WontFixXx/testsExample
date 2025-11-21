import uuid
import random
import string
from base_tester import BaseGrpcTester, GrpcTestConfig


class RegisterTraderTester(BaseGrpcTester):
    
    def __init__(self, config: GrpcTestConfig):
        super().__init__(config)
        # Используем HTTP конфигурацию из базового класса
        self.base_url = self.http_config.base_url
    
    def generate_random_email(self) -> str:
        """Генерирует случайный email в формате [random_8_symbols]@test.com"""
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_part}@test.com"
    
    def create_trader_via_http(self, user_id: str = None, email: str = None) -> dict:
        """Создает трейдера через HTTP API и возвращает результат"""
        if user_id is None:
            user_id = str(uuid.uuid4())
        if email is None:
            email = self.generate_random_email()
        
        payload = {
            "user_id": user_id,
            "email": email
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result = self.run_curl("POST", url, payload, verbose=False)
        
        return {
            "success": result["success"],
            "user_id": user_id,
            "email": email,
            "result": result
        }
    
    def test_register_trader_enabled(self) -> bool:
        """Тест регистрации трейдера со статусом ENABLED"""
        print(f"\n🧪 Тестируем регистрацию трейдера со статусом ENABLED")
        print("=" * 50)
        
        tests_passed = True
        
        print("📝 Шаг 1: Создаем трейдера через HTTP API")
        create_result = self.create_trader_via_http()
        
        if not create_result["success"]:
            print(f"❌ Ошибка создания трейдера: {create_result['result']['error']}")
            self.test_results.append({
                "test": "Register Trader Default",
                "status": "FAIL",
                "details": "Ошибка создания трейдера через HTTP"
            })
            return False
        
        trader_id = create_result["user_id"]
        trader_email = create_result["email"]
        print(f"✅ Трейдер создан успешно:")
        print(f"   trader_id: {trader_id}")
        print(f"   email: {trader_email}")
        
        print(f"\n📝 Шаг 2: Регистрируем трейдера через gRPC API")
        
        register_payload = {
            "commission_payin": 4.53,
            "commission_payout": 2.21,
            "currency_id": 3,
            "region_id": 8,
            "trader_id": trader_id,
            "trader_status": "TRADER_STATUS_ENABLED"
        }
        
        print(f"📊 Данные для регистрации: {register_payload}")
        
        result = self.run_grpcurl("RegisterTrader", register_payload)
        
        if result["success"]:
            response = result["response"]
            print(f"✅ Запрос выполнен успешно")
            print(f"📋 Ответ: {response}")
            
            # Проверяем структуру ответа
            tests_passed &= self.assert_has_property(response, "registerTraderResponse", "Ответ содержит поле 'registerTraderResponse'")
            
            if "registerTraderResponse" in response:
                register_response = response["registerTraderResponse"]
                tests_passed &= self.assert_has_property(register_response, "trader", "Ответ содержит поле 'trader'")
                
                if "trader" in register_response:
                    trader = register_response["trader"]
                    
                    # Проверяем основные поля
                    tests_passed &= self.assert_has_property(trader, "id", "Трейдер содержит поле 'id'")
                    tests_passed &= self.assert_has_property(trader, "email", "Трейдер содержит поле 'email'")
                    tests_passed &= self.assert_has_property(trader, "traderStatus", "Трейдер содержит поле 'traderStatus'")
                    tests_passed &= self.assert_has_property(trader, "hasActiveSessions", "Трейдер содержит поле 'hasActiveSessions'")
                    tests_passed &= self.assert_has_property(trader, "commissionPayin", "Трейдер содержит поле 'commissionPayin'")
                    tests_passed &= self.assert_has_property(trader, "commissionPayout", "Трейдер содержит поле 'commissionPayout'")
                    tests_passed &= self.assert_has_property(trader, "currencyId", "Трейдер содержит поле 'currencyId'")
                    tests_passed &= self.assert_has_property(trader, "regionId", "Трейдер содержит поле 'regionId'")
                    tests_passed &= self.assert_has_property(trader, "createdAt", "Трейдер содержит поле 'createdAt'")
                    tests_passed &= self.assert_has_property(trader, "updatedAt", "Трейдер содержит поле 'updatedAt'")
                    tests_passed &= self.assert_equal(trader["id"], trader_id, "ID трейдера соответствует отправленному")
                    tests_passed &= self.assert_equal(trader["email"], trader_email, "Email трейдера соответствует созданному")
                    tests_passed &= self.assert_equal(trader["traderStatus"], "TRADER_STATUS_ENABLED", "Статус трейдера = TRADER_STATUS_ENABLED")
                    tests_passed &= self.assert_equal(trader["hasActiveSessions"], False, "hasActiveSessions = false")
                    tests_passed &= self.assert_equal(trader["commissionPayin"], 4.53, "Commission payin = 4.53")
                    tests_passed &= self.assert_equal(trader["commissionPayout"], 2.21, "Commission payout = 2.21")
                    tests_passed &= self.assert_equal(trader["currencyId"], 3, "Currency ID = 3")
                    tests_passed &= self.assert_equal(trader["regionId"], 8, "Region ID = 8")
                    
                    # Проверяем timestamp поля (они должны быть не пустыми)
                    created_at = trader["createdAt"]
                    tests_passed &= self.assert_not_empty(created_at, "CreatedAt не пустое")
                    
                    updated_at = trader["updatedAt"]
                    tests_passed &= self.assert_not_empty(updated_at, "UpdatedAt не пустое")
        else:
            print(f"❌ Ошибка выполнения запроса: {result['error']}")
            if 'raw_stdout' in result:
                print(f"📋 Сырой ответ: {result['raw_stdout']}")
            tests_passed = False
        
        self.test_results.append({
            "test": "Register Trader Enabled",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Трейдер зарегистрирован со статусом ENABLED" if tests_passed else "Ошибка при регистрации трейдера"
        })
        
        return tests_passed
    
    def test_register_trader_disabled(self) -> bool:
        """Тест регистрации трейдера со статусом DISABLED"""
        print(f"\n🧪 Тестируем регистрацию трейдера со статусом DISABLED")
        print("=" * 50)
        
        tests_passed = True
        
        # Шаг 1: Создаем трейдера через HTTP API
        print("📝 Шаг 1: Создаем трейдера через HTTP API")
        create_result = self.create_trader_via_http()
        
        if not create_result["success"]:
            print(f"❌ Ошибка создания трейдера: {create_result['result']['error']}")
            self.test_results.append({
                "test": "Register Trader Disabled",
                "status": "FAIL",
                "details": "Ошибка создания трейдера через HTTP"
            })
            return False
        
        trader_id = create_result["user_id"]
        trader_email = create_result["email"]
        print(f"✅ Трейдер создан успешно:")
        print(f"   trader_id: {trader_id}")
        print(f"   email: {trader_email}")
        
        # Шаг 2: Регистрируем трейдера через gRPC API со статусом DISABLED
        print(f"\n📝 Шаг 2: Регистрируем трейдера через gRPC API со статусом DISABLED")
        
        register_payload = {
            "commission_payin": 3.75,
            "commission_payout": 1.85,
            "currency_id": 1,
            "region_id": 5,
            "trader_id": trader_id,
            "trader_status": "TRADER_STATUS_DISABLED"
        }
        
        print(f"📊 Данные для регистрации: {register_payload}")
        
        result = self.run_grpcurl("RegisterTrader", register_payload)
        
        if result["success"]:
            response = result["response"]
            print(f"✅ Запрос выполнен успешно")
            print(f"📋 Ответ: {response}")
            
            # Проверяем структуру ответа
            tests_passed &= self.assert_has_property(response, "registerTraderResponse", "Ответ содержит поле 'registerTraderResponse'")
            
            if "registerTraderResponse" in response:
                register_response = response["registerTraderResponse"]
                tests_passed &= self.assert_has_property(register_response, "trader", "Ответ содержит поле 'trader'")
                
                if "trader" in register_response:
                    trader = register_response["trader"]
                    
                    # Проверяем основные поля
                    tests_passed &= self.assert_has_property(trader, "id", "Трейдер содержит поле 'id'")
                    tests_passed &= self.assert_has_property(trader, "email", "Трейдер содержит поле 'email'")
                    tests_passed &= self.assert_has_property(trader, "traderStatus", "Трейдер содержит поле 'traderStatus'")
                    tests_passed &= self.assert_has_property(trader, "hasActiveSessions", "Трейдер содержит поле 'hasActiveSessions'")
                    tests_passed &= self.assert_has_property(trader, "commissionPayin", "Трейдер содержит поле 'commissionPayin'")
                    tests_passed &= self.assert_has_property(trader, "commissionPayout", "Трейдер содержит поле 'commissionPayout'")
                    tests_passed &= self.assert_has_property(trader, "currencyId", "Трейдер содержит поле 'currencyId'")
                    tests_passed &= self.assert_has_property(trader, "regionId", "Трейдер содержит поле 'regionId'")
                    tests_passed &= self.assert_has_property(trader, "createdAt", "Трейдер содержит поле 'createdAt'")
                    tests_passed &= self.assert_has_property(trader, "updatedAt", "Трейдер содержит поле 'updatedAt'")
                    
                    # Проверяем значения
                    tests_passed &= self.assert_equal(trader["id"], trader_id, "ID трейдера соответствует отправленному")
                    tests_passed &= self.assert_equal(trader["email"], trader_email, "Email трейдера соответствует созданному")
                    tests_passed &= self.assert_equal(trader["traderStatus"], "TRADER_STATUS_DISABLED", "Статус трейдера = TRADER_STATUS_DISABLED")
                    tests_passed &= self.assert_equal(trader["hasActiveSessions"], False, "hasActiveSessions = false")
                    tests_passed &= self.assert_equal(trader["commissionPayin"], 3.75, "Commission payin = 3.75")
                    tests_passed &= self.assert_equal(trader["commissionPayout"], 1.85, "Commission payout = 1.85")
                    tests_passed &= self.assert_equal(trader["currencyId"], 1, "Currency ID = 1")
                    tests_passed &= self.assert_equal(trader["regionId"], 5, "Region ID = 5")
                    
                    # Проверяем timestamp поля (они должны быть не пустыми)
                    created_at = trader["createdAt"]
                    tests_passed &= self.assert_not_empty(created_at, "CreatedAt не пустое")
                    
                    updated_at = trader["updatedAt"]
                    tests_passed &= self.assert_not_empty(updated_at, "UpdatedAt не пустое")
        else:
            print(f"❌ Ошибка выполнения запроса: {result['error']}")
            if 'raw_stdout' in result:
                print(f"📋 Сырой ответ: {result['raw_stdout']}")
            tests_passed = False
        
        self.test_results.append({
            "test": "Register Trader Disabled",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Трейдер зарегистрирован со статусом DISABLED" if tests_passed else "Ошибка при регистрации трейдера"
        })
        
        return tests_passed
    
    def test_register_trader_invalid_status(self) -> bool:
        """Тест регистрации трейдера с неверными статусами"""
        print(f"\n🧪 Тестируем регистрацию трейдера с неверными статусами")
        print("=" * 50)
        
        tests_passed = True
        
        # Шаг 1: Создаем трейдера через HTTP API
        print("📝 Шаг 1: Создаем трейдера через HTTP API")
        create_result = self.create_trader_via_http()
        
        if not create_result["success"]:
            print(f"❌ Ошибка создания трейдера: {create_result['result']['error']}")
            self.test_results.append({
                "test": "Register Trader Invalid Status",
                "status": "FAIL",
                "details": "Ошибка создания трейдера через HTTP"
            })
            return False
        
        trader_id = create_result["user_id"]
        trader_email = create_result["email"]
        print(f"✅ Трейдер создан успешно:")
        print(f"   trader_id: {trader_id}")
        print(f"   email: {trader_email}")
        
        # Шаг 2: Тестируем регистрацию с неверными статусами
        print(f"\n📝 Шаг 2: Тестируем регистрацию с неверными статусами")
        
        invalid_statuses = [
            "TRADER_STATUS_PAYOUT_OFF",
            "TRADER_STATUS_PAYIN_OFF", 
            "TRADER_STATUS_ON_HOLD",
            "TRADER_STATUS_UNINITIALIZED"
        ]
        
        expected_error_message = "register trader can only set status to ENABLED or DISABLED"
        
        for status in invalid_statuses:
            print(f"\n🔍 Тестируем статус: {status}")
            
            register_payload = {
                "commission_payin": 2.5,
                "commission_payout": 1.5,
                "currency_id": 2,
                "region_id": 3,
                "trader_id": trader_id,
                "trader_status": status
            }
            
            print(f"📊 Данные для регистрации: {register_payload}")
            
            result = self.run_grpcurl("RegisterTrader", register_payload)
            
            if result["success"]:
                response = result["response"]
                print(f"❌ Неожиданно: запрос выполнен успешно для статуса {status}")
                print(f"📋 Ответ: {response}")
                tests_passed = False
            else:
                # Ожидаем ошибку с определенным сообщением
                error_message = result.get('raw_stdout', result.get('error', ''))
                
                if expected_error_message in error_message:
                    print(f"✅ Получена ожидаемая ошибка для {status}: {error_message}")
                else:
                    print(f"❌ Получена неожиданная ошибка для {status}: {error_message}")
                    print(f"   Ожидалось: {expected_error_message}")
                    tests_passed = False
        
        self.test_results.append({
            "test": "Register Trader Invalid Status",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Все неверные статусы обработаны корректно" if tests_passed else "Один или несколько неверных статусов обработаны некорректно"
        })
        
        return tests_passed

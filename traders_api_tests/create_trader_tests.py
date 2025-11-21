import uuid
import random
import string
from base_tester import BaseGrpcTester, GrpcTestConfig


class CreateTraderTester(BaseGrpcTester):
    
    def __init__(self, config: GrpcTestConfig):
        super().__init__(config)
        # Используем HTTP конфигурацию из базового класса
        self.base_url = self.http_config.base_url
    
    def generate_random_email(self) -> str:
        """Генерирует случайный email в формате [random_8_symbols]@test.com"""
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_part}@test.com"
    
    def test_create_trader_default(self) -> bool:
        """Тест создания трейдера с валидными данными"""
        print(f"\n🧪 Тестируем создание трейдера")
        print("=" * 50)
        
        tests_passed = True
        
        # Генерируем данные для нового трейдера
        user_id = str(uuid.uuid4())
        email = self.generate_random_email()
        
        print(f"📧 Генерируем трейдера:")
        print(f"   user_id: {user_id}")
        print(f"   email: {email}")
        
        # Подготавливаем payload
        payload = {
            "user_id": user_id,
            "email": email
        }
        
        # Выполняем POST запрос
        url = f"{self.base_url}/traders/createTrader"
        result = self.run_curl("POST", url, payload)
        
        if result["success"]:
            response = result["response"]
            print(f"✅ Запрос выполнен успешно")
            print(f"📋 Ответ: {response}")
            
            # Проверяем структуру ответа
            tests_passed &= self.assert_has_property(response, "status", "Ответ содержит поле 'status'")
            tests_passed &= self.assert_has_property(response, "trader_id", "Ответ содержит поле 'trader_id'")
            
            # Проверяем значения
            if "status" in response:
                tests_passed &= self.assert_equal(response["status"], "created", "Статус равен 'created'")
            
            if "trader_id" in response:
                trader_id = response["trader_id"]
                tests_passed &= self.assert_not_empty(trader_id, "trader_id не пустой")
                tests_passed &= self.assert_is_uuid(trader_id, "trader_id является валидным UUID")
                
                # Дополнительно можем проверить, что вернулся тот же UUID, что мы отправили
                tests_passed &= self.assert_equal(trader_id, user_id, "trader_id соответствует отправленному user_id")
        else:
            print(f"❌ Ошибка выполнения запроса: {result['error']}")
            if 'raw_stdout' in result:
                print(f"📋 Сырой ответ: {result['raw_stdout']}")
            tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Трейдер создан успешно" if tests_passed else "Ошибка при создании трейдера"
        })
        
        return tests_passed
    
    def test_create_trader_duplicate_uuid(self) -> bool:
        """Тест создания двух трейдеров с одинаковым UUID, но разными email"""
        print(f"\n🧪 Тестируем создание трейдеров с дублирующимся UUID")
        print("=" * 50)
        
        tests_passed = True
        
        # Генерируем один UUID для двух трейдеров
        user_id = str(uuid.uuid4())
        email1 = self.generate_random_email()
        email2 = self.generate_random_email()
        
        print(f"📧 Создаем первого трейдера:")
        print(f"   user_id: {user_id}")
        print(f"   email: {email1}")
        
        # Создаем первого трейдера
        payload1 = {
            "user_id": user_id,
            "email": email1
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result1 = self.run_curl("POST", url, payload1)
        
        if result1["success"]:
            response1 = result1["response"]
            print(f"✅ Первый трейдер создан успешно: {response1}")
            
            # Теперь пытаемся создать второго трейдера с тем же UUID
            print(f"\n📧 Создаем второго трейдера с тем же UUID:")
            print(f"   user_id: {user_id}")
            print(f"   email: {email2}")
            
            payload2 = {
                "user_id": user_id,
                "email": email2
            }
            
            result2 = self.run_curl("POST", url, payload2)
            
            if result2["success"]:
                response2 = result2["response"]
                print(f"❌ Неожиданно: второй трейдер создан с дублирующимся UUID: {response2}")
                tests_passed = False
            else:
                # Ожидаем ошибку с текстом "trader already exists: user_id [uuid]"
                error_message = result2.get('raw_stdout', result2.get('error', ''))
                expected_error = f"trader already exists: user_id {user_id}"
                
                if expected_error in error_message:
                    print(f"✅ Получена ожидаемая ошибка: {error_message}")
                else:
                    print(f"❌ Получена неожиданная ошибка: {error_message}")
                    print(f"   Ожидалось: {expected_error}")
                    tests_passed = False
        else:
            print(f"❌ Ошибка создания первого трейдера: {result1['error']}")
            tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Duplicate UUID",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Дублирующийся UUID обработан корректно" if tests_passed else "Дублирующийся UUID обработан некорректно"
        })
        
        return tests_passed
    
    def test_create_trader_duplicate_email(self) -> bool:
        """Тест создания двух трейдеров с одинаковым email, но разными UUID"""
        print(f"\n🧪 Тестируем создание трейдеров с дублирующимся email")
        print("=" * 50)
        
        tests_passed = True
        
        # Генерируем один email для двух трейдеров
        user_id1 = str(uuid.uuid4())
        user_id2 = str(uuid.uuid4())
        email = self.generate_random_email()
        
        print(f"📧 Создаем первого трейдера:")
        print(f"   user_id: {user_id1}")
        print(f"   email: {email}")
        
        # Создаем первого трейдера
        payload1 = {
            "user_id": user_id1,
            "email": email
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result1 = self.run_curl("POST", url, payload1)
        
        if result1["success"]:
            response1 = result1["response"]
            print(f"✅ Первый трейдер создан успешно: {response1}")
            
            # Теперь пытаемся создать второго трейдера с тем же email
            print(f"\n📧 Создаем второго трейдера с тем же email:")
            print(f"   user_id: {user_id2}")
            print(f"   email: {email}")
            
            payload2 = {
                "user_id": user_id2,
                "email": email
            }
            
            result2 = self.run_curl("POST", url, payload2)
            
            if result2["success"]:
                response2 = result2["response"]
                print(f"❌ Неожиданно: второй трейдер создан с дублирующимся email: {response2}")
                tests_passed = False
            else:
                # Ожидаем ошибку с текстом "email already exists: email [email]"
                error_message = result2.get('raw_stdout', result2.get('error', ''))
                expected_error = f"email already exists: email {email}"
                
                if expected_error in error_message:
                    print(f"✅ Получена ожидаемая ошибка: {error_message}")
                else:
                    print(f"❌ Получена неожиданная ошибка: {error_message}")
                    print(f"   Ожидалось: {expected_error}")
                    tests_passed = False
        else:
            print(f"❌ Ошибка создания первого трейдера: {result1['error']}")
            tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Duplicate Email",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Дублирующийся email обработан корректно" if tests_passed else "Дублирующийся email обработан некорректно"
        })
        
        return tests_passed
    
    def test_create_trader_invalid_uuid(self) -> bool:
        """Тест создания трейдера с невалидным UUID"""
        print(f"\n🧪 Тестируем создание трейдера с невалидным UUID")
        print("=" * 50)
        
        tests_passed = True
        
        invalid_user_id = "7d9c2e4d-2a6f"  # Невалидный UUID (неполный)
        email = self.generate_random_email()
        
        print(f"📧 Пытаемся создать трейдера с невалидным UUID:")
        print(f"   user_id: {invalid_user_id}")
        print(f"   email: {email}")
        
        payload = {
            "user_id": invalid_user_id,
            "email": email
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result = self.run_curl("POST", url, payload)
        
        if result["success"]:
            response = result["response"]
            print(f"❌ Неожиданно: трейдер создан с невалидным UUID: {response}")
            tests_passed = False
        else:
            # Ожидаем ошибку с текстом "user_id must be a valid UUID"
            error_message = result.get('raw_stdout', result.get('error', ''))
            expected_error = "user_id must be a valid UUID"
            
            if expected_error in error_message:
                print(f"✅ Получена ожидаемая ошибка: {error_message}")
            else:
                print(f"❌ Получена неожиданная ошибка: {error_message}")
                print(f"   Ожидалось: {expected_error}")
                tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Invalid UUID",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Невалидный UUID обработан корректно" if tests_passed else "Невалидный UUID обработан некорректно"
        })
        
        return tests_passed
    
    def test_create_trader_empty_email(self) -> bool:
        """Тест создания трейдера с пустым email"""
        print(f"\n🧪 Тестируем создание трейдера с пустым email")
        print("=" * 50)
        
        tests_passed = True
        
        user_id = str(uuid.uuid4())
        empty_email = ""  # Пустая строка
        
        print(f"📧 Пытаемся создать трейдера с пустым email:")
        print(f"   user_id: {user_id}")
        print(f"   email: '{empty_email}'")
        
        payload = {
            "user_id": user_id,
            "email": empty_email
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result = self.run_curl("POST", url, payload)
        
        if result["success"]:
            response = result["response"]
            print(f"❌ Неожиданно: трейдер создан с пустым email: {response}")
            tests_passed = False
        else:
            # Ожидаем ошибку с текстом "email must be at least 1 character long"
            error_message = result.get('raw_stdout', result.get('error', ''))
            expected_error = "email must be at least 1 character long"
            
            if expected_error in error_message:
                print(f"✅ Получена ожидаемая ошибка: {error_message}")
            else:
                print(f"❌ Получена неожиданная ошибка: {error_message}")
                print(f"   Ожидалось: {expected_error}")
                tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Empty Email",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Пустой email обработан корректно" if tests_passed else "Пустой email обработан некорректно"
        })
        
        return tests_passed
    
    def test_create_trader_long_email(self) -> bool:
        """Тест создания трейдера с слишком длинным email (256 символов)"""
        print(f"\n🧪 Тестируем создание трейдера с слишком длинным email")
        print("=" * 50)
        
        tests_passed = True
        
        user_id = str(uuid.uuid4())
        # Создаем email длиной 256 символов
        long_prefix = 'a' * 247  # 247 символов
        long_email = f"{long_prefix}@test.com"  # 247 + 9 = 256 символов
        
        print(f"📧 Пытаемся создать трейдера с длинным email:")
        print(f"   user_id: {user_id}")
        print(f"   email: {long_email[:50]}...{long_email[-10:]} (длина: {len(long_email)})")
        
        payload = {
            "user_id": user_id,
            "email": long_email
        }
        
        url = f"{self.base_url}/traders/createTrader"
        result = self.run_curl("POST", url, payload)
        
        if result["success"]:
            response = result["response"]
            print(f"❌ Неожиданно: трейдер создан с длинным email: {response}")
            tests_passed = False
        else:
            # Ожидаем ошибку с текстом "email must be at most 255 characters long"
            error_message = result.get('raw_stdout', result.get('error', ''))
            expected_error = "email must be at most 255 characters long"
            
            if expected_error in error_message:
                print(f"✅ Получена ожидаемая ошибка: {error_message}")
            else:
                print(f"❌ Получена неожиданная ошибка: {error_message}")
                print(f"   Ожидалось: {expected_error}")
                tests_passed = False
        
        self.test_results.append({
            "test": "Create Trader Long Email",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Длинный email обработан корректно" if tests_passed else "Длинный email обработан некорректно"
        })
        
        return tests_passed

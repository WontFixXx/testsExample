from base_tester import BaseGrpcTester

class CurrencyTester(BaseGrpcTester):
    
    def _validate_grpc_response(self, result: dict, test_name: str) -> tuple[bool, dict]:
        if result is None:
            self.test_results.append({
                "test": test_name,
                "status": "FAIL",
                "details": "Не удалось выполнить запрос"
            })
            return False, {}
        
        if not result.get("success", False):
            self.test_results.append({
                "test": test_name,
                "status": "FAIL",
                "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
            })
            return False, {}
        
        return True, result.get("response", {})
    
    def _validate_currencies_response(self, response: dict, test_name: str) -> tuple[bool, list]:
        if "getCurrenciesResponse" not in response:
            self.test_results.append({
                "test": test_name,
                "status": "FAIL",
                "details": "Ответ не содержит getCurrenciesResponse"
            })
            return False, []
        
        currencies_response = response["getCurrenciesResponse"]
        currencies = currencies_response.get("currencies", [])
        
        if not currencies:
            self.test_results.append({
                "test": test_name,
                "status": "FAIL",
                "details": "Массив currencies пуст"
            })
            return False, []
        
        return True, currencies
    
    def _validate_currency_properties(self, currency: dict, test_name: str, expected_values: dict = None) -> bool:
        tests_passed = True

        tests_passed &= self.assert_has_property(currency, "id", f"{test_name}: Currency имеет поле id")
        tests_passed &= self.assert_has_property(currency, "code", f"{test_name}: Currency имеет поле code")
        tests_passed &= self.assert_has_property(currency, "currencyDecimalAccuracy", f"{test_name}: Currency имеет поле currencyDecimalAccuracy")
        tests_passed &= self.assert_has_property(currency, "isAccountCurrency", f"{test_name}: Currency имеет поле isAccountCurrency")
        
        if expected_values:
            for field, expected_value in expected_values.items():
                if field in currency:
                    tests_passed &= self.assert_equal(
                        currency.get(field), 
                        expected_value, 
                        f"{test_name}: Currency {field} = {expected_value}"
                    )
        
        return tests_passed
    
    def test_get_currency(self, currency_id: int = 1) -> bool:
        
        print(f"\n🧪 Тестируем GetCurrency с ID = {currency_id}")
        print("=" * 50)
        
        payload = {"id": currency_id}
        
        result = self.run_grpcurl("GetCurrency", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getCurrencyResponse" not in response:
            print("❌ Ответ не содержит getCurrencyResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getCurrencyResponse"
            })
            return False
        
        currency_response = response["getCurrencyResponse"]
        currency = currency_response.get("currency")
        
        if not currency:
            print("❌ Ответ не содержит currency")
            self.test_results.append({
                "test": "Наличие currency", 
                "status": "FAIL", 
                "details": "Отсутствует currency в ответе"
            })
            return False
        
        # Определяем ожидаемые значения в зависимости от ID валюты
        if currency_id == 1:
            expected_values = {
                "id": 1,
                "code": "USD",
                "currencyDecimalAccuracy": 2,
                "isAccountCurrency": True
            }
        elif currency_id == 15:
            expected_values = {
                "id": 15,
                "code": "BTC",
                "currencyDecimalAccuracy": 8,
                "isAccountCurrency": False
            }
        else:
            expected_values = None
        
        # Валидируем свойства валюты
        tests_passed = self._validate_currency_properties(currency, f"GetCurrency ID={currency_id}", expected_values)
        
        # Записываем результат
        self.test_results.append({
            "test": f"GetCurrency ID={currency_id}",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed
    
    def test_get_currency_error(self, currency_id: int = 100) -> bool:
        
        print(f"\n🧪 Тестируем GetCurrency с несуществующим ID = {currency_id}")
        print("=" * 50)
        
        payload = {"id": currency_id}
        
        result = self.run_grpcurl("GetCurrency", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetCurrency Error ID={currency_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "currency not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetCurrency Error ID={currency_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'currency not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetCurrency Error ID={currency_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
    
    def test_get_currencies_default(self) -> bool:
        try:
            print("🔍 Тестируем GetCurrencies без параметров...")
            
            payload = {}
            result = self.run_grpcurl("GetCurrencies", payload)
            
            # Валидируем gRPC ответ
            is_valid, response = self._validate_grpc_response(result, "GetCurrencies Default")
            if not is_valid:
                return False
            
            # Валидируем ответ с валютами
            is_valid, currencies = self._validate_currencies_response(response, "GetCurrencies Default")
            if not is_valid:
                return False
            
            if len(currencies) <= 1:
                self.test_results.append({
                    "test": "GetCurrencies Default",
                    "status": "FAIL",
                    "details": f"Ожидалось больше 1 валюты, получено {len(currencies)}"
                })
                return False
            
            first_currency = currencies[0]
            
            # Валидируем свойства первой валюты (только структуру)
            tests_passed = self._validate_currency_properties(first_currency, "GetCurrencies Default")
            
            # Если есть вторая валюта, проверяем её конкретные значения
            if len(currencies) > 1:
                btc_currency = currencies[1]
                btc_expected_values = {
                    "id": 15,
                    "code": "BTC",
                    "currencyDecimalAccuracy": 8,
                    "isAccountCurrency": False
                }
                tests_passed &= self._validate_currency_properties(btc_currency, "GetCurrencies Default BTC", btc_expected_values)
            
            self.test_results.append({
                "test": "GetCurrencies Default",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetCurrencies Default",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_currencies_order_code_desc(self) -> bool:
        try:
            print("🔍 Тестируем GetCurrencies с сортировкой по code DESC...")
            
            payload = {
                "order": {
                    "order_by": "code",
                    "order_desc": True
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            
            result = self.run_grpcurl("GetCurrencies", payload)
            
            # Валидируем gRPC ответ
            is_valid, response = self._validate_grpc_response(result, "GetCurrencies Order Code DESC")
            if not is_valid:
                return False
            
            # Валидируем ответ с валютами
            is_valid, currencies = self._validate_currencies_response(response, "GetCurrencies Order Code DESC")
            if not is_valid:
                return False
            
            first_currency = currencies[0]
            
            # Валидируем свойства валюты с ожидаемыми значениями для UZS
            uzs_expected_values = {
                "id": 13,
                "code": "UZS",
                "currencyDecimalAccuracy": 2,
                "isAccountCurrency": True
            }
            tests_passed = self._validate_currency_properties(first_currency, "GetCurrencies Order Code DESC", uzs_expected_values)
            
            self.test_results.append({
                "test": "GetCurrencies Order Code DESC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetCurrencies Order Code DESC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_currencies_order_decimal_asc(self) -> bool:
        try:
            print("🔍 Тестируем GetCurrencies с сортировкой по decimal ASC...")
            
            payload = {
                "order": {
                    "order_by": "currency_decimal_accuracy",
                    "order_desc": False
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            
            result = self.run_grpcurl("GetCurrencies", payload)
            
            # Валидируем gRPC ответ
            is_valid, response = self._validate_grpc_response(result, "GetCurrencies Order Decimal ASC")
            if not is_valid:
                return False
            
            # Валидируем ответ с валютами
            is_valid, currencies = self._validate_currencies_response(response, "GetCurrencies Order Decimal ASC")
            if not is_valid:
                return False
            
            first_currency = currencies[0]
            
            # Валидируем свойства валюты с ожидаемыми значениями для USD
            usd_expected_values = {
                "id": 1,
                "code": "USD",
                "currencyDecimalAccuracy": 2,
                "isAccountCurrency": True
            }
            tests_passed = self._validate_currency_properties(first_currency, "GetCurrencies Order Decimal ASC", usd_expected_values)
            
            self.test_results.append({
                "test": "GetCurrencies Order Decimal ASC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetCurrencies Order Decimal ASC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_currencies_pagination(self) -> bool:
        try:
            print("🔍 Тестируем GetCurrencies с пагинацией...")
            
            payload = {
                "pagination": {
                    "limit": "5",
                    "offset": "2"
                }
            }
            
            result = self.run_grpcurl("GetCurrencies", payload)
            
            # Валидируем gRPC ответ
            is_valid, response = self._validate_grpc_response(result, "GetCurrencies Pagination")
            if not is_valid:
                return False
            
            # Валидируем ответ с валютами
            is_valid, currencies = self._validate_currencies_response(response, "GetCurrencies Pagination")
            if not is_valid:
                return False
            
            # Получаем total_count для пагинации
            currencies_response = response["getCurrenciesResponse"]
            total_count = currencies_response.get("totalCount", 0)
            
            if len(currencies) != 5:
                self.test_results.append({
                    "test": "GetCurrencies Pagination",
                    "status": "FAIL",
                    "details": f"Ожидалось 5 валют, получено {len(currencies)}"
                })
                return False
            
            first_currency = currencies[0]
            
            # Валидируем свойства валюты с ожидаемыми значениями для INR
            inr_expected_values = {
                "id": 14,
                "code": "INR",
                "currencyDecimalAccuracy": 2,
                "isAccountCurrency": True
            }
            tests_passed = self._validate_currency_properties(first_currency, "GetCurrencies Pagination", inr_expected_values)
            
            # Проверяем total_count для пагинации
            tests_passed &= self.assert_equal(total_count, "16", "Total count = 16")
            
            self.test_results.append({
                "test": "GetCurrencies Pagination",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetCurrencies Pagination",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False

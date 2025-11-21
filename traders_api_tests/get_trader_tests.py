from base_tester import BaseGrpcTester

class GetTraderTester(BaseGrpcTester):
    
    def test_get_trader_default(self) -> bool:
        print(f"\n🧪 Тестируем GetTrader - базовый тест")
        print("=" * 50)
        
        payload = {
            "trader_id": "550e8400-e29b-41d4-a716-446655440001"
        }
        
        result = self.run_grpcurl("GetTrader", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getTraderResponse" not in response:
            print("❌ Ответ не содержит getTraderResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getTraderResponse"
            })
            return False
        
        get_trader_response = response["getTraderResponse"]
        trader = get_trader_response.get("trader")
        
        if not trader:
            print("❌ Ответ не содержит trader")
            self.test_results.append({
                "test": "Наличие trader", 
                "status": "FAIL", 
                "details": "Отсутствует trader в ответе"
            })
            return False
        
        tests_passed = True
        
        # Проверяем наличие всех обязательных полей
        tests_passed &= self.assert_has_property(trader, "id", "Trader имеет поле id")
        tests_passed &= self.assert_has_property(trader, "email", "Trader имеет поле email")
        tests_passed &= self.assert_has_property(trader, "traderStatus", "Trader имеет поле traderStatus")
        tests_passed &= self.assert_has_property(trader, "hasActiveSessions", "Trader имеет поле hasActiveSessions")
        tests_passed &= self.assert_has_property(trader, "commissionPayin", "Trader имеет поле commissionPayin")
        tests_passed &= self.assert_has_property(trader, "commissionPayout", "Trader имеет поле commissionPayout")
        tests_passed &= self.assert_has_property(trader, "currencyId", "Trader имеет поле currencyId")
        tests_passed &= self.assert_has_property(trader, "regionId", "Trader имеет поле regionId")
        tests_passed &= self.assert_has_property(trader, "createdAt", "Trader имеет поле createdAt")
        tests_passed &= self.assert_has_property(trader, "updatedAt", "Trader имеет поле updatedAt")
        
        # Проверяем значения полей
        tests_passed &= self.assert_equal(trader.get("id"), "550e8400-e29b-41d4-a716-446655440001", "Trader id соответствует запросу")
        tests_passed &= self.assert_equal(trader.get("email"), "trader1@test.com", "Trader email = trader1@test.com")
        tests_passed &= self.assert_equal(trader.get("traderStatus"), "TRADER_STATUS_ENABLED", "Trader status = TRADER_STATUS_ENABLED")
        tests_passed &= self.assert_equal(trader.get("hasActiveSessions"), False, "Trader hasActiveSessions = false")
        tests_passed &= self.assert_equal(trader.get("commissionPayin"), 3, "Trader commissionPayin = 3")
        tests_passed &= self.assert_equal(trader.get("commissionPayout"), 2.5, "Trader commissionPayout = 2.5")
        tests_passed &= self.assert_equal(trader.get("currencyId"), 3, "Trader currencyId = 3")
        tests_passed &= self.assert_equal(trader.get("regionId"), 8, "Trader regionId = 8")
        
        # Проверяем timestamps (приходят как ISO 8601 строки)
        created_at = trader.get("createdAt")
        if created_at:
            tests_passed &= self.assert_not_empty(created_at, "CreatedAt не пустое")
        
        updated_at = trader.get("updatedAt")
        if updated_at:
            tests_passed &= self.assert_not_empty(updated_at, "UpdatedAt не пустое")

        
        self.test_results.append({
            "test": "GetTrader Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_get_trader_not_found_error(self, trader_id: str = "550e8400-e29b-41d4-a716-446655440999") -> bool:
        print(f"\n🧪 Тестируем GetTrader с несуществующим ID = {trader_id}")
        print("=" * 50)
        
        payload = {"trader_id": trader_id}
        
        result = self.run_grpcurl("GetTrader", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "trader not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'trader not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False

    def test_get_trader_id_invalid_error(self, trader_id: str = "550e8400-e29b-41d4-a716") -> bool:
        print(f"\n🧪 Тестируем GetTrader с невалидным ID = {trader_id}")
        print("=" * 50)
        
        payload = {"trader_id": trader_id}
        
        result = self.run_grpcurl("GetTrader", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "trader id is not valid" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'trader not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetTrader Error ID={trader_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
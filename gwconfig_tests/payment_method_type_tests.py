from base_tester import BaseGrpcTester


class PaymentMethodTypeTester(BaseGrpcTester):
    
    def test_get_payment_method_type(self, payment_method_type_id: int = 1) -> bool:
        print(f"\n🧪 Тестируем GetPaymentMethodType с ID = {payment_method_type_id}")
        print("=" * 50)
        
        payload = {"id": payment_method_type_id}
        
        result = self.run_grpcurl("GetPaymentMethodType", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getPaymentMethodTypeResponse" not in response:
            print("❌ Ответ не содержит getPaymentMethodTypeResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getPaymentMethodTypeResponse"
            })
            return False
        
        payment_method_type_response = response["getPaymentMethodTypeResponse"]
        payment_method_type = payment_method_type_response.get("paymentMethodType")
        
        if not payment_method_type:
            print("❌ Ответ не содержит paymentMethodType")
            self.test_results.append({
                "test": "Наличие paymentMethodType", 
                "status": "FAIL", 
                "details": "Отсутствует paymentMethodType в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_has_property(payment_method_type, "id", "PaymentMethodType имеет поле id")
        tests_passed &= self.assert_has_property(payment_method_type, "paymentMethodTypeName", "PaymentMethodType имеет поле paymentMethodTypeName")
        tests_passed &= self.assert_has_property(payment_method_type, "validationRules", "PaymentMethodType имеет поле validationRules")
        
        if payment_method_type_id == 1:
            tests_passed &= self.assert_equal(payment_method_type.get("id"), 1, "PaymentMethodType id = 1")
            tests_passed &= self.assert_equal(payment_method_type.get("paymentMethodTypeName"), "Credit Card", "PaymentMethodType name = Credit Card")
            tests_passed &= self.assert_equal(payment_method_type.get("validationRules"), "{}", "PaymentMethodType validationRules = {}")
        elif payment_method_type_id == 2:
            tests_passed &= self.assert_equal(payment_method_type.get("id"), 2, "PaymentMethodType id = 2")
            tests_passed &= self.assert_equal(payment_method_type.get("paymentMethodTypeName"), "Instant Payment", "PaymentMethodType name = Instant Payment")
            tests_passed &= self.assert_equal(payment_method_type.get("validationRules"), "{}", "PaymentMethodType validationRules = {}")
        
        self.test_results.append({
            "test": f"GetPaymentMethodType ID={payment_method_type_id}",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed
    
    def test_get_payment_method_type_error(self, payment_method_type_id: int = 3) -> bool:
        print(f"\n🧪 Тестируем GetPaymentMethodType с несуществующим ID = {payment_method_type_id}")
        print("=" * 50)
        
        payload = {"id": payment_method_type_id}
        
        result = self.run_grpcurl("GetPaymentMethodType", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetPaymentMethodType Error ID={payment_method_type_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "payment method type not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetPaymentMethodType Error ID={payment_method_type_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'payment method type not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetPaymentMethodType Error ID={payment_method_type_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
    
    def test_get_payment_method_types_default(self) -> bool:
        try:
            print("🔍 Тестируем GetPaymentMethodTypes без параметров...")
            
            payload = {}
            
            result = self.run_grpcurl("GetPaymentMethodTypes", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Default",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Default",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getPaymentMethodTypesResponse" not in response:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Default",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodTypesResponse"
                })
                return False
            
            payment_method_types_response = response["getPaymentMethodTypesResponse"]
            payment_method_types = payment_method_types_response.get("paymentMethodTypes", [])
            
            if not payment_method_types:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Default",
                    "status": "FAIL",
                    "details": "Массив paymentMethodTypes пуст"
                })
                return False
            
            if len(payment_method_types) <= 1:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Default",
                    "status": "FAIL",
                    "details": f"Ожидалось больше 1 типа, получено {len(payment_method_types)}"
                })
                return False
            
            first_payment_method_type = payment_method_types[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_payment_method_type, "id", "PaymentMethodType имеет поле id")
            tests_passed &= self.assert_has_property(first_payment_method_type, "paymentMethodTypeName", "PaymentMethodType имеет поле paymentMethodTypeName")
            tests_passed &= self.assert_has_property(first_payment_method_type, "validationRules", "PaymentMethodType имеет поле validationRules")
            tests_passed &= self.assert_equal(first_payment_method_type.get("id"), 2, "PaymentMethodType id = 2")
            tests_passed &= self.assert_equal(first_payment_method_type.get("paymentMethodTypeName"), "Instant Payment", "PaymentMethodType name = Instant Payment")
            tests_passed &= self.assert_equal(first_payment_method_type.get("validationRules"), "{}", "PaymentMethodType validationRules = {}")

            self.test_results.append({
                "test": "GetPaymentMethodTypes Default",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethodTypes Default",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_payment_method_types_order_name_asc(self) -> bool:
        try:
            print("🔍 Тестируем GetPaymentMethodTypes с сортировкой по name ASC...")
            
            payload = {
                "order": {
                    "order_by": "payment_method_type_name",
                    "order_desc": False
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            
            result = self.run_grpcurl("GetPaymentMethodTypes", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Order Name ASC",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Order Name ASC",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getPaymentMethodTypesResponse" not in response:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Order Name ASC",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodTypesResponse"
                })
                return False
            
            payment_method_types_response = response["getPaymentMethodTypesResponse"]
            payment_method_types = payment_method_types_response.get("paymentMethodTypes", [])
            
            if not payment_method_types:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Order Name ASC",
                    "status": "FAIL",
                    "details": "Массив paymentMethodTypes пуст"
                })
                return False
            
            first_payment_method_type = payment_method_types[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_payment_method_type, "id", "PaymentMethodType имеет поле id")
            tests_passed &= self.assert_has_property(first_payment_method_type, "paymentMethodTypeName", "PaymentMethodType имеет поле paymentMethodTypeName")
            tests_passed &= self.assert_has_property(first_payment_method_type, "validationRules", "PaymentMethodType имеет поле validationRules")
            tests_passed &= self.assert_equal(first_payment_method_type.get("id"), 1, "PaymentMethodType id = 1")
            tests_passed &= self.assert_equal(first_payment_method_type.get("paymentMethodTypeName"), "Credit Card", "PaymentMethodType name = Credit Card")
            tests_passed &= self.assert_equal(first_payment_method_type.get("validationRules"), "{}", "PaymentMethodType validationRules = {}")
            
            self.test_results.append({
                "test": "GetPaymentMethodTypes Order Name ASC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethodTypes Order Name ASC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_payment_method_types_pagination(self) -> bool:
        try:
            print("🔍 Тестируем GetPaymentMethodTypes с пагинацией...")
            
            payload = {
                "pagination": {
                    "limit": "1",
                    "offset": "1"
                }
            }
            
            result = self.run_grpcurl("GetPaymentMethodTypes", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Pagination",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Pagination",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getPaymentMethodTypesResponse" not in response:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Pagination",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodTypesResponse"
                })
                return False
            
            payment_method_types_response = response["getPaymentMethodTypesResponse"]
            payment_method_types = payment_method_types_response.get("paymentMethodTypes", [])
            
            if not payment_method_types:
                self.test_results.append({
                    "test": "GetPaymentMethodTypes Pagination",
                    "status": "FAIL",
                    "details": "Массив paymentMethodTypes пуст"
                })
                return False
            if len(payment_method_types) != 1:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": f"Ожидалось 1 элемент, получено {len(payment_method_types)}"
                })
            
            first_payment_method_type = payment_method_types[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_payment_method_type, "id", "PaymentMethodType имеет поле id")
            tests_passed &= self.assert_has_property(first_payment_method_type, "paymentMethodTypeName", "PaymentMethodType имеет поле paymentMethodTypeName")
            tests_passed &= self.assert_has_property(first_payment_method_type, "validationRules", "PaymentMethodType имеет поле validationRules")
            tests_passed &= self.assert_equal(first_payment_method_type.get("id"), 1, "PaymentMethodType id = 1")
            tests_passed &= self.assert_equal(first_payment_method_type.get("paymentMethodTypeName"), "Credit Card", "PaymentMethodType name = Credit Card")
            tests_passed &= self.assert_equal(first_payment_method_type.get("validationRules"), "{}", "PaymentMethodType validationRules = {}")
            
            total_count = payment_method_types_response.get("totalCount")
            tests_passed &= self.assert_equal(total_count, "2", "totalCount = 2")

            self.test_results.append({
                "test": "GetPaymentMethodTypes Pagination",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethodTypes Pagination",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False

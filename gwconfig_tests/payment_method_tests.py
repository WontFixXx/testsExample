from base_tester import BaseGrpcTester
class PaymentMethodTester(BaseGrpcTester):
    
    def test_get_payment_method(self, payment_method_id: int = 1) -> bool:

        print(f"\n🧪 Тестируем GetPaymentMethod с ID = {payment_method_id}")
        print("=" * 50)
        payload = {"id": payment_method_id}
        result = self.run_grpcurl("GetPaymentMethod", payload)
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        response = result["response"]
        if "getPaymentMethodResponse" not in response:
            print("❌ Ответ не содержит getPaymentMethodResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getPaymentMethodResponse"
            })
            return False
        payment_method_response = response["getPaymentMethodResponse"]
        payment_method = payment_method_response.get("paymentMethod")
        if not payment_method:
            print("❌ Ответ не содержит paymentMethod")
            self.test_results.append({
                "test": "Наличие paymentMethod", 
                "status": "FAIL", 
                "details": "Отсутствует paymentMethod в ответе"
            })
            return False
        tests_passed = True
        tests_passed &= self.assert_has_property(payment_method, "id", "PaymentMethod имеет поле id")
        tests_passed &= self.assert_has_property(payment_method, "isActive", "PaymentMethod имеет поле isActive")
        tests_passed &= self.assert_has_property(payment_method, "direction", "PaymentMethod имеет поле direction")
        tests_passed &= self.assert_has_property(payment_method, "name", "PaymentMethod имеет поле name")
        tests_passed &= self.assert_has_property(payment_method, "regionId", "PaymentMethod имеет поле regionId")
        tests_passed &= self.assert_has_property(payment_method, "currencyId", "PaymentMethod имеет поле currencyId")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodTypeId", "PaymentMethod имеет поле paymentMethodTypeId")
        tests_passed &= self.assert_has_property(payment_method, "description", "PaymentMethod имеет поле description")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodLogoId", "PaymentMethod имеет поле paymentMethodLogoId")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodCode", "PaymentMethod имеет поле paymentMethodCode")
        tests_passed &= self.assert_has_property(payment_method, "issuerIds", "PaymentMethod имеет поле issuerIds")
        if payment_method_id == 1:
            tests_passed &= self.assert_equal(payment_method.get("id"), 1, "PaymentMethod id = 1")
            tests_passed &= self.assert_equal(payment_method.get("isActive"), True, "PaymentMethod isActive = true")
            tests_passed &= self.assert_equal(payment_method.get("direction"), "PAYIN", "PaymentMethod direction = PAYIN")
            tests_passed &= self.assert_equal(payment_method.get("name"), "Card Number", "PaymentMethod name = Card Number")
            tests_passed &= self.assert_equal(payment_method.get("regionId"), 8, "PaymentMethod regionId = 8")
            tests_passed &= self.assert_equal(payment_method.get("currencyId"), 3, "PaymentMethod currencyId = 3")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodTypeId"), 1, "PaymentMethod paymentMethodTypeId = 1")
            tests_passed &= self.assert_equal(payment_method.get("description"), "Card number payments in RUB", "PaymentMethod description = Card number payments in RUB")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodLogoId"), 1, "PaymentMethod paymentMethodLogoId = 1")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodCode"), "CARD_RUB", "PaymentMethod paymentMethodCode = CARD_RUB")
            tests_passed &= self.assert_equal(payment_method.get("issuerIds"), [1], "PaymentMethod issuerIds = [1]")
        elif payment_method_id == 26:
            tests_passed &= self.assert_equal(payment_method.get("id"), 26, "PaymentMethod id = 26")
            tests_passed &= self.assert_equal(payment_method.get("isActive"), True, "PaymentMethod isActive = true")
            tests_passed &= self.assert_equal(payment_method.get("direction"), "PAYOUT", "PaymentMethod direction = PAYOUT")
            tests_passed &= self.assert_equal(payment_method.get("name"), "Phone Number", "PaymentMethod name = Phone Number")
            tests_passed &= self.assert_equal(payment_method.get("regionId"), 7, "PaymentMethod regionId = 7")
            tests_passed &= self.assert_equal(payment_method.get("currencyId"), 10, "PaymentMethod currencyId = 10")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodTypeId"), 2, "PaymentMethod paymentMethodTypeId = 2")
            tests_passed &= self.assert_equal(payment_method.get("description"), "Phone number payouts in KZT", "PaymentMethod description = Phone number payouts in KZT")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodLogoId"), 4, "PaymentMethod paymentMethodLogoId = 4")
            tests_passed &= self.assert_equal(payment_method.get("paymentMethodCode"), "PHONE_PAYOUT_KZT", "PaymentMethod paymentMethodCode = PHONE_PAYOUT_KZT")
            tests_passed &= self.assert_equal(payment_method.get("issuerIds"), [], "PaymentMethod issuerIds = []")
        self.test_results.append({
            "test": f"GetPaymentMethod ID={payment_method_id}",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        return tests_passed
    def test_get_payment_method_error(self, payment_method_id: int = 1000) -> bool:

        print(f"\n🧪 Тестируем GetPaymentMethod с несуществующим ID = {payment_method_id}")
        print("=" * 50)
        payload = {"id": payment_method_id}
        result = self.run_grpcurl("GetPaymentMethod", payload)
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetPaymentMethod Error ID={payment_method_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        error_msg = result.get("error", "").lower()
        if "payment method not found" in error_msg or "not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetPaymentMethod Error ID={payment_method_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'payment method not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetPaymentMethod Error ID={payment_method_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
    def test_get_payment_methods_default(self) -> bool:

        try:
            print("🔍 Тестируем GetPaymentMethods без параметров...")
            payload = {}
            result = self.run_grpcurl("GetPaymentMethods", payload)
            if result is None:
                self.test_results.append({
                    "test": "GetPaymentMethods Default",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethods Default",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            response = result.get("response", {})
            if "getPaymentMethodsResponse" not in response:
                self.test_results.append({
                    "test": "GetPaymentMethods Default",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodsResponse"
                })
                return False
            payment_methods_response = response["getPaymentMethodsResponse"]
            payment_methods = payment_methods_response.get("paymentMethods", [])
            if not payment_methods:
                self.test_results.append({
                    "test": "GetPaymentMethods Default",
                    "status": "FAIL",
                    "details": "Массив paymentMethods пуст"
                })
                return False
            if len(payment_methods) <= 1:
                self.test_results.append({
                    "test": "GetPaymentMethods Default",
                    "status": "FAIL",
                    "details": f"Ожидалось больше 1 метода, получено {len(payment_methods)}"
                })
                return False
            first_payment_method = payment_methods[0]
            tests_passed = True
            tests_passed &= self.assert_has_property(first_payment_method, "id", "PaymentMethod имеет поле id")
            tests_passed &= self.assert_has_property(first_payment_method, "isActive", "PaymentMethod имеет поле isActive")
            tests_passed &= self.assert_has_property(first_payment_method, "direction", "PaymentMethod имеет поле direction")
            tests_passed &= self.assert_has_property(first_payment_method, "name", "PaymentMethod имеет поле name")
            tests_passed &= self.assert_has_property(first_payment_method, "regionId", "PaymentMethod имеет поле regionId")
            tests_passed &= self.assert_has_property(first_payment_method, "currencyId", "PaymentMethod имеет поле currencyId")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodTypeId", "PaymentMethod имеет поле paymentMethodTypeId")
            tests_passed &= self.assert_has_property(first_payment_method, "description", "PaymentMethod имеет поле description")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodLogoId", "PaymentMethod имеет поле paymentMethodLogoId")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodCode", "PaymentMethod имеет поле paymentMethodCode")
            tests_passed &= self.assert_has_property(first_payment_method, "issuerIds", "PaymentMethod имеет поле issuerIds")
            self.test_results.append({
                "test": "GetPaymentMethods Default",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethods Default",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    def test_get_payment_methods_order_id_desc(self) -> bool:

        try:
            print("🔍 Тестируем GetPaymentMethods с сортировкой по id DESC...")
            payload = {
                "order": {
                    "order_by": "id",
                    "order_desc": False
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            result = self.run_grpcurl("GetPaymentMethods", payload)
            if result is None:
                self.test_results.append({
                    "test": "GetPaymentMethods Order ID DESC",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethods Order ID DESC",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            response = result.get("response", {})
            if "getPaymentMethodsResponse" not in response:
                self.test_results.append({
                    "test": "GetPaymentMethods Order ID DESC",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodsResponse"
                })
                return False
            payment_methods_response = response["getPaymentMethodsResponse"]
            payment_methods = payment_methods_response.get("paymentMethods", [])
            if not payment_methods:
                self.test_results.append({
                    "test": "GetPaymentMethods Order ID DESC",
                    "status": "FAIL",
                    "details": "Массив paymentMethods пуст"
                })
                return False
            first_payment_method = payment_methods[0]
            tests_passed = True
            tests_passed &= self.assert_has_property(first_payment_method, "id", "PaymentMethod имеет поле id")
            tests_passed &= self.assert_has_property(first_payment_method, "isActive", "PaymentMethod имеет поле isActive")
            tests_passed &= self.assert_has_property(first_payment_method, "direction", "PaymentMethod имеет поле direction")
            tests_passed &= self.assert_has_property(first_payment_method, "name", "PaymentMethod имеет поле name")
            tests_passed &= self.assert_has_property(first_payment_method, "regionId", "PaymentMethod имеет поле regionId")
            tests_passed &= self.assert_has_property(first_payment_method, "currencyId", "PaymentMethod имеет поле currencyId")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodTypeId", "PaymentMethod имеет поле paymentMethodTypeId")
            tests_passed &= self.assert_has_property(first_payment_method, "description", "PaymentMethod имеет поле description")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodLogoId", "PaymentMethod имеет поле paymentMethodLogoId")
            tests_passed &= self.assert_has_property(first_payment_method, "paymentMethodCode", "PaymentMethod имеет поле paymentMethodCode")
            tests_passed &= self.assert_has_property(first_payment_method, "issuerIds", "PaymentMethod имеет поле issuerIds")
            tests_passed &= self.assert_equal(first_payment_method.get("id"), 1, "PaymentMethod id = 1")
            tests_passed &= self.assert_equal(first_payment_method.get("isActive"), True, "PaymentMethod isActive = true")
            tests_passed &= self.assert_equal(first_payment_method.get("direction"), "PAYIN", "PaymentMethod direction = PAYIN")
            tests_passed &= self.assert_equal(first_payment_method.get("name"), "Card Number", "PaymentMethod name = Card Number")
            tests_passed &= self.assert_equal(first_payment_method.get("regionId"), 8, "PaymentMethod regionId = 8")
            tests_passed &= self.assert_equal(first_payment_method.get("currencyId"), 3, "PaymentMethod currencyId = 3")
            tests_passed &= self.assert_equal(first_payment_method.get("paymentMethodTypeId"), 1, "PaymentMethod paymentMethodTypeId = 1")
            tests_passed &= self.assert_equal(first_payment_method.get("description"), "Card number payments in RUB", "PaymentMethod description = Card number payments in RUB")
            tests_passed &= self.assert_equal(first_payment_method.get("paymentMethodLogoId"), 1, "PaymentMethod paymentMethodLogoId = 1")
            tests_passed &= self.assert_equal(first_payment_method.get("paymentMethodCode"), "CARD_RUB", "PaymentMethod paymentMethodCode = CARD_RUB")
            tests_passed &= self.assert_equal(first_payment_method.get("issuerIds"), [1], "PaymentMethod issuerIds = [1]")
            self.test_results.append({
                "test": "GetPaymentMethods Order ID DESC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethods Order ID DESC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    def test_get_payment_methods_pagination(self) -> bool:
        try:
            print("🔍 Тестируем GetPaymentMethods с пагинацией...")
            
            # Шаг 1: Получаем все методы платежей без пагинации
            print("📋 Получаем все методы платежей...")
            result_all = self.run_grpcurl("GetPaymentMethods", {})
            if result_all is None or not result_all.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": "Не удалось получить все методы платежей"
                })
                return False
            
            response_all = result_all.get("response", {})
            if "getPaymentMethodsResponse" not in response_all:
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": "Ответ не содержит getPaymentMethodsResponse"
                })
                return False
            
            payment_methods_all = response_all["getPaymentMethodsResponse"].get("paymentMethods", [])
            total_count_all = response_all["getPaymentMethodsResponse"].get("totalCount", 0)
            
            if len(payment_methods_all) < 6:
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": f"Недостаточно методов для тестирования пагинации. Получено: {len(payment_methods_all)}"
                })
                return False
            
            # Сохраняем 5-й элемент (индекс 5, если считать с 0)
            element_5 = payment_methods_all[5] if len(payment_methods_all) > 5 else None
            
            # Шаг 2: Получаем методы с пагинацией (offset=5, limit=5)
            print("📄 Получаем методы с пагинацией (offset=5, limit=5)...")
            payload = {
                "pagination": {
                    "limit": "5",
                    "offset": "5"
                }
            }
            result_paginated = self.run_grpcurl("GetPaymentMethods", payload)
            if result_paginated is None or not result_paginated.get("success", False):
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос с пагинацией"
                })
                return False
            
            response_paginated = result_paginated.get("response", {})
            if "getPaymentMethodsResponse" not in response_paginated:
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": "Ответ с пагинацией не содержит getPaymentMethodsResponse"
                })
                return False
            
            payment_methods_paginated = response_paginated["getPaymentMethodsResponse"].get("paymentMethods", [])
            total_count_paginated = response_paginated["getPaymentMethodsResponse"].get("totalCount", 0)
            
            # Проверки
            tests_passed = True
            
            # Проверяем, что в пагинированном ответе ровно 5 элементов
            tests_passed &= self.assert_equal(len(payment_methods_paginated), 5, f"В пагинированном ответе должно быть 5 элементов, получено: {len(payment_methods_paginated)}")
            
            # Проверяем, что total_count не изменился
            tests_passed &= self.assert_equal(total_count_paginated, total_count_all, f"total_count должен остаться тем же: {total_count_all}, получен: {total_count_paginated}")
            
            # Проверяем, что первый элемент пагинированного ответа равен 5-му элементу полного ответа
            if element_5 and len(payment_methods_paginated) > 0:
                element_0_paginated = payment_methods_paginated[0]
                tests_passed &= self.assert_equal(element_0_paginated.get("id"), element_5.get("id"), f"Первый элемент пагинированного ответа должен быть равен 5-му элементу полного ответа. ID: {element_0_paginated.get('id')} vs {element_5.get('id')}")
                tests_passed &= self.assert_equal(element_0_paginated.get("name"), element_5.get("name"), f"Имена должны совпадать: {element_0_paginated.get('name')} vs {element_5.get('name')}")
            else:
                tests_passed = False
                self.test_results.append({
                    "test": "GetPaymentMethods Pagination",
                    "status": "FAIL",
                    "details": "Не удалось сравнить элементы - недостаточно данных"
                })
                return False

            self.test_results.append({
                "test": "GetPaymentMethods Pagination",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetPaymentMethods Pagination",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    def test_get_payment_methods_filter(self) -> bool:
        print(f"\n🧪 Тестируем GetPaymentMethods с различными фильтрами")
        print("=" * 50)
        
        tests_passed = True
        
        # Тест 1: Фильтр по currency_id = 3
        print("\n🔍 Тест 1: Фильтр по currency_id = 3")
        payload1 = {"filter": {"currency_id": 3}}
        result1 = self.run_grpcurl("GetPaymentMethods", payload1)
        
        if result1["success"]:
            response1 = result1["response"]
            if "getPaymentMethodsResponse" in response1:
                payment_methods1 = response1["getPaymentMethodsResponse"].get("paymentMethods", [])
                total_count1 = response1["getPaymentMethodsResponse"].get("totalCount", 0)
                print(f"📊 Найдено {len(payment_methods1)} методов платежей с currency_id = 3")
                print(f"📊 total_count = {total_count1}")
                
                # Проверяем, что total_count равен количеству элементов
                if int(total_count1) != len(payment_methods1):
                    print(f"❌ total_count ({total_count1}) не равен количеству элементов ({len(payment_methods1)})")
                    tests_passed = False
                else:
                    print(f"✅ total_count соответствует количеству элементов")
                
                # Проверяем, что все методы имеют currency_id = 3
                for i, method in enumerate(payment_methods1):
                    currency_id = method.get("currencyId")
                    if currency_id != 3:
                        print(f"❌ Метод {i+1} имеет currency_id = {currency_id}, ожидался 3")
                        tests_passed = False
                    else:
                        print(f"✅ Метод {i+1} ({method.get('name', 'unknown')}) currency_id = 3")
            else:
                print("❌ Неправильная структура ответа для currency_id фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с currency_id фильтром: {result1['error']}")
            tests_passed = False
        
        # Тест 2: Фильтр по direction = "PAYIN"
        print("\n🔍 Тест 2: Фильтр по direction = 'PAYIN'")
        payload2 = {"filter": {"direction": "PAYIN"}}
        result2 = self.run_grpcurl("GetPaymentMethods", payload2)
        
        if result2["success"]:
            response2 = result2["response"]
            if "getPaymentMethodsResponse" in response2:
                payment_methods2 = response2["getPaymentMethodsResponse"].get("paymentMethods", [])
                total_count2 = response2["getPaymentMethodsResponse"].get("totalCount", 0)
                print(f"📊 Найдено {len(payment_methods2)} методов платежей с direction = 'PAYIN'")
                print(f"📊 total_count = {total_count2}")
                
                # Проверяем, что total_count равен количеству элементов
                if int(total_count2) != len(payment_methods2):
                    print(f"❌ total_count ({total_count2}) не равен количеству элементов ({len(payment_methods2)})")
                    tests_passed = False
                else:
                    print(f"✅ total_count соответствует количеству элементов")
                
                # Проверяем, что все методы имеют direction = "PAYIN"
                for i, method in enumerate(payment_methods2):
                    direction = method.get("direction")
                    if direction != "PAYIN":
                        print(f"❌ Метод {i+1} имеет direction = {direction}, ожидался PAYIN")
                        tests_passed = False
                    else:
                        print(f"✅ Метод {i+1} ({method.get('name', 'unknown')}) direction = PAYIN")
            else:
                print("❌ Неправильная структура ответа для direction фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с direction фильтром: {result2['error']}")
            tests_passed = False
        
        # Тест 3: Фильтр по is_active = true
        print("\n🔍 Тест 3: Фильтр по is_active = true")
        payload3 = {"filter": {"is_active": True}}
        result3 = self.run_grpcurl("GetPaymentMethods", payload3)
        
        if result3["success"]:
            response3 = result3["response"]
            if "getPaymentMethodsResponse" in response3:
                payment_methods3 = response3["getPaymentMethodsResponse"].get("paymentMethods", [])
                total_count3 = response3["getPaymentMethodsResponse"].get("totalCount", 0)
                print(f"📊 Найдено {len(payment_methods3)} активных методов платежей")
                print(f"📊 total_count = {total_count3}")
                
                # Проверяем, что total_count равен количеству элементов
                if int(total_count3) != len(payment_methods3):
                    print(f"❌ total_count ({total_count3}) не равен количеству элементов ({len(payment_methods3)})")
                    tests_passed = False
                else:
                    print(f"✅ total_count соответствует количеству элементов")
                
                # Проверяем, что все методы активны
                for i, method in enumerate(payment_methods3):
                    is_active = method.get("isActive")
                    if is_active != True:
                        print(f"❌ Метод {i+1} имеет is_active = {is_active}, ожидался true")
                        tests_passed = False
                    else:
                        print(f"✅ Метод {i+1} ({method.get('name', 'unknown')}) is_active = true")
            else:
                print("❌ Неправильная структура ответа для is_active фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с is_active фильтром: {result3['error']}")
            tests_passed = False
        
        # Тест 4: Фильтр по payment_method_type_id = 1
        print("\n🔍 Тест 4: Фильтр по payment_method_type_id = 1")
        payload4 = {"filter": {"payment_method_type_id": 1}}
        result4 = self.run_grpcurl("GetPaymentMethods", payload4)
        
        if result4["success"]:
            response4 = result4["response"]
            if "getPaymentMethodsResponse" in response4:
                payment_methods4 = response4["getPaymentMethodsResponse"].get("paymentMethods", [])
                total_count4 = response4["getPaymentMethodsResponse"].get("totalCount", 0)
                print(f"📊 Найдено {len(payment_methods4)} методов платежей с payment_method_type_id = 1")
                print(f"📊 total_count = {total_count4}")
                
                # Проверяем, что total_count равен количеству элементов
                if int(total_count4) != len(payment_methods4):
                    print(f"❌ total_count ({total_count4}) не равен количеству элементов ({len(payment_methods4)})")
                    tests_passed = False
                else:
                    print(f"✅ total_count соответствует количеству элементов")
                
                # Проверяем, что все методы имеют payment_method_type_id = 1
                for i, method in enumerate(payment_methods4):
                    type_id = method.get("paymentMethodTypeId")
                    if type_id != 1:
                        print(f"❌ Метод {i+1} имеет payment_method_type_id = {type_id}, ожидался 1")
                        tests_passed = False
                    else:
                        print(f"✅ Метод {i+1} ({method.get('name', 'unknown')}) payment_method_type_id = 1")
            else:
                print("❌ Неправильная структура ответа для payment_method_type_id фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с payment_method_type_id фильтром: {result4['error']}")
            tests_passed = False
        
        # Тест 5: Фильтр по region_id = 8
        print("\n🔍 Тест 5: Фильтр по region_id = 8")
        payload5 = {"filter": {"region_id": 8}}
        result5 = self.run_grpcurl("GetPaymentMethods", payload5)
        
        if result5["success"]:
            response5 = result5["response"]
            if "getPaymentMethodsResponse" in response5:
                payment_methods5 = response5["getPaymentMethodsResponse"].get("paymentMethods", [])
                total_count5 = response5["getPaymentMethodsResponse"].get("totalCount", 0)
                print(f"📊 Найдено {len(payment_methods5)} методов платежей с region_id = 8")
                print(f"📊 total_count = {total_count5}")
                
                # Проверяем, что total_count равен количеству элементов
                if int(total_count5) != len(payment_methods5):
                    print(f"❌ total_count ({total_count5}) не равен количеству элементов ({len(payment_methods5)})")
                    tests_passed = False
                else:
                    print(f"✅ total_count соответствует количеству элементов")
                
                # Проверяем, что все методы имеют region_id = 8
                for i, method in enumerate(payment_methods5):
                    region_id = method.get("regionId")
                    if region_id != 8:
                        print(f"❌ Метод {i+1} имеет region_id = {region_id}, ожидался 8")
                        tests_passed = False
                    else:
                        print(f"✅ Метод {i+1} ({method.get('name', 'unknown')}) region_id = 8")
            else:
                print("❌ Неправильная структура ответа для region_id фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с region_id фильтром: {result5['error']}")
            tests_passed = False

        self.test_results.append({
            "test": "GetPaymentMethods Filter",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        return tests_passed

    def test_create_payment_method_default(self) -> bool:
        print(f"\n🧪 Тестируем создание PaymentMethod - базовый тест")
        print("=" * 50)

        payload1 = {}
        last_id = self.run_grpcurl("GetPaymentMethods", payload1)
        last_id = last_id.get("response", {}).get("getPaymentMethodsResponse", {}).get("paymentMethods", [{}])[0].get("id")
        print(f"🔍 Последний ID: {last_id}")
        
        payload = {
                "currency_id": 3,
                "description": "test_new_pm",
                "direction": "PAYIN",
                "is_active": False,
                "issuer_ids": [1, 2, 3],
                "name": "test_new_pm1",
                "payment_method_code": "test_new_pm2",
                "payment_method_logo_id": 1,
                "payment_method_type_id": 1,
                "region_id": 8
        }
        
        result = self.run_grpcurl("CreatePaymentMethod", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "createPaymentMethodResponse" not in response:
            print("❌ Ответ не содержит createPaymentMethodResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует createPaymentMethodResponse"
            })
            return False
        
        create_payment_method_response = response["createPaymentMethodResponse"]
        payment_method = create_payment_method_response.get("paymentMethod")
        
        if not payment_method:
            print("❌ Ответ не содержит paymentMethod")
            self.test_results.append({
                "test": "Наличие paymentMethod", 
                "status": "FAIL", 
                "details": "Отсутствует paymentMethod в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_has_property(payment_method, "id", "paymentMethod имеет поле id")
        tests_passed &= self.assert_has_property(payment_method, "isActive", "paymentMethod имеет поле isActive")
        tests_passed &= self.assert_has_property(payment_method, "direction", "paymentMethod имеет поле direction")
        tests_passed &= self.assert_has_property(payment_method, "name", "paymentMethod имеет поле name")
        tests_passed &= self.assert_has_property(payment_method, "regionId", "paymentMethod имеет поле regionId")
        tests_passed &= self.assert_has_property(payment_method, "currencyId", "paymentMethod имеет поле currencyId")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodTypeId", "paymentMethod имеет поле paymentMethodTypeId")
        tests_passed &= self.assert_has_property(payment_method, "description", "paymentMethod имеет поле description")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodLogoId", "paymentMethod имеет поле paymentMethodLogoId")
        tests_passed &= self.assert_has_property(payment_method, "paymentMethodCode", "paymentMethod имеет поле paymentMethodCode")
        
        tests_passed &= self.assert_equal(payment_method.get("id"), last_id+1, f"id = {last_id+1}")
        tests_passed &= self.assert_equal(payment_method.get("isActive"), False, "isActive = false")
        tests_passed &= self.assert_equal(payment_method.get("direction"), "PAYIN", "direction = PAYIN")
        tests_passed &= self.assert_equal(payment_method.get("name"), "test_new_pm1", "name = test_new_pm1")
        tests_passed &= self.assert_equal(payment_method.get("regionId"), 8, "regionId = 8")
        tests_passed &= self.assert_equal(payment_method.get("currencyId"), 3, "currencyId = 3")
        tests_passed &= self.assert_equal(payment_method.get("paymentMethodTypeId"), 1, "paymentMethodTypeId = 1")
        tests_passed &= self.assert_equal(payment_method.get("description"), "test_new_pm", "description = test_new_pm")
        tests_passed &= self.assert_equal(payment_method.get("paymentMethodLogoId"), 1, "paymentMethodLogoId = 1")
        tests_passed &= self.assert_equal(payment_method.get("paymentMethodCode"), "test_new_pm2", "paymentMethodCode = test_new_pm2")
        
        issuer_ids = payment_method.get("issuerIds", [])
        if issuer_ids:
            tests_passed &= self.assert_equal(issuer_ids[0], 1, "issuerIds[0] = 1")
            tests_passed &= self.assert_equal(issuer_ids[1], 2, "issuerIds[1] = 2")
            tests_passed &= self.assert_equal(issuer_ids[2], 3, "issuerIds[2] = 3")
        
        self.test_results.append({
            "test": "CreateOrder Basic",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

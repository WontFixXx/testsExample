import uuid
from base_tester import BaseOrdersApiTester

class CreateOrderTester(BaseOrdersApiTester):
    
    def test_create_order_basic(self) -> bool:
        print(f"\n🧪 Тестируем CreateOrder - базовый тест")
        print("=" * 50)
        
        payload = {
            "company_id": 1,
            "external_client_id": str(uuid.uuid4()),
            "external_order_id": f"external_id_{uuid.uuid4().hex[:8]}",
            "amount": 12000,
            "callback_url": "http://example.com/callback",
            "success_url": "http://example.com/success",
            "fail_url": "http://example.com/fail",
            "correlation_id": "random",
            "payment_method_id": 2
        }
        
        result = self.run_grpcurl("CreateOrder", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "createOrderResponse" not in response:
            print("❌ Ответ не содержит createOrderResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует createOrderResponse"
            })
            return False
        
        create_order_response = response["createOrderResponse"]
        order = create_order_response.get("order")
        
        if not order:
            print("❌ Ответ не содержит order")
            self.test_results.append({
                "test": "Наличие order", 
                "status": "FAIL", 
                "details": "Отсутствует order в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_has_property(order, "orderId", "Order имеет поле orderId")
        tests_passed &= self.assert_has_property(order, "amount", "Order имеет поле amount")
        tests_passed &= self.assert_has_property(order, "status", "Order имеет поле status")
        tests_passed &= self.assert_has_property(order, "createdAt", "Order имеет поле createdAt")
        tests_passed &= self.assert_has_property(order, "externalOrderId", "Order имеет поле externalOrderId")
        tests_passed &= self.assert_has_property(order, "paymentDetails", "Order имеет поле paymentDetails")
        
        tests_passed &= self.assert_is_uuid(order.get("orderId", ""), "Order ID является UUID")
        tests_passed &= self.assert_equal(order.get("amount"), "12000", "Order amount = 12000")
        tests_passed &= self.assert_equal(order.get("status"), "PENDING", "Order status = PENDING")
        tests_passed &= self.assert_not_empty(order.get("createdAt"), "Order createdAt не пустое")
        tests_passed &= self.assert_equal(order.get("externalOrderId"), payload["external_order_id"], "Order externalOrderId соответствует запросу")
        
        payment_details = order.get("paymentDetails", {})
        if payment_details:
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsOwnerName", "PaymentDetails имеет поле paymentDetailsOwnerName")
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsAuxiliaryData", "PaymentDetails имеет поле paymentDetailsAuxiliaryData")
            tests_passed &= self.assert_has_property(payment_details, "paymentDirection", "PaymentDetails имеет поле paymentDirection")
            tests_passed &= self.assert_has_property(payment_details, "currencyId", "PaymentDetails имеет поле currencyId")
            tests_passed &= self.assert_has_property(payment_details, "paymentMethodId", "PaymentDetails имеет поле paymentMethodId")
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsValue", "PaymentDetails имеет поле paymentDetailsValue")
            
            tests_passed &= self.assert_equal(payment_details.get("paymentDirection"), "PAYIN", "PaymentDetails direction = PAYIN")
            tests_passed &= self.assert_equal(payment_details.get("currencyId"), 3, "PaymentDetails currencyId = 3")
            tests_passed &= self.assert_equal(payment_details.get("paymentMethodId"), 2, "PaymentDetails paymentMethodId = 2")
        
        self.test_results.append({
            "test": "CreateOrder Basic",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_create_payout_order_basic(self) -> bool:
        print(f"\n🧪 Тестируем payout CreateOrder - базовый тест")
        print("=" * 50)
        
        payload = {
            "company_id": 1,
            "amount": 12000,
            "payment_details": {
                "payment_details_value": "123",
                "payment_details_auxiliary_data": "123",
                "payment_details_owner_name": "123",
                "issuer_id": 1,
                "issuer_name": "123"
                },
            "external_client_id": str(uuid.uuid4()),
            "external_order_id": f"external_id_{uuid.uuid4().hex[:8]}",
            "callback_url": "https://mock-callback.int.stage.cashierplus.online/callback",
            "success_url": "http://example.com/success",
            "fail_url": "http://example.com/fail",
            "correlation_id": "random",
            "payment_method_id": 8
        }
        
        result = self.run_grpcurl("CreateOrder", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "createOrderResponse" not in response:
            print("❌ Ответ не содержит createOrderResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует createOrderResponse"
            })
            return False
        
        create_order_response = response["createOrderResponse"]
        order = create_order_response.get("order")
        
        if not order:
            print("❌ Ответ не содержит order")
            self.test_results.append({
                "test": "Наличие order", 
                "status": "FAIL", 
                "details": "Отсутствует order в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_has_property(order, "orderId", "Order имеет поле orderId")
        tests_passed &= self.assert_has_property(order, "amount", "Order имеет поле amount")
        tests_passed &= self.assert_has_property(order, "status", "Order имеет поле status")
        tests_passed &= self.assert_has_property(order, "createdAt", "Order имеет поле createdAt")
        tests_passed &= self.assert_has_property(order, "externalOrderId", "Order имеет поле externalOrderId")
        tests_passed &= self.assert_has_property(order, "paymentDetails", "Order имеет поле paymentDetails")
        
        tests_passed &= self.assert_is_uuid(order.get("orderId", ""), "Order ID является UUID")
        tests_passed &= self.assert_equal(order.get("amount"), "12000", "Order amount = 12000")
        tests_passed &= self.assert_equal(order.get("status"), "PENDING", "Order status = PENDING")
        tests_passed &= self.assert_not_empty(order.get("createdAt"), "Order createdAt не пустое")
        tests_passed &= self.assert_equal(order.get("externalOrderId"), payload["external_order_id"], "Order externalOrderId соответствует запросу")
        
        payment_details = order.get("paymentDetails", {})
        if payment_details:
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsOwnerName", "PaymentDetails имеет поле paymentDetailsOwnerName")
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsAuxiliaryData", "PaymentDetails имеет поле paymentDetailsAuxiliaryData")
            tests_passed &= self.assert_has_property(payment_details, "paymentDirection", "PaymentDetails имеет поле paymentDirection")
            tests_passed &= self.assert_has_property(payment_details, "currencyId", "PaymentDetails имеет поле currencyId")
            tests_passed &= self.assert_has_property(payment_details, "paymentMethodId", "PaymentDetails имеет поле paymentMethodId")
            tests_passed &= self.assert_has_property(payment_details, "paymentDetailsValue", "PaymentDetails имеет поле paymentDetailsValue")
            tests_passed &= self.assert_has_property(payment_details, "issuerId", "PaymentDetails имеет поле issuerId")
            tests_passed &= self.assert_has_property(payment_details, "issuerName", "PaymentDetails имеет поле issuerName")
            tests_passed &= self.assert_has_property(payment_details, "issuerType", "PaymentDetails имеет поле issuerType")
            
            tests_passed &= self.assert_equal(payment_details.get("paymentDirection"), "PAYOUT", "PaymentDetails direction = PAYOUT")
            tests_passed &= self.assert_equal(payment_details.get("currencyId"), 3, "PaymentDetails currencyId = 3")
            tests_passed &= self.assert_equal(payment_details.get("paymentMethodId"), 8, "PaymentDetails paymentMethodId = 8")
            tests_passed &= self.assert_equal(payment_details.get("paymentDetailsOwnerName"), payload["payment_details"]["payment_details_owner_name"], "paymentDetailsOwnerName соответствует запросу")
            tests_passed &= self.assert_equal(payment_details.get("paymentDetailsAuxiliaryData"), payload["payment_details"]["payment_details_auxiliary_data"], "paymentDetailsAuxiliaryData соответствует запросу")
            tests_passed &= self.assert_equal(payment_details.get("paymentDetailsValue"), payload["payment_details"]["payment_details_value"], "paymentDetailsValue соответствует запросу")
            tests_passed &= self.assert_equal(payment_details.get("issuerId"), payload["payment_details"]["issuer_id"], "issuerId соответствует запросу")
            tests_passed &= self.assert_equal(payment_details.get("issuerName"), payload["payment_details"]["issuer_name"], "issuerName соответствует запросу")
            tests_passed &= self.assert_equal(payment_details.get("issuerType"), "bank", "issuerType = bank")
        
        self.test_results.append({
            "test": "CreateOrder Basic",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_create_order_payin_min_amount_error(self) -> bool:
        print(f"\n🧪 Тестируем CreateOrder - проверка ошибки при запросе с суммой меньше минимальной")
        print("=" * 50)
        
        payload = {
            "company_id": 1,
            "external_client_id": str(uuid.uuid4()),
            "external_order_id": f"external_id_{uuid.uuid4().hex[:8]}",
            "amount": 10,
            "callback_url": "http://example.com/callback",
            "success_url": "http://example.com/success",
            "fail_url": "http://example.com/fail",
            "correlation_id": "random",
            "payment_method_id": 2
        }
        
        result = self.run_grpcurl("CreateOrder", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "createOrderResponse" not in response:
            print("❌ Ответ не содержит createOrderResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует createOrderResponse"
            })
            return False
        
        create_order_response = response["createOrderResponse"]
        order = create_order_response.get("order")
        decline_reason_code = create_order_response.get("declineReasonCode")
        decline_description = create_order_response.get("declineDescription")
        
        if not decline_reason_code:
            print("❌ Ответ не содержит declineReasonCode")
            self.test_results.append({
                "test": "Наличие declineReasonCode", 
                "status": "FAIL", 
                "details": "Отсутствует declineReasonCode в ответе"
            })
            return False
        
        if not decline_description:
            print("❌ Ответ не содержит declineDescription")
            self.test_results.append({
                "test": "Наличие declineDescription", 
                "status": "FAIL", 
                "details": "Отсутствует declineDescription в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_equal(decline_reason_code, "INVALID_AMOUNT", "Order decline_reason_code = INVALID_AMOUNT")
        tests_passed &= self.assert_equal(decline_description, "Invalid order amount", "Order decline_description = Invalid order amount")
        tests_passed &= self.assert_equal(order.get("status"), "DECLINED", "Order status = DECLINED")
        tests_passed &= self.assert_equal(order.get("declineCancelCode"), "INVALID_AMOUNT", "Order decline_cancel_code = INVALID_AMOUNT")
        
        self.test_results.append({
            "test": "CreateOrder PayIn Min Amount Error",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_create_order_payin_max_amount_error(self) -> bool:
        print(f"\n🧪 Тестируем CreateOrder - проверка ошибки при запросе с суммой больше максимальной")
        print("=" * 50)
        
        payload = {
            "company_id": 1,
            "external_client_id": str(uuid.uuid4()),
            "external_order_id": f"external_id_{uuid.uuid4().hex[:8]}",
            "amount": 50001,
            "callback_url": "http://example.com/callback",
            "success_url": "http://example.com/success",
            "fail_url": "http://example.com/fail",
            "correlation_id": "random",
            "payment_method_id": 2
        }
        
        result = self.run_grpcurl("CreateOrder", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "createOrderResponse" not in response:
            print("❌ Ответ не содержит createOrderResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует createOrderResponse"
            })
            return False
        
        create_order_response = response["createOrderResponse"]
        order = create_order_response.get("order")
        decline_reason_code = create_order_response.get("declineReasonCode")
        decline_description = create_order_response.get("declineDescription")
        
        if not decline_reason_code:
            print("❌ Ответ не содержит declineReasonCode")
            self.test_results.append({
                "test": "Наличие declineReasonCode", 
                "status": "FAIL", 
                "details": "Отсутствует declineReasonCode в ответе"
            })
            return False
        
        if not decline_description:
            print("❌ Ответ не содержит declineDescription")
            self.test_results.append({
                "test": "Наличие declineDescription", 
                "status": "FAIL", 
                "details": "Отсутствует declineDescription в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_equal(decline_reason_code, "INVALID_AMOUNT", "Order decline_reason_code = INVALID_AMOUNT")
        tests_passed &= self.assert_equal(decline_description, "Invalid order amount", "Order decline_description = Invalid order amount")
        tests_passed &= self.assert_equal(order.get("status"), "DECLINED", "Order status = DECLINED")
        tests_passed &= self.assert_equal(order.get("declineCancelCode"), "INVALID_AMOUNT", "Order decline_cancel_code = INVALID_AMOUNT")
        
        self.test_results.append({
            "test": "CreateOrder PayIn Min Amount Error",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_create_order_non_existing_company_error(self) -> bool:
        print(f"\n🧪 Тестируем CreateOrder - проверка ошибки при запросе с несуществующим company_id")
        print("=" * 50)
        
        payload = {
            "company_id": 100,
            "external_client_id": str(uuid.uuid4()),
            "external_order_id": f"external_id_{uuid.uuid4().hex[:8]}",
            "amount": 12000,
            "callback_url": "http://example.com/callback",
            "success_url": "http://example.com/success",
            "fail_url": "http://example.com/fail",
            "correlation_id": "random",
            "payment_method_id": 2
        }
        
        result = self.run_grpcurl("CreateOrder", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"CreateOrder Non Existing Company Error",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "invalid company id" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"CreateOrder Non Existing Company Error",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid company id'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"CreateOrder Non Existing Company Error",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
from base_tester import BaseGrpcTester

class IssuerTester(BaseGrpcTester):

    def test_get_issuer(self, issuer_id: int = 1) -> bool:
        print(f"\n🧪 Тестируем GetIssuer с ID = {issuer_id}")
        print("=" * 50)

        payload = {"id": issuer_id}

        result = self.run_grpcurl("GetIssuer", payload)

        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        response = result["response"]
        if "getIssuerResponse" not in response:
            print("❌ Ответ не содержит getIssuerResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getIssuerResponse"
            })
            return False
        issuer_response = response["getIssuerResponse"]
        issuer = issuer_response.get("issuer")
        if not issuer:
            print("❌ Ответ не содержит issuer")
            self.test_results.append({
                "test": "Наличие issuer", 
                "status": "FAIL", 
                "details": "Отсутствует issuer в ответе"
            })
            return False
        tests_passed = True
        tests_passed &= self.assert_has_property(issuer, "id", "Issuer имеет поле id")
        tests_passed &= self.assert_has_property(issuer, "issuerName", "Issuer имеет поле issuerName")
        tests_passed &= self.assert_has_property(issuer, "issuerType", "Issuer имеет поле issuerType")
        tests_passed &= self.assert_has_property(issuer, "issuerCode", "Issuer имеет поле issuerCode")
        if issuer_id == 1:
            tests_passed &= self.assert_equal(issuer.get("id"), 1, "Issuer id = 1")
            tests_passed &= self.assert_equal(issuer.get("issuerName"), "Any issuer", "Issuer name = Any issuer")
            tests_passed &= self.assert_equal(issuer.get("issuerType"), "bank", "Issuer type = bank")
            tests_passed &= self.assert_equal(issuer.get("issuerCode"), "", "Issuer code = empty")
        elif issuer_id == 216:
            tests_passed &= self.assert_equal(issuer.get("id"), 216, "Issuer id = 216")
            tests_passed &= self.assert_equal(issuer.get("issuerName"), "VK Pay", "Issuer name = VK Pay")
            tests_passed &= self.assert_equal(issuer.get("issuerType"), "bank", "Issuer type = bank")
            tests_passed &= self.assert_equal(issuer.get("issuerCode"), "", "Issuer code = empty")
        self.test_results.append({
            "test": f"GetIssuer ID={issuer_id}",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        return tests_passed
    def test_get_issuer_error(self, issuer_id: int = 217) -> bool:

        print(f"\n🧪 Тестируем GetIssuer с несуществующим ID = {issuer_id}")
        print("=" * 50)
        payload = {"id": issuer_id}
        result = self.run_grpcurl("GetIssuer", payload)
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetIssuer Error ID={issuer_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        error_msg = result.get("error", "").lower()
        if "issuer not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetIssuer Error ID={issuer_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'issuer not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetIssuer Error ID={issuer_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False

    def test_get_issuers_default(self) -> bool:

        try:
            print("🔍 Тестируем GetIssuers без параметров...")
            payload = {}
            result = self.run_grpcurl("GetIssuers", payload)
            if result is None:
                self.test_results.append({
                    "test": "GetIssuers Default",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetIssuers Default",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            response = result.get("response", {})
            if "getIssuersResponse" not in response:
                self.test_results.append({
                    "test": "GetIssuers Default",
                    "status": "FAIL",
                    "details": "Ответ не содержит getIssuersResponse"
                })
                return False
            issuers_response = response["getIssuersResponse"]
            issuers = issuers_response.get("issuers", [])
            if not issuers:
                self.test_results.append({
                    "test": "GetIssuers Default",
                    "status": "FAIL",
                    "details": "Массив issuers пуст"
                })
                return False
            if len(issuers) <= 1:
                self.test_results.append({
                    "test": "GetIssuers Default",
                    "status": "FAIL",
                    "details": f"Ожидалось больше 1 эмитента, получено {len(issuers)}"
                })
                return False
            first_issuer = issuers[0]
            tests_passed = True
            tests_passed &= self.assert_has_property(first_issuer, "id", "Issuer имеет поле id")
            tests_passed &= self.assert_has_property(first_issuer, "issuerName", "Issuer имеет поле issuerName")
            tests_passed &= self.assert_has_property(first_issuer, "issuerType", "Issuer имеет поле issuerType")
            tests_passed &= self.assert_has_property(first_issuer, "issuerCode", "Issuer имеет поле issuerCode")
            tests_passed &= self.assert_equal(first_issuer.get("id"), 216, "VK Pay issuer id = 216")
            tests_passed &= self.assert_equal(first_issuer.get("issuerName"), "VK Pay", "VK Pay issuer name = VK Pay")
            tests_passed &= self.assert_equal(first_issuer.get("issuerType"), "bank", "VK Pay issuer type = bank")
            tests_passed &= self.assert_equal(first_issuer.get("issuerCode"), "", "VK Pay issuer code = empty")
            self.test_results.append({
                "test": "GetIssuers Default",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetIssuers Default",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    def test_get_issuers_order_name_desc(self) -> bool:
        try:
            print("🔍 Тестируем GetIssuers с сортировкой по issuer_name DESC...")
            payload = {
                "order": {
                    "order_by": "issuer_name",
                    "order_desc": True
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            result = self.run_grpcurl("GetIssuers", payload)
            if result is None:
                self.test_results.append({
                    "test": "GetIssuers Order Name DESC",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetIssuers Order Name DESC",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            response = result.get("response", {})
            if "getIssuersResponse" not in response:
                self.test_results.append({
                    "test": "GetIssuers Order Name DESC",
                    "status": "FAIL",
                    "details": "Ответ не содержит getIssuersResponse"
                })
                return False
            issuers_response = response["getIssuersResponse"]
            issuers = issuers_response.get("issuers", [])
            if not issuers:
                self.test_results.append({
                    "test": "GetIssuers Order Name DESC",
                    "status": "FAIL",
                    "details": "Массив issuers пуст"
                })
                return False
            first_issuer = issuers[0]
            tests_passed = True
            tests_passed &= self.assert_has_property(first_issuer, "id", "Issuer имеет поле id")
            tests_passed &= self.assert_has_property(first_issuer, "issuerName", "Issuer имеет поле issuerName")
            tests_passed &= self.assert_has_property(first_issuer, "issuerType", "Issuer имеет поле issuerType")
            tests_passed &= self.assert_has_property(first_issuer, "issuerCode", "Issuer имеет поле issuerCode")
            tests_passed &= self.assert_equal(first_issuer.get("id"), 87, "Issuer id = 87")
            tests_passed &= self.assert_equal(first_issuer.get("issuerName"), "Zolotaya Korona", "Issuer name = Zolotaya Korona")
            tests_passed &= self.assert_equal(first_issuer.get("issuerType"), "bank", "Issuer type = bank")
            tests_passed &= self.assert_equal(first_issuer.get("issuerCode"), "", "Issuer code = empty")
            self.test_results.append({
                "test": "GetIssuers Order Name DESC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetIssuers Order Name DESC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    def test_get_issuers_pagination(self) -> bool:
        try:
            print("🔍 Тестируем GetIssuers с пагинацией...")
            payload = {
                "pagination": {
                    "limit": "5",
                    "offset": "5"
                }
            }
            result = self.run_grpcurl("GetIssuers", payload)
            if result is None:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            response = result.get("response", {})
            if "getIssuersResponse" not in response:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": "Ответ не содержит getIssuersResponse"
                })
                return False
            issuers_response = response["getIssuersResponse"]
            issuers = issuers_response.get("issuers", [])
            if not issuers:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": "Массив issuers пуст"
                })
                return False
            if len(issuers) != 5:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": f"Ожидалось 5 элементов, получено {len(issuers)}"
                })
                return False
            first_issuer = issuers[0]
            tests_passed = True
            tests_passed &= self.assert_has_property(first_issuer, "id", "Issuer имеет поле id")
            tests_passed &= self.assert_has_property(first_issuer, "issuerName", "Issuer имеет поле issuerName")
            tests_passed &= self.assert_has_property(first_issuer, "issuerType", "Issuer имеет поле issuerType")
            tests_passed &= self.assert_has_property(first_issuer, "issuerCode", "Issuer имеет поле issuerCode")
            tests_passed &= self.assert_equal(first_issuer.get("id"), 211, "Issuer id = 211")
            tests_passed &= self.assert_equal(first_issuer.get("issuerName"), "Es-Bi-Ay Bank", "Issuer name = Es-Bi-Ay Bank")
            tests_passed &= self.assert_equal(first_issuer.get("issuerType"), "bank", "Issuer type = bank")
            tests_passed &= self.assert_equal(first_issuer.get("issuerCode"), "", "Issuer code = empty")
            total_count = issuers_response.get("totalCount")
            tests_passed &= self.assert_equal(total_count, "216", "totalCount = 216")
            self.test_results.append({
                "test": "GetIssuers Pagination",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            return tests_passed
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetIssuers Pagination",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False


from base_tester import BaseGrpcTester


class RegionTester(BaseGrpcTester):
    
    def test_get_region(self, region_id: int = 1) -> bool:
        print(f"\n🧪 Тестируем GetRegion с ID = {region_id}")
        print("=" * 50)
        
        payload = {"id": region_id}
        
        result = self.run_grpcurl("GetRegion", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getRegionResponse" not in response:
            print("❌ Ответ не содержит getRegionResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getRegionResponse"
            })
            return False
        
        region_response = response["getRegionResponse"]
        region = region_response.get("region")
        
        if not region:
            print("❌ Ответ не содержит region")
            self.test_results.append({
                "test": "Наличие region", 
                "status": "FAIL", 
                "details": "Отсутствует region в ответе"
            })
            return False
        
        tests_passed = True
        
        tests_passed &= self.assert_has_property(region, "id", "Region имеет поле id")
        tests_passed &= self.assert_has_property(region, "title", "Region имеет поле title")
        
        if region_id == 1:
            tests_passed &= self.assert_equal(region.get("id"), 1, "Region id = 1")
            tests_passed &= self.assert_equal(region.get("title"), "UA", "Region title = UA")
        
        self.test_results.append({
            "test": f"GetRegion ID={region_id}",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed
    
    def test_get_region_error(self, region_id: int = 100) -> bool:
        print(f"\n🧪 Тестируем GetRegion с несуществующим ID = {region_id}")
        print("=" * 50)
        
        payload = {"id": region_id}
        
        result = self.run_grpcurl("GetRegion", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"GetRegion Error ID={region_id}",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "region not found" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"GetRegion Error ID={region_id}",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'region not found'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"GetRegion Error ID={region_id}",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False
    
    def test_get_regions_default(self) -> bool:
        try:
            print("🔍 Тестируем GetRegions без параметров...")
            
            payload = {}
            
            result = self.run_grpcurl("GetRegions", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetRegions Default",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetRegions Default",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getRegionsResponse" not in response:
                self.test_results.append({
                    "test": "GetRegions Default",
                    "status": "FAIL",
                    "details": "Ответ не содержит getRegionsResponse"
                })
                return False
            
            regions_response = response["getRegionsResponse"]
            regions = regions_response.get("regions", [])
            
            if not regions:
                self.test_results.append({
                    "test": "GetRegions Default",
                    "status": "FAIL",
                    "details": "Массив regions пуст"
                })
                return False
            
            if len(regions) <= 1:
                self.test_results.append({
                    "test": "GetRegions Default",
                    "status": "FAIL",
                    "details": f"Ожидалось больше 1 региона, получено {len(regions)}"
                })
                return False
            
            first_region = regions[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_region, "id", "Region имеет поле id")
            tests_passed &= self.assert_has_property(first_region, "title", "Region имеет поле title")
            tests_passed &= self.assert_equal(first_region.get("id"), 12, "Region id = 12")
            tests_passed &= self.assert_equal(first_region.get("title"), "IN", "Region title = IN")
            
            self.test_results.append({
                "test": "GetRegions Default",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetRegions Default",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_regions_order_code_desc(self) -> bool:
        try:
            print("🔍 Тестируем GetRegions с сортировкой по id DESC...")
            
            payload = {
                "order": {
                    "order_by": "id",
                    "order_desc": True
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            
            result = self.run_grpcurl("GetRegions", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetRegions Order ID DESC",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetRegions Order ID DESC",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getRegionsResponse" not in response:
                self.test_results.append({
                    "test": "GetRegions Order ID DESC",
                    "status": "FAIL",
                    "details": "Ответ не содержит getRegionsResponse"
                })
                return False
            
            regions_response = response["getRegionsResponse"]
            regions = regions_response.get("regions", [])
            
            if not regions:
                self.test_results.append({
                    "test": "GetRegions Order ID DESC",
                    "status": "FAIL",
                    "details": "Массив regions пуст"
                })
                return False
            
            first_region = regions[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_region, "id", "Region имеет поле id")
            tests_passed &= self.assert_has_property(first_region, "title", "Region имеет поле title")
            tests_passed &= self.assert_equal(first_region.get("id"), 12, "Region id = 12")
            tests_passed &= self.assert_equal(first_region.get("title"), "IN", "Region title = IN")
            
            self.test_results.append({
                "test": "GetRegions Order ID DESC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetRegions Order ID DESC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_regions_order_title_asc(self) -> bool:
        try:
            print("🔍 Тестируем GetRegions с сортировкой по title ASC...")
            
            payload = {
                "order": {
                    "order_by": "title",
                    "order_desc": False
                },
                "pagination": {
                    "limit": "100",
                    "offset": "0"
                }
            }
            
            result = self.run_grpcurl("GetRegions", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetRegions Order Title ASC",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetRegions Order Title ASC",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getRegionsResponse" not in response:
                self.test_results.append({
                    "test": "GetRegions Order Title ASC",
                    "status": "FAIL",
                    "details": "Ответ не содержит getRegionsResponse"
                })
                return False
            
            regions_response = response["getRegionsResponse"]
            regions = regions_response.get("regions", [])
            
            if not regions:
                self.test_results.append({
                    "test": "GetRegions Order Title ASC",
                    "status": "FAIL",
                    "details": "Массив regions пуст"
                })
                return False
            
            first_region = regions[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_region, "id", "Region имеет поле id")
            tests_passed &= self.assert_has_property(first_region, "title", "Region имеет поле title")
            tests_passed &= self.assert_equal(first_region.get("id"), 2, "Region id = 2")
            tests_passed &= self.assert_equal(first_region.get("title"), "AM", "Region title = AM")
            
            self.test_results.append({
                "test": "GetRegions Order Title ASC",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetRegions Order Title ASC",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False
    
    def test_get_regions_pagination(self) -> bool:
        try:
            print("🔍 Тестируем GetRegions с пагинацией...")
            
            payload = {
                "pagination": {
                    "limit": "5",
                    "offset": "2"
                }
            }
            
            result = self.run_grpcurl("GetRegions", payload)
            
            if result is None:
                self.test_results.append({
                    "test": "GetRegions Pagination",
                    "status": "FAIL",
                    "details": "Не удалось выполнить запрос"
                })
                return False
            
            if not result.get("success", False):
                self.test_results.append({
                    "test": "GetRegions Pagination",
                    "status": "FAIL",
                    "details": f"gRPC запрос неуспешен: {result.get('error', 'Unknown error')}"
                })
                return False
            
            response = result.get("response", {})
            
            if "getRegionsResponse" not in response:
                self.test_results.append({
                    "test": "GetRegions Pagination",
                    "status": "FAIL",
                    "details": "Ответ не содержит getRegionsResponse"
                })
                return False
            
            regions_response = response["getRegionsResponse"]
            regions = regions_response.get("regions", [])
            
            if not regions:
                self.test_results.append({
                    "test": "GetRegions Pagination",
                    "status": "FAIL",
                    "details": "Массив regions пуст"
                })
                return False
            if len(regions) != 5:
                self.test_results.append({
                    "test": "GetIssuers Pagination",
                    "status": "FAIL",
                    "details": f"Ожидалось 5 элементов, получено {len(regions)}"
                })
            
            first_region = regions[0]
            
            tests_passed = True
            
            tests_passed &= self.assert_has_property(first_region, "id", "Region имеет поле id")
            tests_passed &= self.assert_has_property(first_region, "title", "Region имеет поле title")
            tests_passed &= self.assert_equal(first_region.get("id"), 10, "Region id = 10")
            tests_passed &= self.assert_equal(first_region.get("title"), "TR", "Region title = TR")

            total_count = regions_response.get("totalCount")
            tests_passed &= self.assert_equal(total_count, "12", "totalCount = 12")
            
            self.test_results.append({
                "test": "GetRegions Pagination",
                "status": "PASS" if tests_passed else "FAIL",
                "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
            })
            
            return tests_passed
            
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
            self.test_results.append({
                "test": "GetRegions Pagination",
                "status": "FAIL",
                "details": f"Ошибка: {e}"
            })
            return False


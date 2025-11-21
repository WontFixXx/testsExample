from base_tester import BaseOffersApiTester

class GetOffersTester(BaseOffersApiTester):
    
    def test_get_offers_default(self) -> bool:
        print(f"\n🧪 Тестируем GetOffers - базовый тест")
        print("=" * 50)
        
        payload = {}
        
        result = self.run_grpcurl("GetOffers", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getOffersResponse" not in response:
            print("❌ Ответ не содержит getOffersResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getOffersResponse"
            })
            return False
        
        get_offers_response = response["getOffersResponse"]
        offers = get_offers_response.get("offers", [])
        
        if not offers:
            print("❌ Ответ не содержит offers")
            self.test_results.append({
                "test": "Наличие offers", 
                "status": "FAIL", 
                "details": "Отсутствует offers в ответе"
            })
            return False
        
        if len(offers) == 0:
            print("⚠️ Массив offers пуст")
            self.test_results.append({
                "test": "Наличие offers", 
                "status": "WARN", 
                "details": "Массив offers пуст"
            })
            return True
        
        # Берем первый оффер для проверки структуры
        first_offer = offers[0]
        tests_passed = True
        
        # Проверяем наличие всех обязательных полей в первом оффере
        tests_passed &= self.assert_has_property(first_offer, "id", "Offer имеет поле id")
        tests_passed &= self.assert_has_property(first_offer, "name", "Offer имеет поле name")
        tests_passed &= self.assert_has_property(first_offer, "directionType", "Offer имеет поле directionType")
        tests_passed &= self.assert_has_property(first_offer, "traderPaymentDetailsId", "Offer имеет поле traderPaymentDetailsId")
        tests_passed &= self.assert_has_property(first_offer, "currencyId", "Offer имеет поле currencyId")
        tests_passed &= self.assert_has_property(first_offer, "paymentMethodTypeId", "Offer имеет поле paymentMethodTypeId")
        tests_passed &= self.assert_has_property(first_offer, "traderId", "Offer имеет поле traderId")
        tests_passed &= self.assert_has_property(first_offer, "traderAccountId", "Offer имеет поле traderAccountId")
        tests_passed &= self.assert_has_property(first_offer, "maxOrderSize", "Offer имеет поле maxOrderSize")
        tests_passed &= self.assert_has_property(first_offer, "minOrderSize", "Offer имеет поле minOrderSize")
        tests_passed &= self.assert_has_property(first_offer, "offerAmount", "Offer имеет поле offerAmount")
        tests_passed &= self.assert_has_property(first_offer, "ordersOnHold", "Offer имеет поле ordersOnHold")
        tests_passed &= self.assert_has_property(first_offer, "allowSameAmountOrders", "Offer имеет поле allowSameAmountOrders")
        tests_passed &= self.assert_has_property(first_offer, "orderLastProcessingTs", "Offer имеет поле orderLastProcessingTs")
        tests_passed &= self.assert_has_property(first_offer, "offerCommission", "Offer имеет поле offerCommission")
        tests_passed &= self.assert_has_property(first_offer, "offerCommissionScore", "Offer имеет поле offerCommissionScore")
        tests_passed &= self.assert_has_property(first_offer, "regionId", "Offer имеет поле regionId")
        tests_passed &= self.assert_has_property(first_offer, "issuerId", "Offer имеет поле issuerId")
        tests_passed &= self.assert_has_property(first_offer, "allowAnyBank", "Offer имеет поле allowAnyBank")
        tests_passed &= self.assert_has_property(first_offer, "status", "Offer имеет поле status")
        
        # Проверяем, что ID является UUID
        tests_passed &= self.assert_is_uuid(first_offer.get("id", ""), "Offer ID является UUID")
        
        # Проверяем, что traderAccountId является UUID
        tests_passed &= self.assert_is_uuid(first_offer.get("traderAccountId", ""), "Offer traderAccountId является UUID")
        
        # Проверяем, что traderPaymentDetailsId является UUID
        tests_passed &= self.assert_is_uuid(first_offer.get("traderPaymentDetailsId", ""), "Offer traderPaymentDetailsId является UUID")
        
        # Проверяем, что traderId является UUID
        tests_passed &= self.assert_is_uuid(first_offer.get("traderId", ""), "Offer traderId является UUID")
        
        self.test_results.append({
            "test": "GetOffers Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_get_offer_default(self) -> bool:
        print(f"\n🧪 Тестируем GetOffer - базовый тест")
        print("=" * 50)
        
        result_for_compare = self.run_grpcurl("GetOffers", {})
        last_offer_id = result_for_compare.get("response", {}).get("getOffersResponse", {}).get("offers", [{}])[0].get("id")
        print(f"🔍 Последний ID: {last_offer_id}")

        payload = {
            "offer_id": last_offer_id
        }
        
        result = self.run_grpcurl("GetOffer", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True
        
        # Проверяем наличие всех обязательных полей в первом оффере
        tests_passed &= self.assert_has_property(offer, "id", "Offer имеет поле id")
        tests_passed &= self.assert_has_property(offer, "name", "Offer имеет поле name")
        tests_passed &= self.assert_has_property(offer, "directionType", "Offer имеет поле directionType")
        tests_passed &= self.assert_has_property(offer, "traderPaymentDetailsId", "Offer имеет поле traderPaymentDetailsId")
        tests_passed &= self.assert_has_property(offer, "currencyId", "Offer имеет поле currencyId")
        tests_passed &= self.assert_has_property(offer, "paymentMethodTypeId", "Offer имеет поле paymentMethodTypeId")
        tests_passed &= self.assert_has_property(offer, "traderId", "Offer имеет поле traderId")
        tests_passed &= self.assert_has_property(offer, "traderAccountId", "Offer имеет поле traderAccountId")
        tests_passed &= self.assert_has_property(offer, "maxOrderSize", "Offer имеет поле maxOrderSize")
        tests_passed &= self.assert_has_property(offer, "minOrderSize", "Offer имеет поле minOrderSize")
        tests_passed &= self.assert_has_property(offer, "offerAmount", "Offer имеет поле offerAmount")
        tests_passed &= self.assert_has_property(offer, "ordersOnHold", "Offer имеет поле ordersOnHold")
        tests_passed &= self.assert_has_property(offer, "allowSameAmountOrders", "Offer имеет поле allowSameAmountOrders")
        tests_passed &= self.assert_has_property(offer, "orderLastProcessingTs", "Offer имеет поле orderLastProcessingTs")
        tests_passed &= self.assert_has_property(offer, "offerCommission", "Offer имеет поле offerCommission")
        tests_passed &= self.assert_has_property(offer, "offerCommissionScore", "Offer имеет поле offerCommissionScore")
        tests_passed &= self.assert_has_property(offer, "regionId", "Offer имеет поле regionId")
        tests_passed &= self.assert_has_property(offer, "issuerId", "Offer имеет поле issuerId")
        tests_passed &= self.assert_has_property(offer, "allowAnyBank", "Offer имеет поле allowAnyBank")
        tests_passed &= self.assert_has_property(offer, "status", "Offer имеет поле status")

        # Получаем данные из result_for_compare для сравнения
        compare_offer = result_for_compare.get("response", {}).get("getOffersResponse", {}).get("offers", [{}])[0]
        
        # Сравниваем значения полей
        tests_passed &= self.assert_equal(offer.get("id"), compare_offer.get("id"), "Offer id соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("name"), compare_offer.get("name"), "Offer name соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("directionType"), compare_offer.get("directionType"), "Offer directionType соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("traderPaymentDetailsId"), compare_offer.get("traderPaymentDetailsId"), "Offer traderPaymentDetailsId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("currencyId"), compare_offer.get("currencyId"), "Offer currencyId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("paymentMethodTypeId"), compare_offer.get("paymentMethodTypeId"), "Offer paymentMethodTypeId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("traderId"), compare_offer.get("traderId"), "Offer traderId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("traderAccountId"), compare_offer.get("traderAccountId"), "Offer traderAccountId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("maxOrderSize"), compare_offer.get("maxOrderSize"), "Offer maxOrderSize соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("minOrderSize"), compare_offer.get("minOrderSize"), "Offer minOrderSize соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("offerAmount"), compare_offer.get("offerAmount"), "Offer offerAmount соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("ordersOnHold"), compare_offer.get("ordersOnHold"), "Offer ordersOnHold соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("allowSameAmountOrders"), compare_offer.get("allowSameAmountOrders"), "Offer allowSameAmountOrders соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("orderLastProcessingTs"), compare_offer.get("orderLastProcessingTs"), "Offer orderLastProcessingTs соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("offerCommission"), compare_offer.get("offerCommission"), "Offer offerCommission соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("offerCommissionScore"), compare_offer.get("offerCommissionScore"), "Offer offerCommissionScore соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("regionId"), compare_offer.get("regionId"), "Offer regionId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("issuerId"), compare_offer.get("issuerId"), "Offer issuerId соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("allowAnyBank"), compare_offer.get("allowAnyBank"), "Offer allowAnyBank соответствует GetOffers")
        tests_passed &= self.assert_equal(offer.get("status"), compare_offer.get("status"), "Offer status соответствует GetOffers")
        
        self.test_results.append({
            "test": "GetOffer Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed
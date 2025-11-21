import uuid
from base_tester import BaseOffersApiTester

class CreateOfferTester(BaseOffersApiTester):
    
    def test_create_offer_payin_default(self) -> bool:
        print(f"\n🧪 Тестируем создание PayIn Offer - базовый тест")
        print("=" * 50)
        
        payload = {
            "pay_in_offer": {
                "allow_no_issuer_pools": True,
                "allow_same_amount_orders": True,
                "amount": "1000000",
                "max_order_size": "1000000",
                "min_order_size": "20000",
                "name": f"offer_{uuid.uuid4().hex[:8]}",
                "trader_id": "550e8400-e29b-41d4-a716-446655440001",
                "trader_payment_details_id": "550e8400-e29b-41d4-a716-446655440021"
            }
        }
        
        result = self.run_grpcurl("PublishNewOffer", payload)
        
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
        
        # Проверяем наличие всех обязательных полей
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
        tests_passed &= self.assert_has_property(offer, "status", "Offer имеет поле status")
        
        # Проверяем значения полей
        tests_passed &= self.assert_is_uuid(offer.get("id", ""), "Offer ID является UUID")
        tests_passed &= self.assert_equal(offer.get("name"), payload["pay_in_offer"]["name"], f"Offer name = {payload['pay_in_offer']['name']}")
        tests_passed &= self.assert_equal(offer.get("directionType"), "PAYIN", "Offer directionType = PAYIN")
        tests_passed &= self.assert_equal(offer.get("traderPaymentDetailsId"), "550e8400-e29b-41d4-a716-446655440021", "Offer traderPaymentDetailsId соответствует запросу")
        tests_passed &= self.assert_equal(offer.get("currencyId"), "3", "Offer currencyId = 3")
        tests_passed &= self.assert_equal(offer.get("paymentMethodTypeId"), "2", "Offer paymentMethodTypeId = 2")
        tests_passed &= self.assert_equal(offer.get("traderId"), "550e8400-e29b-41d4-a716-446655440001", "Offer traderId соответствует запросу")
        tests_passed &= self.assert_is_uuid(offer.get("traderAccountId", ""), "Offer traderAccountId является UUID")
        tests_passed &= self.assert_equal(offer.get("maxOrderSize"), "1000000", "Offer maxOrderSize = 1000000")
        tests_passed &= self.assert_equal(offer.get("minOrderSize"), "20000", "Offer minOrderSize = 20000")
        tests_passed &= self.assert_equal(offer.get("offerAmount"), "1000000", "Offer offerAmount = 1000000")
        tests_passed &= self.assert_equal(offer.get("ordersOnHold"), "", "Offer ordersOnHold пустое")
        tests_passed &= self.assert_equal(offer.get("allowSameAmountOrders"), True, "Offer allowSameAmountOrders = true")
        tests_passed &= self.assert_equal(offer.get("orderLastProcessingTs"), None, "Offer orderLastProcessingTs = null")
        tests_passed &= self.assert_equal(offer.get("offerCommission"), 3, "Offer offerCommission = 3")
        tests_passed &= self.assert_equal(offer.get("offerCommissionScore"), 97, "Offer offerCommissionScore = 97")
        tests_passed &= self.assert_equal(offer.get("regionId"), 8, "Offer regionId = 8")
        tests_passed &= self.assert_equal(offer.get("allowAnyBank"), True, "Offer allowAnyBank = true")
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_ACTIVE", "Offer status = OFFER_ACTIVE")
        
        self.test_results.append({
            "test": "CreateOffer PayIn Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_create_offer_payout_default(self) -> bool:
        print(f"\n🧪 Тестируем создание PayOut Offer - базовый тест")
        print("=" * 50)
        
        payload = {
            "pay_out_offer": {
                "issuer_id": 1,
                "allow_no_issuer_pools": True,
                "allow_same_amount_orders": True,
                "amount": "1000000",
                "max_order_size": "1000000",
                "min_order_size": "10000",
                "name": f"offer_{uuid.uuid4().hex[:8]}",
                "payment_method_type_id": 2,
                "trader_id": "550e8400-e29b-41d4-a716-446655440001",
                "trader_payment_details_id": "550e8400-e29b-41d4-a716-446655440021"
            }
        }
        
        result = self.run_grpcurl("PublishNewOffer", payload)
        
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
        
        # Проверяем наличие всех обязательных полей
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
        
        # Проверяем значения полей
        tests_passed &= self.assert_is_uuid(offer.get("id", ""), "Offer ID является UUID")
        tests_passed &= self.assert_equal(offer.get("name"), payload["pay_out_offer"]["name"], f"Offer name = {payload['pay_out_offer']['name']}")
        tests_passed &= self.assert_equal(offer.get("directionType"), "PAYOUT", "Offer directionType = PAYOUT")
        tests_passed &= self.assert_equal(offer.get("traderPaymentDetailsId"), "550e8400-e29b-41d4-a716-446655440021", "Offer traderPaymentDetailsId соответствует запросу")
        tests_passed &= self.assert_equal(offer.get("currencyId"), "3", "Offer currencyId = 3")
        tests_passed &= self.assert_equal(offer.get("paymentMethodTypeId"), "2", "Offer paymentMethodTypeId = 2")
        tests_passed &= self.assert_equal(offer.get("traderId"), "550e8400-e29b-41d4-a716-446655440001", "Offer traderId соответствует запросу")
        tests_passed &= self.assert_is_uuid(offer.get("traderAccountId", ""), "Offer traderAccountId является UUID")
        tests_passed &= self.assert_equal(offer.get("maxOrderSize"), "1000000", "Offer maxOrderSize = 1000000")
        tests_passed &= self.assert_equal(offer.get("minOrderSize"), "10000", "Offer minOrderSize = 10000")
        tests_passed &= self.assert_equal(offer.get("offerAmount"), "1000000", "Offer offerAmount = 1000000")
        tests_passed &= self.assert_equal(offer.get("ordersOnHold"), "", "Offer ordersOnHold пустое")
        tests_passed &= self.assert_equal(offer.get("allowSameAmountOrders"), True, "Offer allowSameAmountOrders = true")
        tests_passed &= self.assert_equal(offer.get("orderLastProcessingTs"), None, "Offer orderLastProcessingTs = null")
        tests_passed &= self.assert_equal(offer.get("offerCommission"), 2.5, "Offer offerCommission = 2.5")
        tests_passed &= self.assert_equal(offer.get("offerCommissionScore"), 97, "Offer offerCommissionScore = 97")
        tests_passed &= self.assert_equal(offer.get("regionId"), 8, "Offer regionId = 8")
        tests_passed &= self.assert_equal(offer.get("issuerId"), 1, "Offer issuerId = 1")
        tests_passed &= self.assert_equal(offer.get("allowAnyBank"), True, "Offer allowAnyBank = true")
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_ACTIVE", "Offer status = OFFER_ACTIVE")
        
        self.test_results.append({
            "test": "CreateOffer PayOut Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

import uuid
import time
from base_tester import BaseOffersApiTester

class UpdateOfferTester(BaseOffersApiTester):
    
    
    def _cancel_all_offers(self, test_name: str = "Unknown Test", verbose: bool = True) -> tuple[bool, int, int]:
        if verbose:
            print(f"🚫 Отмена всех существующих офферов для теста: {test_name}")
        
        # Этап 1: Собираем все офферы через пагинацию
        all_offers = []
        offset = 0
        limit = 50  # Максимальный лимит
        total_count = None
        
        if verbose:
            print("📋 Собираем все офферы через пагинацию...")
        
        while True:
            payload = {
                "pagination": {
                    "limit": str(limit),
                    "offset": str(offset)
                }
            }
            
            result = self.run_grpcurl("GetOffers", payload, verbose=False)
            
            if not result["success"]:
                print(f"❌ Ошибка получения офферов: {result['error']}")
                return False, 0, 0
            
            response = result["response"]
            if "getOffersResponse" not in response:
                print("❌ Неправильная структура ответа - отсутствует getOffersResponse")
                return False, 0, 0
            
            offers_response = response["getOffersResponse"]
            offers_batch = offers_response.get("offers", [])
            
            # Получаем total_count из первого запроса
            if total_count is None:
                total_count = int(offers_response.get("totalCount", 0))
                if verbose:
                    print(f"📊 Всего офферов в системе: {total_count}")
            
            all_offers.extend(offers_batch)
            
            if verbose:
                print(f"📄 Получено {len(offers_batch)} офферов (offset: {offset}, всего собрано: {len(all_offers)})")
            
            # Если получили меньше офферов чем лимит, значит это последняя страница
            if len(offers_batch) < limit:
                break
            
            offset += limit
            
            # Защита от бесконечного цикла
            if len(all_offers) >= total_count:
                break
        
        if verbose:
            print(f"✅ Собрано {len(all_offers)} офферов из {total_count}")
        
        # Этап 2: Фильтруем только активные офферы
        active_offers = [offer for offer in all_offers if offer.get("status") == "OFFER_ACTIVE"]
        
        if not active_offers:
            if verbose:
                print("📋 Нет активных офферов для отмены")
            return True, 0, 0
        
        if verbose:
            print(f"🎯 Найдено {len(active_offers)} активных офферов для отмены")
        
        # Этап 3: Отменяем все активные офферы
        cancelled_count = 0
        failed_cancellations = 0
        
        for i, offer in enumerate(active_offers, 1):
            offer_id = offer.get("id")
            offer_name = offer.get("name", "Unknown")
            offer_status = offer.get("status", "Unknown")
            
            if verbose:
                print(f"  {i}/{len(active_offers)}: Отменяем оффер {offer_name} (ID: {offer_id}, статус: {offer_status})")
            
            # Вызываем CancelOffer для каждого оффера в тихом режиме
            cancel_payload = {"offer_id": offer_id}
            cancel_result = self.run_grpcurl("CancelOffer", cancel_payload, verbose=False)
            
            if cancel_result["success"]:
                cancelled_count += 1
                if verbose:
                    print(f"    ✅ Оффер {offer_name} успешно отменен")
            else:
                failed_cancellations += 1
                if verbose:
                    print(f"    ❌ Не удалось отменить оффер {offer_name}: {cancel_result['error']}")
        
        if verbose:
            print(f"\n📊 Результаты отмены офферов:")
            print(f"   ✅ Успешно отменено: {cancelled_count}")
            print(f"   ❌ Ошибок отмены: {failed_cancellations}")
            print(f"   📋 Всего активных офферов: {len(active_offers)}")
        else:
            print(f"🚫 Отменено {cancelled_count}/{len(active_offers)} активных офферов")
        
        return True, cancelled_count, failed_cancellations
    
    def awaiting_for_processing(self, order_id: str) -> bool:
        print(f"⏳ Ждем изменения статуса заказа {order_id} на 'PROCESSING' (таймаут: 10 сек)")

        payload = {
            "order_id": order_id
        }

        start_time = time.time()
        check_interval = 1  # Проверяем каждую секунду
        
        while time.time() - start_time < 10:
            result = self.run_grpcurl("GetOrderById", payload, verbose=False)
            
            if not result["success"]:
                print(f"❌ Не удалось получить ордер: {result['error']}")
                return False
            
            response = result["response"]
            
            # Извлекаем статус заказа из ответа
            if "getOrderByIdResponse" in response:
                order_data = response["getOrderByIdResponse"]
                
                # Получаем статус заказа из order.status
                current_status = "unknown"
                if "order" in order_data and "status" in order_data["order"]:
                    current_status = order_data["order"].get("status")
                
                print(f"📊 Текущий статус заказа: '{current_status}'")
                
                if current_status == "PROCESSING":
                    elapsed_time = time.time() - start_time
                    print(f"✅ Статус заказа изменился на 'PROCESSING' за {elapsed_time:.1f} секунд")
                    return True
                
                # Если статус не PROCESSING, ждем и повторяем
                time.sleep(check_interval)
            else:
                print("❌ Неправильная структура ответа - отсутствует getOrderByIdResponse")
                return False
        
        # Если таймаут истек
        elapsed_time = time.time() - start_time
        print(f"❌ Таймаут 10 секунд истек. Статус заказа так и не изменился на 'PROCESSING'")
        return False

    def test_pause_offer(self) -> bool:
        print(f"\n🧪 Тестируем паузу Offer - базовый тест")
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

        offer_id = response["getOfferResponse"]["offer"]["id"]

        payload = {
            "offer_id": offer_id
        }

        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if not pause_result["success"]:
            print(f"❌ Не удалось поставить оффер на паузу: {pause_result['error']}")
            self.test_results.append({
                "test": "Постановка оффера на паузу", 
                "status": "FAIL", 
                "details": f"Ошибка: {pause_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно поставлен на паузу")
        
        # Проверяем ответ от PauseOffer
        response = pause_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа PauseOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в PauseOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True     
        # Проверяем значения полей
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_ON_HOLD", "Offer status = OFFER_ON_HOLD")

        self.test_results.append({
            "test": "PauseOffer",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_cancel_offer_without_orders(self) -> bool:
        print(f"\n🧪 Тестируем отмену Offer без ордеров - базовый тест")
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

        offer_id = response["getOfferResponse"]["offer"]["id"]

        payload = {
            "offer_id": offer_id
        }

        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем ответ от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True     
        # Проверяем значения полей
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_CANCELED", "Offer status = OFFER_CANCELED")

        self.test_results.append({
            "test": "CancelOfferWithoutOrders",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed


    def test_error_reactivate_active_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при активации уже активного Offer")
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

        offer_id = response["getOfferResponse"]["offer"]["id"]

        payload = {
            "offer_id": offer_id
        }

        result = self.run_grpcurl("ReactivateOffer", payload)
        
        if result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": f"Error Reactivate Active Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка")
            self.test_results.append({
                "test": f"Error Reactivate Active Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {result.get('error')}")
            self.test_results.append({
                "test": f"Error Reactivate Active Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {result.get('error')}"
            })
            return False

    def test_cancel_active_offer_with_orders(self) -> bool:
        print(f"\n🧪 Тестируем отмену активного Offer с ордерами")
        print("=" * 50)
        
        # Этап 1: Отменяем все существующие офферы
        print("🔍 Этап 1: Отмена всех существующих офферов...")
        is_success, cancelled_count, failed_cancellations = self._cancel_all_offers("Cancel Active Offer With Orders")
        
        if not is_success:
            self.test_results.append({
                "test": "Отмена существующих офферов",
                "status": "FAIL",
                "details": "Не удалось отменить существующие офферы"
            })
            return False
        
        # Этап 2: Создаем новый оффер для тестирования
        print("\n🆕 Этап 2: Создание нового оффера для тестирования...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)

        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")

        # Этап 3: Создаем ордер для нового оффера
        print("\n📦 Этап 3: Создание ордера для нового оффера...")
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
        
        order_result = self.run_grpcurl("CreateOrder", payload)
        
        if not order_result["success"]:
            print(f"❌ Не удалось создать ордер: {order_result['error']}")
            self.test_results.append({
                "test": "Создание ордера", 
                "status": "FAIL", 
                "details": f"Ошибка: {order_result['error']}"
            })
            return False
        
        print("✅ Ордер успешно создан")
        
        # Даем сервису время на обработку пары ордер-оффер
        self.awaiting_for_processing(order_result["response"]["createOrderResponse"]["order"]["orderId"])

        # Этап 4: Отменяем оффер с ордером
        print("\n🚫 Этап 4: Отмена оффера с ордером...")
        payload = {
            "offer_id": offer_id
        }

        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер с ордером: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера с ордером", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось получить информацию об оффере: {cancel_result['error']}")
            self.test_results.append({
                "test": "Получение информации об оффере", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        get_offer_response = cancel_result["response"]
        
        if "getOfferResponse" not in get_offer_response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа GetOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        offer = get_offer_response["getOfferResponse"].get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в GetOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True     
        # Проверяем значения полей
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_INACTIVE", "Offer status = OFFER_INACTIVE")

        self.test_results.append({
            "test": "CancelActiveOfferWithOrders",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        print("\n🎉 Тест успешно завершен!")
        return tests_passed
        
    def test_activate_paused_offer(self) -> bool:
        print(f"\n🧪 Тестируем активацию остановленного Offer")
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

        offer_id = response["getOfferResponse"]["offer"]["id"]

        payload = {
            "offer_id": offer_id
        }

        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if not pause_result["success"]:
            print(f"❌ Не удалось остановить оффер: {pause_result['error']}")
            self.test_results.append({
                "test": "Остановка оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {pause_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно остановлен")

        reactivate_result = self.run_grpcurl("ReactivateOffer", payload)
        
        if not reactivate_result["success"]:
            print(f"❌ Не удалось активировать оффер: {reactivate_result['error']}")
            self.test_results.append({
                "test": "Активация оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {reactivate_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно активирован")
        
        # Проверяем ответ от ReactivateOffer
        response = reactivate_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа ReactivateOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в ReactivateOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True     
        # Проверяем значения полей
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_ACTIVE", "Offer status = OFFER_ACTIVE")

        self.test_results.append({
            "test": "ActivatePausedOffer",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed
        
    def test_transition_offer_on_hold_to_inactive(self) -> bool:
        print(f"\n🧪 Тестируем переход Offer из ON_HOLD в INACTIVE")
        print("=" * 50)
        
        # Этап 1: Отменяем все существующие офферы
        print("🔍 Этап 1: Отмена всех существующих офферов...")
        is_success, cancelled_count, failed_cancellations = self._cancel_all_offers("Transition Offer ON_HOLD to INACTIVE")
        
        if not is_success:
            self.test_results.append({
                "test": "Отмена существующих офферов",
                "status": "FAIL",
                "details": "Не удалось отменить существующие офферы"
            })
            return False
        
        # Этап 2: Создаем новый оффер
        print("\n🆕 Этап 2: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 3: Создаем ордер
        print("\n📦 Этап 3: Создание ордера...")
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
        
        order_result = self.run_grpcurl("CreateOrder", payload)
        
        if not order_result["success"]:
            print(f"❌ Не удалось создать ордер: {order_result['error']}")
            self.test_results.append({
                "test": "Создание ордера", 
                "status": "FAIL", 
                "details": f"Ошибка: {order_result['error']}"
            })
            return False
        
        print("✅ Ордер успешно создан")
        
        # Этап 4: Ждем для обработки сервисом
        self.awaiting_for_processing(order_result["response"]["createOrderResponse"]["order"]["orderId"])
        print("✅ Время ожидания завершено")
        
        # Этап 5: Ставим оффер на паузу
        print("\n⏸️ Этап 5: Ставим оффер на паузу...")
        payload = {"offer_id": offer_id}
        
        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if not pause_result["success"]:
            print(f"❌ Не удалось поставить оффер на паузу: {pause_result['error']}")
            self.test_results.append({
                "test": "Постановка оффера на паузу", 
                "status": "FAIL", 
                "details": f"Ошибка: {pause_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно поставлен на паузу")
        
        # Этап 6: Отменяем оффер и проверяем статус INACTIVE
        print("\n🚫 Этап 6: Отмена оффера и проверка статуса INACTIVE...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True
        # Проверяем, что статус = INACTIVE
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_INACTIVE", "Offer status = OFFER_INACTIVE")
        
        self.test_results.append({
            "test": "TransitionOfferOnHoldToInactive",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        print("\n🎉 Тест успешно завершен!")
        return tests_passed
        
    def test_transition_offer_on_hold_to_canceled(self) -> bool:
        print(f"\n🧪 Тестируем переход Offer из ON_HOLD в CANCELED")
        print("=" * 50)
        
        # Этап 1: Создаем новый оффер
        print("🆕 Этап 1: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 2: Ставим оффер на паузу
        print("\n⏸️ Этап 2: Ставим оффер на паузу...")
        payload = {"offer_id": offer_id}
        
        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if not pause_result["success"]:
            print(f"❌ Не удалось поставить оффер на паузу: {pause_result['error']}")
            self.test_results.append({
                "test": "Постановка оффера на паузу", 
                "status": "FAIL", 
                "details": f"Ошибка: {pause_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно поставлен на паузу")
        
        # Этап 3: Отменяем оффер и проверяем статус CANCELED
        print("\n🚫 Этап 3: Отмена оффера и проверка статуса CANCELED...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        tests_passed = True
        # Проверяем, что статус = CANCELED
        tests_passed &= self.assert_equal(offer.get("status"), "OFFER_CANCELED", "Offer status = OFFER_CANCELED")
        
        self.test_results.append({
            "test": "TransitionOfferOnHoldToCanceled",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        print("\n🎉 Тест успешно завершен!")
        return tests_passed
        
    def test_error_pause_already_paused_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке поставить уже остановленный оффер на паузу")
        print("=" * 50)
        
        # Этап 1: Создаем новый оффер
        print("🆕 Этап 1: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 2: Ставим оффер на паузу первый раз
        print("\n⏸️ Этап 2: Ставим оффер на паузу первый раз...")
        payload = {"offer_id": offer_id}
        
        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if not pause_result["success"]:
            print(f"❌ Не удалось поставить оффер на паузу первый раз: {pause_result['error']}")
            self.test_results.append({
                "test": "Постановка оффера на паузу первый раз", 
                "status": "FAIL", 
                "details": f"Ошибка: {pause_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно поставлен на паузу первый раз")
        
        # Этап 3: Пытаемся поставить оффер на паузу второй раз (ожидаем ошибку)
        print("\n⏸️ Этап 3: Пытаемся поставить оффер на паузу второй раз (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        pause_result_second = self.run_grpcurl("PauseOffer", payload)
        
        if pause_result_second["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Pause Already Paused Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = pause_result_second.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Pause Already Paused Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {pause_result_second.get('error')}")
            self.test_results.append({
                "test": "Error Pause Already Paused Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {pause_result_second.get('error')}"
            })
            return False
        
    def test_error_reactivate_inactive_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке активировать неактивный оффер")
        print("=" * 50)
        
        # Этап 1: Отменяем все существующие офферы
        print("🔍 Этап 1: Отмена всех существующих офферов...")
        is_success, cancelled_count, failed_cancellations = self._cancel_all_offers("Error Reactivate Inactive Offer")
        
        if not is_success:
            self.test_results.append({
                "test": "Отмена существующих офферов",
                "status": "FAIL",
                "details": "Не удалось отменить существующие офферы"
            })
            return False
        
        # Этап 2: Создаем новый оффер
        print("\n🆕 Этап 2: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 3: Создаем ордер
        print("\n📦 Этап 3: Создание ордера...")
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
        
        order_result = self.run_grpcurl("CreateOrder", payload)
        
        if not order_result["success"]:
            print(f"❌ Не удалось создать ордер: {order_result['error']}")
            self.test_results.append({
                "test": "Создание ордера", 
                "status": "FAIL", 
                "details": f"Ошибка: {order_result['error']}"
            })
            return False
        
        print("✅ Ордер успешно создан")
        
        # Этап 4: Ждем для обработки
        print("⏳ Этап 4: Ждем для обработки сервисом...")
        self.awaiting_for_processing(order_result["response"]["createOrderResponse"]["order"]["orderId"])
        print("✅ Время ожидания завершено")
        
        # Этап 5: Отключаем оффер и проверяем статус INACTIVE
        print("\n🚫 Этап 5: Отключение оффера и проверка статуса INACTIVE...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отключить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отключение оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отключен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = INACTIVE
        if offer.get("status") != "OFFER_INACTIVE":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_INACTIVE")
            self.test_results.append({
                "test": "Статус оффера после отключения", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_INACTIVE"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в INACTIVE")
        
        # Этап 6: Пытаемся реактивировать неактивный оффер (ожидаем ошибку)
        print("\n🔄 Этап 6: Попытка реактивации неактивного оффера (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        reactivate_result = self.run_grpcurl("ReactivateOffer", payload)
        
        if reactivate_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Reactivate Inactive Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = reactivate_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Reactivate Inactive Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {reactivate_result.get('error')}")
            self.test_results.append({
                "test": "Error Reactivate Inactive Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {reactivate_result.get('error')}"
            })
            return False
        
    def test_error_pause_inactive_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке поставить неактивный оффер на паузу")
        print("=" * 50)
        
        # Этап 1: Отменяем все существующие офферы
        print("🔍 Этап 1: Отмена всех существующих офферов...")
        is_success, cancelled_count, failed_cancellations = self._cancel_all_offers("Cancel Active Offer With Orders")
        
        if not is_success:
            self.test_results.append({
                "test": "Отмена существующих офферов",
                "status": "FAIL",
                "details": "Не удалось отменить существующие офферы"
            })
            return False
        
        # Этап 2: Создаем новый оффер
        print("\n🆕 Этап 2: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 3: Создаем ордер
        print("\n📦 Этап 3: Создание ордера...")
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
        
        order_result = self.run_grpcurl("CreateOrder", payload)
        
        if not order_result["success"]:
            print(f"❌ Не удалось создать ордер: {order_result['error']}")
            self.test_results.append({
                "test": "Создание ордера", 
                "status": "FAIL", 
                "details": f"Ошибка: {order_result['error']}"
            })
            return False
        
        print("✅ Ордер успешно создан")
        
        # Этап 4: Ждем для обработки
        print("⏳ Этап 4: Ждем для обработки сервисом...")
        self.awaiting_for_processing(order_result["response"]["createOrderResponse"]["order"]["orderId"])
        print("✅ Время ожидания завершено")
        
        # Этап 5: Отключаем оффер и проверяем статус INACTIVE
        print("\n🚫 Этап 5: Отключение оффера и проверка статуса INACTIVE...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отключить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отключение оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отключен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = INACTIVE
        if offer.get("status") != "OFFER_INACTIVE":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_INACTIVE")
            self.test_results.append({
                "test": "Статус оффера после отключения", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_INACTIVE"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в INACTIVE")
        
        # Этап 6: Пытаемся поставить неактивный оффер на паузу (ожидаем ошибку)
        print("\n⏸️ Этап 6: Попытка постановки неактивного оффера на паузу (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if pause_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Pause Inactive Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = pause_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Pause Inactive Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {pause_result.get('error')}")
            self.test_results.append({
                "test": "Error Pause Inactive Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {pause_result.get('error')}"
            })
            return False
        
    def test_error_cancel_inactive_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке отменить неактивный оффер")
        print("=" * 50)
        
        # Этап 1: Отменяем все существующие офферы
        print("🔍 Этап 1: Отмена всех существующих офферов...")
        is_success, cancelled_count, failed_cancellations = self._cancel_all_offers("Cancel Active Offer With Orders")
        
        if not is_success:
            self.test_results.append({
                "test": "Отмена существующих офферов",
                "status": "FAIL",
                "details": "Не удалось отменить существующие офферы"
            })
            return False
        
        # Этап 2: Создаем новый оффер
        print("\n🆕 Этап 2: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 3: Создаем ордер
        print("\n📦 Этап 3: Создание ордера...")
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
        
        order_result = self.run_grpcurl("CreateOrder", payload)
        
        if not order_result["success"]:
            print(f"❌ Не удалось создать ордер: {order_result['error']}")
            self.test_results.append({
                "test": "Создание ордера", 
                "status": "FAIL", 
                "details": f"Ошибка: {order_result['error']}"
            })
            return False
        
        print("✅ Ордер успешно создан")
        
        # Этап 4: Ждем для обработки
        print("⏳ Этап 4: Ждем для обработки сервисом...")
        self.awaiting_for_processing(order_result["response"]["createOrderResponse"]["order"]["orderId"])
        print("✅ Время ожидания завершено")
        
        # Этап 5: Отключаем оффер и проверяем статус INACTIVE
        print("\n🚫 Этап 5: Отключение оффера и проверка статуса INACTIVE...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отключить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отключение оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отключен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = INACTIVE
        if offer.get("status") != "OFFER_INACTIVE":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_INACTIVE")
            self.test_results.append({
                "test": "Статус оффера после отключения", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_INACTIVE"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в INACTIVE")
        
        # Этап 6: Пытаемся отменить неактивный оффер еще раз (ожидаем ошибку)
        print("\n🚫 Этап 6: Попытка повторной отмены неактивного оффера (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        cancel_again_result = self.run_grpcurl("CancelOffer", payload)
        
        if cancel_again_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Cancel Inactive Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = cancel_again_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Cancel Inactive Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {cancel_again_result.get('error')}")
            self.test_results.append({
                "test": "Error Cancel Inactive Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {cancel_again_result.get('error')}"
            })
            return False
        
    def test_error_cancel_canceled_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке отменить уже отмененный оффер")
        print("=" * 50)
        
        # Этап 1: Создаем новый оффер
        print("🆕 Этап 1: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 2: Отменяем оффер и проверяем статус CANCELED
        print("\n🚫 Этап 2: Отмена оффера и проверка статуса CANCELED...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = CANCELED
        if offer.get("status") != "OFFER_CANCELED":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_CANCELED")
            self.test_results.append({
                "test": "Статус оффера после отмены", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_CANCELED"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в CANCELED")
        
        # Этап 3: Пытаемся отменить уже отмененный оффер еще раз (ожидаем ошибку)
        print("\n🚫 Этап 3: Попытка повторной отмены уже отмененного оффера (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        cancel_again_result = self.run_grpcurl("CancelOffer", payload)
        
        if cancel_again_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Cancel Canceled Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = cancel_again_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Cancel Canceled Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {cancel_again_result.get('error')}")
            self.test_results.append({
                "test": "Error Cancel Canceled Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {cancel_again_result.get('error')}"
            })
            return False
        
    def test_error_reactivate_canceled_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке активировать отмененный оффер")
        print("=" * 50)
        
        # Этап 1: Создаем новый оффер
        print("🆕 Этап 1: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 2: Отменяем оффер и проверяем статус CANCELED
        print("\n🚫 Этап 2: Отмена оффера и проверка статуса CANCELED...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = CANCELED
        if offer.get("status") != "OFFER_CANCELED":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_CANCELED")
            self.test_results.append({
                "test": "Статус оффера после отмены", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_CANCELED"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в CANCELED")
        
        # Этап 3: Пытаемся активировать отмененный оффер (ожидаем ошибку)
        print("\n🔄 Этап 3: Попытка активации отмененного оффера (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        reactivate_result = self.run_grpcurl("ReactivateOffer", payload)
        
        if reactivate_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Reactivate Canceled Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = reactivate_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Reactivate Canceled Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {reactivate_result.get('error')}")
            self.test_results.append({
                "test": "Error Reactivate Canceled Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {reactivate_result.get('error')}"
            })
            return False
        
    def test_error_pause_canceled_offer(self) -> bool:
        print(f"\n🧪 Тестируем ошибку при попытке поставить на паузу отмененный оффер")
        print("=" * 50)
        
        # Этап 1: Создаем новый оффер
        print("🆕 Этап 1: Создание нового оффера...")
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
        
        create_result = self.run_grpcurl("PublishNewOffer", payload)
        
        if not create_result["success"]:
            print(f"❌ Не удалось создать новый оффер: {create_result['error']}")
            self.test_results.append({
                "test": "Создание нового оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {create_result['error']}"
            })
            return False
        
        create_response = create_result["response"]
        offer_id = create_response["getOfferResponse"]["offer"]["id"]
        print(f"✅ Новый оффер создан с ID: {offer_id}")
        
        # Этап 2: Отменяем оффер и проверяем статус CANCELED
        print("\n🚫 Этап 2: Отмена оффера и проверка статуса CANCELED...")
        payload = {"offer_id": offer_id}
        
        cancel_result = self.run_grpcurl("CancelOffer", payload)
        
        if not cancel_result["success"]:
            print(f"❌ Не удалось отменить оффер: {cancel_result['error']}")
            self.test_results.append({
                "test": "Отмена оффера", 
                "status": "FAIL", 
                "details": f"Ошибка: {cancel_result['error']}"
            })
            return False
        
        print("✅ Оффер успешно отменен")
        
        # Проверяем статус в ответе от CancelOffer
        response = cancel_result["response"]
        
        if "getOfferResponse" not in response:
            print("❌ Ответ не содержит getOfferResponse")
            self.test_results.append({
                "test": "Структура ответа CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует getOfferResponse"
            })
            return False
        
        get_offer_response = response["getOfferResponse"]
        offer = get_offer_response.get("offer")
        
        if not offer:
            print("❌ Ответ не содержит offer")
            self.test_results.append({
                "test": "Наличие offer в CancelOffer", 
                "status": "FAIL", 
                "details": "Отсутствует offer в ответе"
            })
            return False
        
        # Проверяем, что статус = CANCELED
        if offer.get("status") != "OFFER_CANCELED":
            print(f"❌ Неожиданный статус оффера: {offer.get('status')}, ожидался OFFER_CANCELED")
            self.test_results.append({
                "test": "Статус оффера после отмены", 
                "status": "FAIL", 
                "details": f"Статус: {offer.get('status')}, ожидался: OFFER_CANCELED"
            })
            return False
        
        print("✅ Статус оффера корректно установлен в CANCELED")
        
        # Этап 3: Пытаемся поставить на паузу отмененный оффер (ожидаем ошибку)
        print("\n⏸️ Этап 3: Попытка постановки на паузу отмененного оффера (ожидаем ошибку)...")
        payload = {"offer_id": offer_id}
        
        pause_result = self.run_grpcurl("PauseOffer", payload)
        
        if pause_result["success"]:
            print("❌ Ожидалась ошибка, но запрос прошел успешно")
            self.test_results.append({
                "test": "Error Pause Canceled Offer",
                "status": "FAIL",
                "details": "Ожидалась ошибка, но запрос прошел успешно"
            })
            return False
        
        error_msg = pause_result.get("error", "").lower()
        if "invalid offer status transition" in error_msg:
            print("✅ Получена ожидаемая ошибка 'invalid offer status transition'")
            self.test_results.append({
                "test": "Error Pause Canceled Offer",
                "status": "PASS",
                "details": "Получена ожидаемая ошибка 'invalid offer status transition'"
            })
            return True
        else:
            print(f"❌ Неожиданная ошибка: {pause_result.get('error')}")
            self.test_results.append({
                "test": "Error Pause Canceled Offer",
                "status": "FAIL",
                "details": f"Неожиданная ошибка: {pause_result.get('error')}"
            })
            return False
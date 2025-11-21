from base_tester import BaseGrpcTester

class GetTradersTester(BaseGrpcTester):
    
    def test_get_traders_default(self) -> bool:
        print(f"\n🧪 Тестируем GetTraders - базовый тест")
        print("=" * 50)
        
        payload = {}
        
        result = self.run_grpcurl("GetTraders", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос выполнен", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getTradersResponse" not in response:
            print("❌ Ответ не содержит getTradersResponse")
            self.test_results.append({
                "test": "Структура ответа", 
                "status": "FAIL", 
                "details": "Отсутствует getTradersResponse"
            })
            return False
        
        get_traders_response = response["getTradersResponse"]
        
        # Проверяем наличие массива traders
        if "traders" not in get_traders_response:
            print("❌ Ответ не содержит traders")
            self.test_results.append({
                "test": "Наличие traders", 
                "status": "FAIL", 
                "details": "Отсутствует traders в ответе"
            })
            return False
        
        traders = get_traders_response.get("traders", [])
        total_count = get_traders_response.get("totalCount", "0")
        
        tests_passed = True
        
        # Проверяем, что total_count больше 0
        tests_passed &= self.assert_has_property(get_traders_response, "totalCount", "Ответ имеет поле totalCount")
        
        # Преобразуем total_count в число для сравнения
        try:
            total_count_int = int(total_count)
            if total_count_int > 0:
                print(f"✅ Total count > 0: {total_count_int}")
            else:
                print(f"❌ Total count должен быть больше 0, получен: {total_count_int}")
                tests_passed = False
                self.test_results.append({
                    "test": "Total count > 0", 
                    "status": "FAIL", 
                    "details": f"Total count = {total_count_int}, ожидался > 0"
                })
        except ValueError:
            print(f"❌ Total count не является числом: {total_count}")
            tests_passed = False
            self.test_results.append({
                "test": "Total count is number", 
                "status": "FAIL", 
                "details": f"Total count не является числом: {total_count}"
            })
        
        # Если есть трейдеры, проверяем структуру первого
        if traders and len(traders) > 0:
            first_trader = traders[0]
            print(f"🔍 Проверяем структуру первого трейдера из {len(traders)} найденных")
            
            # Проверяем наличие всех обязательных полей у первого трейдера
            tests_passed &= self.assert_has_property(first_trader, "id", "Trader имеет поле id")
            tests_passed &= self.assert_has_property(first_trader, "email", "Trader имеет поле email")
            tests_passed &= self.assert_has_property(first_trader, "traderStatus", "Trader имеет поле traderStatus")
            tests_passed &= self.assert_has_property(first_trader, "hasActiveSessions", "Trader имеет поле hasActiveSessions")
            tests_passed &= self.assert_has_property(first_trader, "commissionPayin", "Trader имеет поле commissionPayin")
            tests_passed &= self.assert_has_property(first_trader, "commissionPayout", "Trader имеет поле commissionPayout")
            tests_passed &= self.assert_has_property(first_trader, "currencyId", "Trader имеет поле currencyId")
            tests_passed &= self.assert_has_property(first_trader, "regionId", "Trader имеет поле regionId")
            tests_passed &= self.assert_has_property(first_trader, "createdAt", "Trader имеет поле createdAt")
            tests_passed &= self.assert_has_property(first_trader, "updatedAt", "Trader имеет поле updatedAt")
            
            # Проверяем, что ID является UUID (или хотя бы не пустой)
            trader_id = first_trader.get("id", "")
            tests_passed &= self.assert_not_empty(trader_id, "Trader ID не пустой")
            
            # Проверяем, что email не пустой
            trader_email = first_trader.get("email", "")
            tests_passed &= self.assert_not_empty(trader_email, "Trader email не пустой")
            
        else:
            print("⚠️ Список трейдеров пуст")
            # Это может быть валидным состоянием, но лучше отметить как предупреждение
            self.test_results.append({
                "test": "Наличие трейдеров", 
                "status": "WARN", 
                "details": "Список трейдеров пуст"
            })
        
        self.test_results.append({
            "test": "GetTraders Default",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько тестов провалились"
        })
        
        return tests_passed

    def test_get_traders_order_asc(self) -> bool:
        print(f"\n🧪 Тестируем GetTraders с сортировкой по id ASC")
        print("=" * 50)
        
        # Этап 1: Получаем всех трейдеров без сортировки для локальной сортировки
        print("📋 Этап 1: Получение всех трейдеров для локальной сортировки...")
        all_traders = []
        offset = 0
        limit = 50
        total_count = None
        
        while True:
            payload = {
                "pagination": {
                    "limit": str(limit),
                    "offset": str(offset)
                }
            }
            
            result = self.run_grpcurl("GetTraders", payload, verbose=False)
            
            if not result["success"]:
                print(f"❌ Ошибка получения трейдеров: {result['error']}")
                self.test_results.append({
                    "test": "Получение всех трейдеров", 
                    "status": "FAIL", 
                    "details": f"Ошибка: {result['error']}"
                })
                return False
            
            response = result["response"]
            if "getTradersResponse" not in response:
                print("❌ Неправильная структура ответа - отсутствует getTradersResponse")
                self.test_results.append({
                    "test": "Структура ответа GetTraders", 
                    "status": "FAIL", 
                    "details": "Отсутствует getTradersResponse"
                })
                return False
            
            traders_response = response["getTradersResponse"]
            traders_batch = traders_response.get("traders", [])
            
            # Получаем total_count из первого запроса
            if total_count is None:
                total_count = int(traders_response.get("totalCount", 0))
                print(f"📊 Всего трейдеров в системе: {total_count}")
            
            all_traders.extend(traders_batch)
            
            # Если получили меньше трейдеров чем лимит, значит это последняя страница
            if len(traders_batch) < limit:
                break
            
            offset += limit
            
            # Защита от бесконечного цикла
            if len(all_traders) >= total_count:
                break
        
        print(f"✅ Собрано {len(all_traders)} трейдеров из {total_count}")
        
        if not all_traders:
            print("❌ Список трейдеров пуст")
            self.test_results.append({
                "test": "Наличие трейдеров", 
                "status": "FAIL", 
                "details": "Список трейдеров пуст"
            })
            return False
        
        # Этап 2: Локальная сортировка по id ASC
        print("🔄 Этап 2: Локальная сортировка по id ASC...")
        # Сортируем по id ASC (строковое сравнение)
        sorted_traders = sorted(all_traders, key=lambda x: x.get("id", ""))
        
        # Берем первого трейдера из отсортированного списка
        expected_first_trader = sorted_traders[0]
        expected_first_trader_id = expected_first_trader.get("id")
        
        print(f"📊 Ожидаемый первый трейдер: ID={expected_first_trader_id}")
        
        # Показываем информацию о сортировке
        print(f"🔍 Информация о сортировке:")
        print(f"   - Всего трейдеров: {len(sorted_traders)}")
        print(f"   - Все ID уникальны: {len(set(t.get('id', '') for t in sorted_traders)) == len(sorted_traders)}")
        
        # Показываем первые 3 трейдера для отладки
        print(f"🔍 Первые 3 трейдера после локальной сортировки:")
        for i, trader in enumerate(sorted_traders[:3]):
            print(f"   {i+1}. ID={trader.get('id')}")
        
        # Этап 3: Запрос с сортировкой от сервера
        print("🌐 Этап 3: Запрос с сортировкой от сервера...")
        payload = {
            "order": {
                "order_by": "id",
                "order_desc": False
            }
        }
        
        result = self.run_grpcurl("GetTraders", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос с сортировкой", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getTradersResponse" not in response:
            print("❌ Ответ не содержит getTradersResponse")
            self.test_results.append({
                "test": "Структура ответа с сортировкой", 
                "status": "FAIL", 
                "details": "Отсутствует getTradersResponse"
            })
            return False
        
        get_traders_response = response["getTradersResponse"]
        server_traders = get_traders_response.get("traders", [])
        server_total_count = int(get_traders_response.get("totalCount", 0))
        
        if not server_traders:
            print("❌ Список трейдеров от сервера пуст")
            self.test_results.append({
                "test": "Наличие трейдеров от сервера", 
                "status": "FAIL", 
                "details": "Список трейдеров от сервера пуст"
            })
            return False
        
        # Этап 4: Сравнение результатов
        print("🔍 Этап 4: Сравнение результатов сортировки...")
        actual_first_trader = server_traders[0]
        actual_first_trader_id = actual_first_trader.get("id")
        
        print(f"📊 Фактический первый трейдер: ID={actual_first_trader_id}")
        
        # Показываем первые 3 трейдера от сервера для отладки
        print(f"🔍 Первые 3 трейдера от сервера:")
        for i, trader in enumerate(server_traders[:3]):
            print(f"   {i+1}. ID={trader.get('id')}")
        
        tests_passed = True
        
        # Проверяем, что total_count совпадает
        if server_total_count != total_count:
            print(f"❌ total_count не совпадает: сервер={server_total_count}, локально={total_count}")
            tests_passed = False
        else:
            print(f"✅ total_count совпадает: {server_total_count}")
        
        # Проверяем, что ID первого трейдера совпадает
        if actual_first_trader_id != expected_first_trader_id:
            print(f"❌ ID первого трейдера не совпадает: сервер={actual_first_trader_id}, ожидался={expected_first_trader_id}")
            tests_passed = False
        else:
            print(f"✅ ID первого трейдера совпадает: {actual_first_trader_id}")
        
        # Проверяем, что все трейдеры от сервера отсортированы правильно по ID
        print("🔍 Проверка сортировки всех трейдеров от сервера...")
        server_ids = [t.get("id", "") for t in server_traders]
        is_sorted = all(server_ids[i] <= server_ids[i+1] for i in range(len(server_ids)-1))
        
        if is_sorted:
            print(f"✅ Все трейдеры от сервера отсортированы по ID ASC")
        else:
            print(f"❌ Трейдеры от сервера НЕ отсортированы по ID ASC")
            tests_passed = False
        
        self.test_results.append({
            "test": "GetTraders Order ASC",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько проверок провалились"
        })
        
        return tests_passed

    def test_get_traders_order_desc(self) -> bool:
        print(f"\n🧪 Тестируем GetTraders с сортировкой по email DESC")
        print("=" * 50)
        
        # Этап 1: Получаем всех трейдеров без сортировки для локальной сортировки
        print("📋 Этап 1: Получение всех трейдеров для локальной сортировки...")
        all_traders = []
        offset = 0
        limit = 50
        total_count = None
        
        while True:
            payload = {
                "pagination": {
                    "limit": str(limit),
                    "offset": str(offset)
                }
            }
            
            result = self.run_grpcurl("GetTraders", payload, verbose=False)
            
            if not result["success"]:
                print(f"❌ Ошибка получения трейдеров: {result['error']}")
                self.test_results.append({
                    "test": "Получение всех трейдеров", 
                    "status": "FAIL", 
                    "details": f"Ошибка: {result['error']}"
                })
                return False
            
            response = result["response"]
            if "getTradersResponse" not in response:
                print("❌ Неправильная структура ответа - отсутствует getTradersResponse")
                self.test_results.append({
                    "test": "Структура ответа GetTraders", 
                    "status": "FAIL", 
                    "details": "Отсутствует getTradersResponse"
                })
                return False
            
            traders_response = response["getTradersResponse"]
            traders_batch = traders_response.get("traders", [])
            
            # Получаем total_count из первого запроса
            if total_count is None:
                total_count = int(traders_response.get("totalCount", 0))
                print(f"📊 Всего трейдеров в системе: {total_count}")
            
            all_traders.extend(traders_batch)
            
            # Если получили меньше трейдеров чем лимит, значит это последняя страница
            if len(traders_batch) < limit:
                break
            
            offset += limit
            
            # Защита от бесконечного цикла
            if len(all_traders) >= total_count:
                break
        
        print(f"✅ Собрано {len(all_traders)} трейдеров из {total_count}")
        
        if not all_traders:
            print("❌ Список трейдеров пуст")
            self.test_results.append({
                "test": "Наличие трейдеров", 
                "status": "FAIL", 
                "details": "Список трейдеров пуст"
            })
            return False
        
        # Этап 2: Локальная сортировка по email DESC
        print("🔄 Этап 2: Локальная сортировка по email DESC...")
        # Сортируем по email DESC (case-insensitive строковое сравнение в обратном порядке)
        sorted_traders = sorted(all_traders, key=lambda x: x.get("email", "").lower(), reverse=True)
        
        # Берем первого трейдера из отсортированного списка
        expected_first_trader = sorted_traders[0]
        expected_first_trader_id = expected_first_trader.get("id")
        expected_first_trader_email = expected_first_trader.get("email")
        
        print(f"📊 Ожидаемый первый трейдер: ID={expected_first_trader_id}, email={expected_first_trader_email}")
        
        # Показываем информацию о сортировке
        print(f"🔍 Информация о сортировке:")
        print(f"   - Всего трейдеров: {len(sorted_traders)}")
        email_values = [t.get("email", "") for t in sorted_traders]
        unique_emails = set(email_values)
        print(f"   - Уникальных email адресов: {len(unique_emails)}")
        
        # Показываем первые 3 трейдера для отладки
        print(f"🔍 Первые 3 трейдера после локальной сортировки:")
        for i, trader in enumerate(sorted_traders[:3]):
            print(f"   {i+1}. ID={trader.get('id')}, email={trader.get('email')}")
        
        # Этап 3: Запрос с сортировкой от сервера
        print("🌐 Этап 3: Запрос с сортировкой от сервера...")
        payload = {
            "order": {
                "order_by": "email",
                "order_desc": True
            }
        }
        
        result = self.run_grpcurl("GetTraders", payload)
        
        if not result["success"]:
            print(f"❌ gRPC запрос неуспешен: {result['error']}")
            self.test_results.append({
                "test": "gRPC запрос с сортировкой", 
                "status": "FAIL", 
                "details": f"Ошибка: {result['error']}"
            })
            return False
        
        response = result["response"]
        
        if "getTradersResponse" not in response:
            print("❌ Ответ не содержит getTradersResponse")
            self.test_results.append({
                "test": "Структура ответа с сортировкой", 
                "status": "FAIL", 
                "details": "Отсутствует getTradersResponse"
            })
            return False
        
        get_traders_response = response["getTradersResponse"]
        server_traders = get_traders_response.get("traders", [])
        server_total_count = int(get_traders_response.get("totalCount", 0))
        
        if not server_traders:
            print("❌ Список трейдеров от сервера пуст")
            self.test_results.append({
                "test": "Наличие трейдеров от сервера", 
                "status": "FAIL", 
                "details": "Список трейдеров от сервера пуст"
            })
            return False
        
        # Этап 4: Сравнение результатов
        print("🔍 Этап 4: Сравнение результатов сортировки...")
        actual_first_trader = server_traders[0]
        actual_first_trader_id = actual_first_trader.get("id")
        actual_first_trader_email = actual_first_trader.get("email")
        
        print(f"📊 Фактический первый трейдер: ID={actual_first_trader_id}, email={actual_first_trader_email}")
        
        # Показываем первые 3 трейдера от сервера для отладки
        print(f"🔍 Первые 3 трейдера от сервера:")
        for i, trader in enumerate(server_traders[:3]):
            print(f"   {i+1}. ID={trader.get('id')}, email={trader.get('email')}")
        
        tests_passed = True
        
        # Проверяем, что total_count совпадает
        if server_total_count != total_count:
            print(f"❌ total_count не совпадает: сервер={server_total_count}, локально={total_count}")
            tests_passed = False
        else:
            print(f"✅ total_count совпадает: {server_total_count}")
        
        # Проверяем, что ID первого трейдера совпадает
        if actual_first_trader_id != expected_first_trader_id:
            print(f"❌ ID первого трейдера не совпадает: сервер={actual_first_trader_id}, ожидался={expected_first_trader_id}")
            tests_passed = False
        else:
            print(f"✅ ID первого трейдера совпадает: {actual_first_trader_id}")
        
        # Проверяем, что email первого трейдера совпадает
        if actual_first_trader_email != expected_first_trader_email:
            print(f"❌ email первого трейдера не совпадает: сервер={actual_first_trader_email}, ожидался={expected_first_trader_email}")
            tests_passed = False
        else:
            print(f"✅ email первого трейдера совпадает: {actual_first_trader_email}")
        
        # Проверяем, что первые несколько трейдеров совпадают между локальной и серверной сортировкой
        print("🔍 Проверка совпадения первых трейдеров между локальной и серверной сортировкой...")
        
        # Проверяем первые 3 элемента (которые точно совпадают)
        check_count = min(3, len(sorted_traders), len(server_traders))
        local_emails = [t.get("email", "") for t in sorted_traders[:check_count]]
        server_emails = [t.get("email", "") for t in server_traders[:check_count]]
        
        emails_match = local_emails == server_emails
        
        if emails_match:
            print(f"✅ Первые {check_count} email адресов совпадают между локальной и серверной сортировкой")
        else:
            print(f"❌ Первые {check_count} email адресов НЕ совпадают между локальной и серверной сортировкой")
            print(f"   Локальная сортировка: {local_emails}")
            print(f"   Серверная сортировка: {server_emails}")
            tests_passed = False
        
        self.test_results.append({
            "test": "GetTraders Order DESC",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько проверок провалились"
        })
        
        return tests_passed

    def test_get_traders_pagination(self) -> bool:
        print(f"\n🧪 Тестируем GetTraders с пагинацией")
        print("=" * 50)
        
        # Этап 1: Получаем всех трейдеров без пагинации
        print("📋 Этап 1: Получение всех трейдеров без пагинации...")
        payload_empty = {}
        
        result_empty = self.run_grpcurl("GetTraders", payload_empty)
        
        if not result_empty["success"]:
            print(f"❌ gRPC запрос неуспешен: {result_empty['error']}")
            self.test_results.append({
                "test": "gRPC запрос без пагинации", 
                "status": "FAIL", 
                "details": f"Ошибка: {result_empty['error']}"
            })
            return False
        
        response_empty = result_empty["response"]
        
        if "getTradersResponse" not in response_empty:
            print("❌ Ответ не содержит getTradersResponse")
            self.test_results.append({
                "test": "Структура ответа без пагинации", 
                "status": "FAIL", 
                "details": "Отсутствует getTradersResponse"
            })
            return False
        
        get_traders_response_empty = response_empty["getTradersResponse"]
        all_traders = get_traders_response_empty.get("traders", [])
        total_count = int(get_traders_response_empty.get("totalCount", 0))
        
        print(f"📊 Всего трейдеров в системе: {total_count}")
        print(f"📊 Получено трейдеров: {len(all_traders)}")
        
        if len(all_traders) < 6:
            print(f"❌ Недостаточно трейдеров для тестирования пагинации. Нужно минимум 6, получено {len(all_traders)}")
            self.test_results.append({
                "test": "Достаточно трейдеров для пагинации", 
                "status": "FAIL", 
                "details": f"Нужно минимум 6 трейдеров, получено {len(all_traders)}"
            })
            return False
        
        # Запоминаем 6-й элемент (индекс 5)
        sixth_trader = all_traders[5]
        sixth_trader_id = sixth_trader.get("id")
        sixth_trader_email = sixth_trader.get("email")
        
        print(f"📊 6-й трейдер (индекс 5): ID={sixth_trader_id}, email={sixth_trader_email}")
        
        # Этап 2: Запрос с пагинацией (limit=50, offset=5)
        print("\n🌐 Этап 2: Запрос с пагинацией (limit=50, offset=5)...")
        payload_paginated = {
            "pagination": {
                "limit": "50",
                "offset": "5"
            }
        }
        
        result_paginated = self.run_grpcurl("GetTraders", payload_paginated)
        
        if not result_paginated["success"]:
            print(f"❌ gRPC запрос с пагинацией неуспешен: {result_paginated['error']}")
            self.test_results.append({
                "test": "gRPC запрос с пагинацией", 
                "status": "FAIL", 
                "details": f"Ошибка: {result_paginated['error']}"
            })
            return False
        
        response_paginated = result_paginated["response"]
        
        if "getTradersResponse" not in response_paginated:
            print("❌ Ответ с пагинацией не содержит getTradersResponse")
            self.test_results.append({
                "test": "Структура ответа с пагинацией", 
                "status": "FAIL", 
                "details": "Отсутствует getTradersResponse"
            })
            return False
        
        get_traders_response_paginated = response_paginated["getTradersResponse"]
        paginated_traders = get_traders_response_paginated.get("traders", [])
        paginated_total_count = int(get_traders_response_paginated.get("totalCount", 0))
        
        print(f"📊 Трейдеров с пагинацией: {len(paginated_traders)}")
        print(f"📊 Total count с пагинацией: {paginated_total_count}")
        
        if not paginated_traders:
            print("❌ Список трейдеров с пагинацией пуст")
            self.test_results.append({
                "test": "Наличие трейдеров с пагинацией", 
                "status": "FAIL", 
                "details": "Список трейдеров с пагинацией пуст"
            })
            return False
        
        # Берем первый элемент из пагинированного результата
        first_paginated_trader = paginated_traders[0]
        first_paginated_trader_id = first_paginated_trader.get("id")
        first_paginated_trader_email = first_paginated_trader.get("email")
        
        print(f"📊 Первый трейдер с пагинацией: ID={first_paginated_trader_id}, email={first_paginated_trader_email}")
        
        # Этап 3: Сравнение результатов
        print("\n🔍 Этап 3: Сравнение результатов пагинации...")
        tests_passed = True
        
        # Проверяем, что total_count совпадает
        if paginated_total_count != total_count:
            print(f"❌ total_count не совпадает: без пагинации={total_count}, с пагинацией={paginated_total_count}")
            tests_passed = False
        else:
            print(f"✅ total_count совпадает: {total_count}")
        
        # Проверяем, что ID 6-го трейдера совпадает с ID первого трейдера из пагинированного результата
        if first_paginated_trader_id != sixth_trader_id:
            print(f"❌ ID не совпадает: 6-й трейдер={sixth_trader_id}, первый с пагинацией={first_paginated_trader_id}")
            tests_passed = False
        else:
            print(f"✅ ID 6-го трейдера совпадает с ID первого трейдера из пагинированного результата: {sixth_trader_id}")
        
        # Проверяем, что email 6-го трейдера совпадает с email первого трейдера из пагинированного результата
        if first_paginated_trader_email != sixth_trader_email:
            print(f"❌ Email не совпадает: 6-й трейдер={sixth_trader_email}, первый с пагинацией={first_paginated_trader_email}")
            tests_passed = False
        else:
            print(f"✅ Email 6-го трейдера совпадает с email первого трейдера из пагинированного результата: {sixth_trader_email}")
        
        # Проверяем, что количество элементов в пагинированном результате корректно
        expected_paginated_count = min(50, total_count - 5)  # limit=50, offset=5
        if len(paginated_traders) != expected_paginated_count:
            print(f"❌ Количество элементов в пагинированном результате неверно: ожидалось={expected_paginated_count}, получено={len(paginated_traders)}")
            tests_passed = False
        else:
            print(f"✅ Количество элементов в пагинированном результате корректно: {len(paginated_traders)}")
        
        self.test_results.append({
            "test": "GetTraders Pagination",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Тест пройден успешно" if tests_passed else "Один или несколько проверок провалились"
        })
        
        return tests_passed

    def test_get_traders_filters(self) -> bool:
        print(f"\n🧪 Тестируем GetTraders с различными фильтрами")
        print("=" * 50)
        
        tests_passed = True
        
        # Тест 1: Фильтр по currency_id = 3
        print("\n🔍 Тест 1: Фильтр по currency_id = 3")
        payload1 = {"filter": {"currency_id": 3}}
        result1 = self.run_grpcurl("GetTraders", payload1)
        
        if result1["success"]:
            response1 = result1["response"]
            if "getTradersResponse" in response1:
                traders1 = response1["getTradersResponse"].get("traders", [])
                print(f"📊 Найдено {len(traders1)} трейдеров с currency_id = 3")
                
                # Проверяем, что все трейдеры имеют currency_id = 3
                for i, trader in enumerate(traders1):
                    currency_id = trader.get("currencyId")
                    if currency_id != 3:
                        print(f"❌ Трейдер {i+1} имеет currency_id = {currency_id}, ожидался 3")
                        tests_passed = False
                    else:
                        print(f"✅ Трейдер {i+1} ({trader.get('email', 'unknown')}) currency_id = 3")
            else:
                print("❌ Неправильная структура ответа для currency_id фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с currency_id фильтром: {result1['error']}")
            tests_passed = False
        
        # Тест 2: Фильтр по email = "trader1@test.com"
        print("\n🔍 Тест 2: Фильтр по email = 'trader1@test.com'")
        payload2 = {"filter": {"email": "trader1@test.com"}}
        result2 = self.run_grpcurl("GetTraders", payload2)
        
        if result2["success"]:
            response2 = result2["response"]
            if "getTradersResponse" in response2:
                traders2 = response2["getTradersResponse"].get("traders", [])
                print(f"📊 Найдено {len(traders2)} трейдеров с email = 'trader1@test.com'")
                
                # Проверяем, что все трейдеры имеют правильный email
                for i, trader in enumerate(traders2):
                    email = trader.get("email")
                    if email != "trader1@test.com":
                        print(f"❌ Трейдер {i+1} имеет email = {email}, ожидался trader1@test.com")
                        tests_passed = False
                    else:
                        print(f"✅ Трейдер {i+1} email = trader1@test.com")
            else:
                print("❌ Неправильная структура ответа для email фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с email фильтром: {result2['error']}")
            tests_passed = False
        
        # Тест 3: Фильтр по trader_status = "TRADER_STATUS_ENABLED"
        print("\n🔍 Тест 3: Фильтр по trader_status = 'TRADER_STATUS_ENABLED'")
        payload3 = {"filter": {"trader_status": "TRADER_STATUS_ENABLED"}}
        result3 = self.run_grpcurl("GetTraders", payload3)
        
        if result3["success"]:
            response3 = result3["response"]
            if "getTradersResponse" in response3:
                traders3 = response3["getTradersResponse"].get("traders", [])
                print(f"📊 Найдено {len(traders3)} трейдеров со статусом ENABLED")
                
                # Проверяем, что все трейдеры имеют правильный статус
                for i, trader in enumerate(traders3):
                    status = trader.get("traderStatus")
                    if status != "TRADER_STATUS_ENABLED":
                        print(f"❌ Трейдер {i+1} имеет статус = {status}, ожидался TRADER_STATUS_ENABLED")
                        tests_passed = False
                    else:
                        print(f"✅ Трейдер {i+1} ({trader.get('email', 'unknown')}) статус = TRADER_STATUS_ENABLED")
            else:
                print("❌ Неправильная структура ответа для trader_status фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с trader_status фильтром: {result3['error']}")
            tests_passed = False
        
        # Тест 4: Фильтр по has_active_sessions = false
        print("\n🔍 Тест 4: Фильтр по has_active_sessions = false")
        payload4 = {"filter": {"has_active_sessions": False}}
        result4 = self.run_grpcurl("GetTraders", payload4)
        
        if result4["success"]:
            response4 = result4["response"]
            if "getTradersResponse" in response4:
                traders4 = response4["getTradersResponse"].get("traders", [])
                print(f"📊 Найдено {len(traders4)} трейдеров с has_active_sessions = false")
                
                # Проверяем, что все трейдеры имеют has_active_sessions = false
                for i, trader in enumerate(traders4):
                    has_sessions = trader.get("hasActiveSessions")
                    if has_sessions != False:
                        print(f"❌ Трейдер {i+1} имеет has_active_sessions = {has_sessions}, ожидался false")
                        tests_passed = False
                    else:
                        print(f"✅ Трейдер {i+1} ({trader.get('email', 'unknown')}) has_active_sessions = false")
            else:
                print("❌ Неправильная структура ответа для has_active_sessions фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с has_active_sessions фильтром: {result4['error']}")
            tests_passed = False
        
        # Тест 5: Фильтр по trader_id = "550e8400-e29b-41d4-a716-446655440001"
        print("\n🔍 Тест 5: Фильтр по trader_id = '550e8400-e29b-41d4-a716-446655440001'")
        payload5 = {"filter": {"trader_id": "550e8400-e29b-41d4-a716-446655440001"}}
        result5 = self.run_grpcurl("GetTraders", payload5)
        
        if result5["success"]:
            response5 = result5["response"]
            if "getTradersResponse" in response5:
                traders5 = response5["getTradersResponse"].get("traders", [])
                print(f"📊 Найдено {len(traders5)} трейдеров с trader_id = '550e8400-e29b-41d4-a716-446655440001'")
                
                # Должен вернуться ровно один трейдер с конкретным ID
                if len(traders5) != 1:
                    print(f"❌ Ожидался 1 трейдер, получено {len(traders5)}")
                    tests_passed = False
                else:
                    trader = traders5[0]
                    trader_id = trader.get("id")
                    if trader_id != "550e8400-e29b-41d4-a716-446655440001":
                        print(f"❌ Трейдер имеет id = {trader_id}, ожидался 550e8400-e29b-41d4-a716-446655440001")
                        tests_passed = False
                    else:
                        print(f"✅ Найден трейдер с правильным ID: {trader.get('email', 'unknown')}")
            else:
                print("❌ Неправильная структура ответа для trader_id фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с trader_id фильтром: {result5['error']}")
            tests_passed = False
        
        # Тест 6: Фильтр по payment_method_type_id (проверяем разные значения)
        print("\n🔍 Тест 6: Фильтр по payment_method_type_id (сравнение значений 1 и 2)")
        
        # Запрос с payment_method_type_id = 1
        payload6a = {"filter": {"payment_method_type_id": 1}}
        result6a = self.run_grpcurl("GetTraders", payload6a)
        
        total_count_1 = None
        if result6a["success"]:
            response6a = result6a["response"]
            if "getTradersResponse" in response6a:
                traders6a = response6a["getTradersResponse"].get("traders", [])
                total_count_1 = response6a["getTradersResponse"].get("totalCount")
                print(f"📊 payment_method_type_id = 1: найдено {len(traders6a)} трейдеров, total_count = {total_count_1}")
                
                # Проверяем, что все трейдеры имеют payment_method_type_id = 1 (если поле присутствует)
                for i, trader in enumerate(traders6a):
                    # Поле может отсутствовать в ответе, проверяем если есть
                    if "paymentMethodTypeId" in trader:
                        pm_type_id = trader.get("paymentMethodTypeId")
                        if pm_type_id != 1:
                            print(f"❌ Трейдер {i+1} имеет payment_method_type_id = {pm_type_id}, ожидался 1")
                            tests_passed = False
            else:
                print("❌ Неправильная структура ответа для payment_method_type_id = 1 фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с payment_method_type_id = 1 фильтром: {result6a['error']}")
            tests_passed = False
        
        # Запрос с payment_method_type_id = 2
        payload6b = {"filter": {"payment_method_type_id": 2}}
        result6b = self.run_grpcurl("GetTraders", payload6b)
        
        total_count_2 = None
        if result6b["success"]:
            response6b = result6b["response"]
            if "getTradersResponse" in response6b:
                traders6b = response6b["getTradersResponse"].get("traders", [])
                total_count_2 = response6b["getTradersResponse"].get("totalCount")
                print(f"📊 payment_method_type_id = 2: найдено {len(traders6b)} трейдеров, total_count = {total_count_2}")
                
                # Проверяем, что все трейдеры имеют payment_method_type_id = 2 (если поле присутствует)
                for i, trader in enumerate(traders6b):
                    # Поле может отсутствовать в ответе, проверяем если есть
                    if "paymentMethodTypeId" in trader:
                        pm_type_id = trader.get("paymentMethodTypeId")
                        if pm_type_id != 2:
                            print(f"❌ Трейдер {i+1} имеет payment_method_type_id = {pm_type_id}, ожидался 2")
                            tests_passed = False
            else:
                print("❌ Неправильная структура ответа для payment_method_type_id = 2 фильтра")
                tests_passed = False
        else:
            print(f"❌ Ошибка запроса с payment_method_type_id = 2 фильтром: {result6b['error']}")
            tests_passed = False
        
        # Сравниваем total_count для разных значений payment_method_type_id
        if total_count_1 is not None and total_count_2 is not None:
            # Преобразуем в числа для сравнения
            try:
                count_1 = int(total_count_1) if isinstance(total_count_1, str) else total_count_1
                count_2 = int(total_count_2) if isinstance(total_count_2, str) else total_count_2
                
                if count_1 == count_2:
                    print(f"❌ ОШИБКА: total_count одинаковые для разных payment_method_type_id ({count_1} = {count_2})")
                    print("   Это может указывать на проблему с фильтрацией")
                    tests_passed = False
                else:
                    print(f"✅ total_count отличаются для разных payment_method_type_id ({count_1} ≠ {count_2})")
                    print("   Фильтрация работает корректно")
            except (ValueError, TypeError):
                print(f"❌ Ошибка при сравнении total_count: {total_count_1} и {total_count_2}")
                tests_passed = False
        else:
            print("❌ Не удалось получить total_count для сравнения")
            tests_passed = False
        
        self.test_results.append({
            "test": "GetTraders Filters",
            "status": "PASS" if tests_passed else "FAIL",
            "details": "Все фильтры работают корректно" if tests_passed else "Один или несколько фильтров работают некорректно"
        })
        
        return tests_passed

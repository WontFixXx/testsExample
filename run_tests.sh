#!/bin/bash

# Проверяем аргументы командной строки
CATEGORY="$1"

show_help() {
    echo "🚀 Запуск gRPC тестов Payment"
    echo "==============================================="
    echo
    echo "Использование: $0 [КАТЕГОРИЯ]"
    echo
    echo "Доступные категории:"
    echo "  currencies       - Тесты валют (💰)"
    echo "  regions          - Тесты регионов (🌍)"
    echo "  issuers          - Тесты эмитентов (🏦)"
    echo "  payment-types    - Тесты типов методов платежей (💳)"
    echo "  payment-methods  - Тесты методов платежей (💸)"
    echo "  orders           - Тесты Orders API (📦)"
    echo "  offers           - Тесты Offers API (📦)"
    echo "  traders          - Тесты Traders API (🧑‍💼)"
    echo "  create-traders   - Тесты создания трейдеров (📝)"
    echo "  register-traders - Тесты регистрации трейдеров (🔗)"
    echo "  all              - Все тесты (по умолчанию)"
    echo
    echo "Примеры:"
    echo "  $0                    # Запуск всех тестов"
    echo "  $0 all                # Запуск всех тестов"
    echo "  $0 currencies         # Только тесты валют"
    echo "  $0 traders            # Только тесты трейдеров"
    echo
}

# Если передан аргумент help или -h
if [[ "$CATEGORY" == "help" || "$CATEGORY" == "-h" || "$CATEGORY" == "--help" ]]; then
    show_help
    exit 0
fi

# Если категория не указана, запускаем все тесты
if [[ -z "$CATEGORY" ]]; then
    CATEGORY="all"
fi

echo "🚀 Запуск gRPC тестов Payment Gateway"
echo "==============================================="
echo "📂 Категория: $CATEGORY"
echo "⚙️  Конфигурация: используется config.py"
echo "🌐 gRPC хост: $(python3 -c "from config import DEFAULT_CONFIG; print(DEFAULT_CONFIG.grpc_host)")"
echo "🔌 gRPC порт: $(python3 -c "from config import DEFAULT_CONFIG; print(DEFAULT_CONFIG.grpc_port)")"
echo "🌍 HTTP хост: $(python3 -c "from config import DEFAULT_CONFIG; print(DEFAULT_CONFIG.http_host)")"
echo "🔌 HTTP порт: $(python3 -c "from config import DEFAULT_CONFIG; print(DEFAULT_CONFIG.http_port)")"
echo

echo "✅ Все зависимости найдены"
echo

# Глобальные переменные для подсчета тестов
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
# Массив для хранения детальных результатов
TEST_RESULTS=()

reset_test_counters() {
    TOTAL_TESTS=0
    PASSED_TESTS=0
    FAILED_TESTS=0
    TEST_RESULTS=()
}

run_test() {
    local test_name="$1"
    local test_cmd="$2"
    
    echo "🧪 Запуск: $test_name"
    echo "Команда: $test_cmd"
    echo "----------------------------------------"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_cmd"; then
        echo "✅ $test_name - УСПЕШНО"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("✅ $test_name - PASS")
    else
        echo "❌ $test_name - ПРОВАЛЕНО"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("❌ $test_name - FAIL")
        return 1
    fi
    echo
}

show_category_summary() {
    local category_name="$1"
    
    if [ $TOTAL_TESTS -gt 1 ]; then
        echo
        echo "================================================================================"
        echo "🎯 СВОДКА ПО КАТЕГОРИИ: $category_name"
        echo "================================================================================"
        echo "📊 Всего тестов: $TOTAL_TESTS"
        echo "✅ Прошло: $PASSED_TESTS"
        echo "❌ Провалено: $FAILED_TESTS"
        if [ $TOTAL_TESTS -gt 0 ]; then
            local success_rate=$((PASSED_TESTS * 100 / TOTAL_TESTS))
            echo "🎯 Процент успеха: $success_rate%"
        fi
        echo
        echo "📋 Детальные результаты:"
        for result in "${TEST_RESULTS[@]}"; do
            echo "   $result"
        done
        echo "================================================================================"
    fi
}

run_currencies_tests() {
    echo "💰 Запуск тестов валют:"
    echo
    
    run_test "USD Currency (ID=1)" "python3 grpc_tester_modular.py --test currency --currency-id 1"
    run_test "ETH Currency (ID=15)" "python3 grpc_tester_modular.py --test currency --currency-id 15"
    run_test "Currency Error (ID=100)" "python3 grpc_tester_modular.py --test currency_error"
    run_test "GetCurrencies Default" "python3 grpc_tester_modular.py --test currencies_default"
    run_test "GetCurrencies Order by Code DESC" "python3 grpc_tester_modular.py --test currencies_order_code"
    run_test "GetCurrencies Order by Decimal ASC" "python3 grpc_tester_modular.py --test currencies_order_decimal"
    run_test "GetCurrencies Pagination" "python3 grpc_tester_modular.py --test currencies_pagination"
    echo
}

run_regions_tests() {
    echo "🌍 Запуск тестов регионов:"
    echo
    
    run_test "UA Region (ID=1)" "python3 grpc_tester_modular.py --test region --region-id 1"
    run_test "Region Error (ID=100)" "python3 grpc_tester_modular.py --test region_error"
    run_test "GetRegions Default" "python3 grpc_tester_modular.py --test regions_default"
    run_test "GetRegions Order by ID ASC" "python3 grpc_tester_modular.py --test regions_order"
    run_test "GetRegions Order by Title ASC" "python3 grpc_tester_modular.py --test regions_order_title"
    run_test "GetRegions Pagination" "python3 grpc_tester_modular.py --test regions_pagination"
    echo
}

run_issuers_tests() {
    echo "🏦 Запуск тестов эмитентов:"
    echo
    
    run_test "Any Issuer (ID=1)" "python3 grpc_tester_modular.py --test issuer --issuer-id 1"
    run_test "VK Pay Issuer (ID=216)" "python3 grpc_tester_modular.py --test issuer --issuer-id 216"
    run_test "Issuer Error (ID=217)" "python3 grpc_tester_modular.py --test issuer_error"
    run_test "GetIssuers Default" "python3 grpc_tester_modular.py --test issuers_default"
    run_test "GetIssuers Order by Name DESC" "python3 grpc_tester_modular.py --test issuers_order_name"
    run_test "GetIssuers Pagination" "python3 grpc_tester_modular.py --test issuers_pagination"
    echo
}

run_payment_types_tests() {
    echo "💳 Запуск тестов типов методов платежей:"
    echo
    
    run_test "Credit Card Type (ID=1)" "python3 grpc_tester_modular.py --test payment_method_type --payment-method-type-id 1"
    run_test "Instant Payment Type (ID=2)" "python3 grpc_tester_modular.py --test payment_method_type --payment-method-type-id 2"
    run_test "PaymentMethodType Error (ID=3)" "python3 grpc_tester_modular.py --test payment_method_type_error"
    run_test "GetPaymentMethodTypes Default" "python3 grpc_tester_modular.py --test payment_method_types_default"
    run_test "GetPaymentMethodTypes Order by Name ASC" "python3 grpc_tester_modular.py --test payment_method_types_order_name"
    run_test "GetPaymentMethodTypes Pagination" "python3 grpc_tester_modular.py --test payment_method_types_pagination"
    echo
}

run_payment_methods_tests() {
    echo "💸 Запуск тестов методов платежей:"
    echo
    
    run_test "Card Number Method (ID=1)" "python3 grpc_tester_modular.py --test payment_method --payment-method-id 1"
    run_test "Phone Number Method (ID=26)" "python3 grpc_tester_modular.py --test payment_method --payment-method-id 26"
    run_test "PaymentMethod Error (ID=1000)" "python3 grpc_tester_modular.py --test payment_method_error"
    run_test "GetPaymentMethods Default" "python3 grpc_tester_modular.py --test payment_methods_default"
    run_test "GetPaymentMethods Order by ID DESC" "python3 grpc_tester_modular.py --test payment_methods_order_id"
    run_test "GetPaymentMethods Pagination" "python3 grpc_tester_modular.py --test payment_methods_pagination"
    run_test "GetPaymentMethods Filter" "python3 grpc_tester_modular.py --test payment_methods_filter"
    run_test "CreatePaymentMethod Default" "python3 grpc_tester_modular.py --test create_payment_method_default"
    echo
}

run_orders_tests() {
    echo "📦 Запуск тестов Orders API:"
    echo
    
    run_test "CreateOrder Basic" "python3 grpc_tester_modular.py --test create_order_basic"
    run_test "CreatePayoutOrder Basic" "python3 grpc_tester_modular.py --test create_payout_order_basic"
    run_test "CreateOrder PayIn Min Amount Error" "python3 grpc_tester_modular.py --test create_order_payin_min_amount_error"
    run_test "CreateOrder PayIn Max Amount Error" "python3 grpc_tester_modular.py --test create_order_payin_max_amount_error"
    run_test "CreateOrder Non Existing Company Error" "python3 grpc_tester_modular.py --test create_order_non_existing_company_error"
    echo
}

run_offers_tests() {
    echo "📦 Запуск тестов Offers API:"
    echo
    
    run_test "CreateOffer PayIn Default" "python3 grpc_tester_modular.py --test create_offer_payin_default"
    run_test "CreateOffer PayOut Default" "python3 grpc_tester_modular.py --test create_offer_payout_default"
    run_test "GetOffers Default" "python3 grpc_tester_modular.py --test get_offers_default"
    run_test "GetOffer Default" "python3 grpc_tester_modular.py --test get_offer_default"
    run_test "Pause Offer" "python3 grpc_tester_modular.py --test pause_offer"
    run_test "Cancel Offer Without Orders" "python3 grpc_tester_modular.py --test cancel_offer_without_orders"
    run_test "Error Reactivate Active Offer" "python3 grpc_tester_modular.py --test error_reactivate_active_offer"
    run_test "Cancel Active Offer With Orders" "python3 grpc_tester_modular.py --test cancel_active_offer_with_orders"
    run_test "Activate Paused Offer" "python3 grpc_tester_modular.py --test activate_paused_offer"
    run_test "Transition Offer On Hold To Inactive" "python3 grpc_tester_modular.py --test transition_offer_on_hold_to_inactive"
    run_test "Transition Offer On Hold To Canceled" "python3 grpc_tester_modular.py --test transition_offer_on_hold_to_canceled"
    run_test "Error Pause Already Paused Offer" "python3 grpc_tester_modular.py --test error_pause_already_paused_offer"
    run_test "Error Reactivate Inactive Offer" "python3 grpc_tester_modular.py --test error_reactivate_inactive_offer"
    run_test "Error Cancel Inactive Offer" "python3 grpc_tester_modular.py --test error_cancel_inactive_offer"
    run_test "Error Cancel Canceled Offer" "python3 grpc_tester_modular.py --test error_cancel_canceled_offer"
    run_test "Error Reactivate Canceled Offer" "python3 grpc_tester_modular.py --test error_reactivate_canceled_offer"
    run_test "Error Pause Canceled Offer" "python3 grpc_tester_modular.py --test error_pause_canceled_offer"
    run_test "Error Pause Inactive Offer" "python3 grpc_tester_modular.py --test error_pause_inactive_offer"
    echo
}

run_traders_tests() {
    echo "🧑‍💼 Запуск тестов Traders API:"
    echo
    
    run_test "GetTrader Default" "python3 grpc_tester_modular.py --test get_trader_default"
    run_test "GetTrader Error" "python3 grpc_tester_modular.py --test get_trader_not_found_error"
    run_test "GetTrader ID Invalid Error" "python3 grpc_tester_modular.py --test get_trader_id_invalid_error"
    run_test "GetTraders Default" "python3 grpc_tester_modular.py --test get_traders_default"
    run_test "GetTraders Order ASC" "python3 grpc_tester_modular.py --test get_traders_order_asc"
    run_test "GetTraders Order DESC" "python3 grpc_tester_modular.py --test get_traders_order_desc"
    run_test "GetTraders Pagination" "python3 grpc_tester_modular.py --test get_traders_pagination"
    run_test "GetTraders Filters" "python3 grpc_tester_modular.py --test get_traders_filters"
    echo
}

run_create_traders_tests() {
    echo "📝 Запуск тестов создания трейдеров (HTTP REST API):"
    echo
    
    run_test "Create Trader Default" "python3 grpc_tester_modular.py --test create_trader_default"
    run_test "Create Trader Duplicate UUID" "python3 grpc_tester_modular.py --test create_trader_duplicate_uuid"
    run_test "Create Trader Duplicate Email" "python3 grpc_tester_modular.py --test create_trader_duplicate_email"
    run_test "Create Trader Invalid UUID" "python3 grpc_tester_modular.py --test create_trader_invalid_uuid"
    run_test "Create Trader Empty Email" "python3 grpc_tester_modular.py --test create_trader_empty_email"
    run_test "Create Trader Long Email" "python3 grpc_tester_modular.py --test create_trader_long_email"
    echo
}

run_register_traders_tests() {
    echo "🔗 Запуск тестов регистрации трейдеров (HTTP + gRPC):"
    echo
    
    run_test "Register Trader Enabled" "python3 grpc_tester_modular.py --test register_trader_enabled"
    run_test "Register Trader Disabled" "python3 grpc_tester_modular.py --test register_trader_disabled"
    run_test "Register Trader Invalid Status" "python3 grpc_tester_modular.py --test register_trader_invalid_status"
    echo
}

# Все тесты организованы в функции выше
# Выполнение происходит через case statement ниже

# Выбор категории тестов для запуска
case "$CATEGORY" in
    "currencies")
        reset_test_counters
        run_currencies_tests
        show_category_summary "Валюты (💰)"
        ;;
    "regions")
        reset_test_counters
        run_regions_tests
        show_category_summary "Регионы (🌍)"
        ;;
    "issuers")
        reset_test_counters
        run_issuers_tests
        show_category_summary "Эмитенты (🏦)"
        ;;
    "payment-types")
        reset_test_counters
        run_payment_types_tests
        show_category_summary "Типы методов платежей (💳)"
        ;;
    "payment-methods")
        reset_test_counters
        run_payment_methods_tests
        show_category_summary "Методы платежей (💸)"
        ;;
    "orders")
        reset_test_counters
        run_orders_tests
        show_category_summary "Orders API (📦)"
        ;;
    "offers")
        reset_test_counters
        run_offers_tests
        show_category_summary "Offers API (📦)"
        ;;
    "traders")
        reset_test_counters
        run_traders_tests
        show_category_summary "Traders API (🧑‍💼)"
        ;;
    "create-traders")
        reset_test_counters
        run_create_traders_tests
        show_category_summary "Создание трейдеров (📝)"
        ;;
    "register-traders")
        reset_test_counters
        run_register_traders_tests
        show_category_summary "Регистрация трейдеров (🔗)"
        ;;
    "all")
        reset_test_counters
        run_currencies_tests
        run_regions_tests
        run_issuers_tests
        run_payment_types_tests
        run_payment_methods_tests
        run_orders_tests
        run_offers_tests
        run_traders_tests
        run_create_traders_tests
        run_register_traders_tests
        show_category_summary "ВСЕ ТЕСТЫ"
        ;;
    *)
        echo "❌ Неизвестная категория: $CATEGORY"
        echo
        show_help
        exit 1
        ;;
esac

echo "🎉 Тесты категории '$CATEGORY' завершены!"
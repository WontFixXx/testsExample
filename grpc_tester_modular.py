import argparse
import subprocess
import sys
from config import DEFAULT_CONFIG
from gwconfig_tests import GrpcTestConfig, CurrencyTester, RegionTester, IssuerTester, PaymentMethodTypeTester, PaymentMethodTester
from orders_api_tests import OrdersApiTestConfig, CreateOrderTester
from offers_api_tests import OffersApiTestConfig, CreateOfferTester, GetOffersTester, UpdateOfferTester
from traders_api_tests import GetTraderTester, GetTradersTester, CreateTraderTester, RegisterTraderTester


def main():
    parser = argparse.ArgumentParser(description="Модульный gRPC Tester для Payment Gateway")
    parser.add_argument("--host", default=DEFAULT_CONFIG.grpc_host, help=f"Хост сервера (по умолчанию: {DEFAULT_CONFIG.grpc_host})")
    parser.add_argument("--port", type=int, default=DEFAULT_CONFIG.grpc_port, help=f"Порт сервера (по умолчанию: {DEFAULT_CONFIG.grpc_port})")
    parser.add_argument("--currency-id", type=int, default=1, help="ID валюты для тестирования (по умолчанию: 1)")
    parser.add_argument("--region-id", type=int, default=1, help="ID региона для тестирования (по умолчанию: 1)")
    parser.add_argument("--issuer-id", type=int, default=1, help="ID эмитента для тестирования (по умолчанию: 1)")
    parser.add_argument("--payment-method-type-id", type=int, default=1, help="ID типа метода платежа для тестирования (по умолчанию: 1)")
    parser.add_argument("--payment-method-id", type=int, default=1, help="ID метода платежа для тестирования (по умолчанию: 1)")
    parser.add_argument("--trader-id", default="550e8400-e29b-41d4-a716-446655440001", help="ID трейдера для тестирования (по умолчанию: 550e8400-e29b-41d4-a716-446655440001)")
    parser.add_argument("--test", choices=["currency", "currency_error", "currencies_default", "currencies_order_code", "currencies_order_decimal", "currencies_pagination", "region", "region_error", "regions_default", "regions_order", "regions_order_title", "regions_pagination", "issuer", "issuer_error", "issuers_default", "issuers_order_name", "issuers_pagination", "payment_method_type", "payment_method_type_error", "payment_method_types_default", "payment_method_types_order_name", "payment_method_types_pagination", "payment_method", "payment_method_error", "payment_methods_default", "payment_methods_order_id", "payment_methods_pagination", "payment_methods_filter", "create_payment_method_default", "create_order_basic", "create_payout_order_basic", "create_order_payin_min_amount_error", "create_order_payin_max_amount_error", "create_order_non_existing_company_error", "create_offer_payin_default", "create_offer_payout_default", "get_offers_default", "get_offer_default", "cancel_active_offer_with_orders", "activate_paused_offer", "transition_offer_on_hold_to_inactive", "transition_offer_on_hold_to_canceled", "error_pause_already_paused_offer", "pause_offer", "cancel_offer_without_orders", "error_reactivate_active_offer", "error_reactivate_inactive_offer", "error_cancel_inactive_offer", "error_cancel_canceled_offer", "error_reactivate_canceled_offer", "error_pause_canceled_offer", "error_pause_inactive_offer", "get_trader_default", "get_trader_not_found_error", "get_trader_id_invalid_error", "get_traders_default", "get_traders_order_asc", "get_traders_order_desc", "get_traders_pagination", "get_traders_filters", "create_trader_default", "create_trader_duplicate_uuid", "create_trader_duplicate_email", "create_trader_invalid_uuid", "create_trader_empty_email", "create_trader_long_email", "register_trader_enabled", "register_trader_disabled", "register_trader_invalid_status", "all"], default="currency", help="Какой тест запустить")
    
    args = parser.parse_args()
    
    try:
        subprocess.run(["grpcurl", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ grpcurl не найден. Установите его:")
        print("   macOS: brew install grpcurl")
        print("   Linux: apt-get install grpcurl или скачайте с GitHub")
        sys.exit(1)
    
    config = GrpcTestConfig(
        host=args.host,
        port=args.port,
        insecure=DEFAULT_CONFIG.grpc_insecure
    )
    
    print(f"🎯 Запускаем gRPC тесты на {config.host}:{config.port}")
    
    success = True
    active_testers = []
    all_test_results = []  # Список для хранения результатов всех тестов
    
    if args.test in ["currency", "currency_error", "currencies_default", "currencies_order_code", "currencies_order_decimal", "currencies_pagination", "all"]:
        currency_tester = CurrencyTester(config)
        active_testers.append(currency_tester)
        
        if args.test in ["currency", "all"]:
            result = currency_tester.test_get_currency(args.currency_id)
            success &= result
            all_test_results.append({"test": "GetCurrency", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["currency_error", "all"]:
            result = currency_tester.test_get_currency_error(100)
            success &= result
            all_test_results.append({"test": "GetCurrency Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["currencies_default", "all"]:
            result = currency_tester.test_get_currencies_default()
            success &= result
            all_test_results.append({"test": "GetCurrencies Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["currencies_order_code", "all"]:
            result = currency_tester.test_get_currencies_order_code_desc()
            success &= result
            all_test_results.append({"test": "GetCurrencies Order Code", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["currencies_order_decimal", "all"]:
            result = currency_tester.test_get_currencies_order_decimal_asc()
            success &= result
            all_test_results.append({"test": "GetCurrencies Order Decimal", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["currencies_pagination", "all"]:
            result = currency_tester.test_get_currencies_pagination()
            success &= result
            all_test_results.append({"test": "GetCurrencies Pagination", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["region", "region_error", "regions_default", "regions_order", "regions_order_title", "regions_pagination", "all"]:
        region_tester = RegionTester(config)
        active_testers.append(region_tester)
        
        if args.test in ["region", "all"]:
            result = region_tester.test_get_region(args.region_id)
            success &= result
            all_test_results.append({"test": "GetRegion", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["region_error", "all"]:
            result = region_tester.test_get_region_error(100)
            success &= result
            all_test_results.append({"test": "GetRegion Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["regions_default", "all"]:
            result = region_tester.test_get_regions_default()
            success &= result
            all_test_results.append({"test": "GetRegions Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["regions_order", "all"]:
            result = region_tester.test_get_regions_order_code_desc()
            success &= result
            all_test_results.append({"test": "GetRegions Order", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["regions_order_title", "all"]:
            result = region_tester.test_get_regions_order_title_asc()
            success &= result
            all_test_results.append({"test": "GetRegions Order Title", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["regions_pagination", "all"]:
            result = region_tester.test_get_regions_pagination()
            success &= result
            all_test_results.append({"test": "GetRegions Pagination", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["issuer", "issuer_error", "issuers_default", "issuers_order_name", "issuers_pagination", "all"]:
        issuer_tester = IssuerTester(config)
        active_testers.append(issuer_tester)
        
        if args.test in ["issuer", "all"]:
            result = issuer_tester.test_get_issuer(args.issuer_id)
            success &= result
            all_test_results.append({"test": "GetIssuer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["issuer_error", "all"]:
            result = issuer_tester.test_get_issuer_error(217)
            success &= result
            all_test_results.append({"test": "GetIssuer Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["issuers_default", "all"]:
            result = issuer_tester.test_get_issuers_default()
            success &= result
            all_test_results.append({"test": "GetIssuers Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["issuers_order_name", "all"]:
            result = issuer_tester.test_get_issuers_order_name_desc()
            success &= result
            all_test_results.append({"test": "GetIssuers Order Name", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["issuers_pagination", "all"]:
            result = issuer_tester.test_get_issuers_pagination()
            success &= result
            all_test_results.append({"test": "GetIssuers Pagination", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["payment_method_type", "payment_method_type_error", "payment_method_types_default", "payment_method_types_order_name", "payment_method_types_pagination", "all"]:
        payment_method_type_tester = PaymentMethodTypeTester(config)
        active_testers.append(payment_method_type_tester)
        
        if args.test in ["payment_method_type", "all"]:
            result = payment_method_type_tester.test_get_payment_method_type(args.payment_method_type_id)
            success &= result
            all_test_results.append({"test": "GetPaymentMethodType", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_method_type_error", "all"]:
            result = payment_method_type_tester.test_get_payment_method_type_error(3)
            success &= result
            all_test_results.append({"test": "GetPaymentMethodType Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_method_types_default", "all"]:
            result = payment_method_type_tester.test_get_payment_method_types_default()
            success &= result
            all_test_results.append({"test": "GetPaymentMethodTypes Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_method_types_order_name", "all"]:
            result = payment_method_type_tester.test_get_payment_method_types_order_name_asc()
            success &= result
            all_test_results.append({"test": "GetPaymentMethodTypes Order Name", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_method_types_pagination", "all"]:
            result = payment_method_type_tester.test_get_payment_method_types_pagination()
            success &= result
            all_test_results.append({"test": "GetPaymentMethodTypes Pagination", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["payment_method", "payment_method_error", "payment_methods_default", "payment_methods_order_id", "payment_methods_pagination", "payment_methods_filter", "create_payment_method_default", "all"]:
        payment_method_tester = PaymentMethodTester(config)
        active_testers.append(payment_method_tester)
        
        if args.test in ["payment_method", "all"]:
            result = payment_method_tester.test_get_payment_method(args.payment_method_id)
            success &= result
            all_test_results.append({"test": "GetPaymentMethod", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_method_error", "all"]:
            result = payment_method_tester.test_get_payment_method_error(1000)
            success &= result
            all_test_results.append({"test": "GetPaymentMethod Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_methods_default", "all"]:
            result = payment_method_tester.test_get_payment_methods_default()
            success &= result
            all_test_results.append({"test": "GetPaymentMethods Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_methods_order_id", "all"]:
            result = payment_method_tester.test_get_payment_methods_order_id_desc()
            success &= result
            all_test_results.append({"test": "GetPaymentMethods Order ID", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_methods_pagination", "all"]:
            result = payment_method_tester.test_get_payment_methods_pagination()
            success &= result
            all_test_results.append({"test": "GetPaymentMethods Pagination", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["payment_methods_filter", "all"]:
            result = payment_method_tester.test_get_payment_methods_filter()
            success &= result
            all_test_results.append({"test": "GetPaymentMethods Filter", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_payment_method_default", "all"]:
            result = payment_method_tester.test_create_payment_method_default()
            success &= result
            all_test_results.append({"test": "CreatePaymentMethod Default", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["create_order_basic", "create_payout_order_basic", "create_order_payin_min_amount_error", "create_order_payin_max_amount_error", "create_order_non_existing_company_error", "all"]:
        orders_config = OrdersApiTestConfig(host=args.host, port=args.port, insecure=DEFAULT_CONFIG.grpc_insecure)
        create_order_tester = CreateOrderTester(orders_config)
        active_testers.append(create_order_tester)
        
        if args.test in ["create_order_basic", "all"]:
            result = create_order_tester.test_create_order_basic()
            success &= result
            all_test_results.append({"test": "CreateOrder Basic", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_payout_order_basic", "all"]:
            result = create_order_tester.test_create_payout_order_basic()
            success &= result
            all_test_results.append({"test": "CreatePayoutOrder Basic", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_order_payin_min_amount_error", "all"]:
            result = create_order_tester.test_create_order_payin_min_amount_error()
            success &= result
            all_test_results.append({"test": "CreateOrder PayIn Min Amount Error", "status": "PASS" if result else "FAIL"})

        if args.test in ["create_order_payin_max_amount_error", "all"]:
            result = create_order_tester.test_create_order_payin_max_amount_error()
            success &= result
            all_test_results.append({"test": "CreateOrder PayIn Max Amount Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_order_non_existing_company_error", "all"]:
            result = create_order_tester.test_create_order_non_existing_company_error()
            success &= result
            all_test_results.append({"test": "CreateOrder Non Existing Company Error", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["create_offer_payin_default", "create_offer_payout_default", "get_offers_default", "get_offer_default", "cancel_active_offer_with_orders", "activate_paused_offer", "transition_offer_on_hold_to_inactive", "transition_offer_on_hold_to_canceled", "error_pause_already_paused_offer", "pause_offer", "cancel_offer_without_orders", "error_reactivate_active_offer", "error_reactivate_inactive_offer", "error_cancel_inactive_offer", "error_cancel_canceled_offer", "error_reactivate_canceled_offer", "error_pause_canceled_offer", "error_pause_inactive_offer", "all"]:
        offers_config = OffersApiTestConfig(host=args.host, port=args.port, insecure=DEFAULT_CONFIG.grpc_insecure)
        
        if args.test in ["create_offer_payin_default", "all"]:
            create_offer_tester = CreateOfferTester(offers_config)
            active_testers.append(create_offer_tester)
            result = create_offer_tester.test_create_offer_payin_default()
            success &= result
            all_test_results.append({"test": "CreateOffer PayIn Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_offer_payout_default", "all"]:
            create_offer_tester = CreateOfferTester(offers_config)
            active_testers.append(create_offer_tester)
            result = create_offer_tester.test_create_offer_payout_default()
            success &= result
            all_test_results.append({"test": "CreateOffer PayOut Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["get_offers_default", "all"]:
            get_offers_tester = GetOffersTester(offers_config)
            active_testers.append(get_offers_tester)
            result = get_offers_tester.test_get_offers_default()
            success &= result
            all_test_results.append({"test": "GetOffers Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["get_offer_default", "all"]:
            get_offers_tester = GetOffersTester(offers_config)
            active_testers.append(get_offers_tester)
            result = get_offers_tester.test_get_offer_default()
            success &= result
            all_test_results.append({"test": "GetOffer Default", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["cancel_active_offer_with_orders", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_cancel_active_offer_with_orders()
            success &= result
            all_test_results.append({"test": "Cancel Active Offer With Orders", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["activate_paused_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_activate_paused_offer()
            success &= result
            all_test_results.append({"test": "Activate Paused Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["transition_offer_on_hold_to_inactive", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_transition_offer_on_hold_to_inactive()
            success &= result
            all_test_results.append({"test": "Transition Offer On Hold To Inactive", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["transition_offer_on_hold_to_canceled", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_transition_offer_on_hold_to_canceled()
            success &= result
            all_test_results.append({"test": "Transition Offer On Hold To Canceled", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_pause_already_paused_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_pause_already_paused_offer()
            success &= result
            all_test_results.append({"test": "Error Pause Already Paused Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["pause_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_pause_offer()
            success &= result
            all_test_results.append({"test": "Pause Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["cancel_offer_without_orders", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_cancel_offer_without_orders()
            success &= result
            all_test_results.append({"test": "Cancel Offer Without Orders", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_reactivate_active_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_reactivate_active_offer()
            success &= result
            all_test_results.append({"test": "Error Reactivate Active Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_reactivate_inactive_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_reactivate_inactive_offer()
            success &= result
            all_test_results.append({"test": "Error Reactivate Inactive Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_cancel_inactive_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_cancel_inactive_offer()
            success &= result
            all_test_results.append({"test": "Error Cancel Inactive Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_cancel_canceled_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_cancel_canceled_offer()
            success &= result
            all_test_results.append({"test": "Error Cancel Canceled Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_reactivate_canceled_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_reactivate_canceled_offer()
            success &= result
            all_test_results.append({"test": "Error Reactivate Canceled Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_pause_canceled_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_pause_canceled_offer()
            success &= result
            all_test_results.append({"test": "Error Pause Canceled Offer", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["error_pause_inactive_offer", "all"]:
            update_offer_tester = UpdateOfferTester(offers_config)
            active_testers.append(update_offer_tester)
            result = update_offer_tester.test_error_pause_inactive_offer()
            success &= result
            all_test_results.append({"test": "Error Pause Inactive Offer", "status": "PASS" if result else "FAIL"})
    
    if args.test in ["get_trader_default", "get_trader_not_found_error", "get_trader_id_invalid_error", "get_traders_default", "get_traders_order_asc", "get_traders_order_desc", "get_traders_pagination", "get_traders_filters", "create_trader_default", "create_trader_duplicate_uuid", "create_trader_duplicate_email", "create_trader_invalid_uuid", "create_trader_empty_email", "create_trader_long_email", "register_trader_enabled", "register_trader_disabled", "register_trader_invalid_status", "all"]:
        traders_config = GrpcTestConfig(host=args.host, port=args.port, insecure=DEFAULT_CONFIG.grpc_insecure)
        
        if args.test in ["get_trader_default", "get_trader_not_found_error", "get_trader_id_invalid_error", "all"]:
            get_trader_tester = GetTraderTester(traders_config)
            active_testers.append(get_trader_tester)
            
            if args.test in ["get_trader_default", "all"]:
                result = get_trader_tester.test_get_trader_default()
                success &= result
                all_test_results.append({"test": "GetTrader Default", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["get_trader_not_found_error", "all"]:
                result = get_trader_tester.test_get_trader_not_found_error()
                success &= result
                all_test_results.append({"test": "GetTrader Error", "status": "PASS" if result else "FAIL"})

            if args.test in ["get_trader_id_invalid_error", "all"]:
                result = get_trader_tester.test_get_trader_id_invalid_error()
                success &= result
                all_test_results.append({"test": "GetTrader ID Invalid Error", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["get_traders_default", "get_traders_order_asc", "get_traders_order_desc", "get_traders_pagination", "get_traders_filters", "all"]:
            get_traders_tester = GetTradersTester(traders_config)
            active_testers.append(get_traders_tester)
            
            if args.test in ["get_traders_default", "all"]:
                result = get_traders_tester.test_get_traders_default()
                success &= result
                all_test_results.append({"test": "GetTraders Default", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["get_traders_order_asc", "all"]:
                result = get_traders_tester.test_get_traders_order_asc()
                success &= result
                all_test_results.append({"test": "GetTraders Order ASC", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["get_traders_order_desc", "all"]:
                result = get_traders_tester.test_get_traders_order_desc()
                success &= result
                all_test_results.append({"test": "GetTraders Order DESC", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["get_traders_pagination", "all"]:
                result = get_traders_tester.test_get_traders_pagination()
                success &= result
                all_test_results.append({"test": "GetTraders Pagination", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["get_traders_filters", "all"]:
                result = get_traders_tester.test_get_traders_filters()
                success &= result
                all_test_results.append({"test": "GetTraders Filters", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["create_trader_default", "create_trader_duplicate_uuid", "create_trader_duplicate_email", "create_trader_invalid_uuid", "create_trader_empty_email", "create_trader_long_email", "all"]:
            create_trader_tester = CreateTraderTester(traders_config)
            active_testers.append(create_trader_tester)
            
            if args.test in ["create_trader_default", "all"]:
                result = create_trader_tester.test_create_trader_default()
                success &= result
                all_test_results.append({"test": "Create Trader Default", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["create_trader_duplicate_uuid", "all"]:
                result = create_trader_tester.test_create_trader_duplicate_uuid()
                success &= result
                all_test_results.append({"test": "Create Trader Duplicate UUID", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["create_trader_duplicate_email", "all"]:
                result = create_trader_tester.test_create_trader_duplicate_email()
                success &= result
                all_test_results.append({"test": "Create Trader Duplicate Email", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["create_trader_invalid_uuid", "all"]:
                result = create_trader_tester.test_create_trader_invalid_uuid()
                success &= result
                all_test_results.append({"test": "Create Trader Invalid UUID", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["create_trader_empty_email", "all"]:
                result = create_trader_tester.test_create_trader_empty_email()
                success &= result
                all_test_results.append({"test": "Create Trader Empty Email", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["create_trader_long_email", "all"]:
                result = create_trader_tester.test_create_trader_long_email()
                success &= result
                all_test_results.append({"test": "Create Trader Long Email", "status": "PASS" if result else "FAIL"})
        
        if args.test in ["register_trader_enabled", "register_trader_disabled", "register_trader_invalid_status", "all"]:
            register_trader_tester = RegisterTraderTester(traders_config)
            active_testers.append(register_trader_tester)
            
            if args.test in ["register_trader_enabled", "all"]:
                result = register_trader_tester.test_register_trader_enabled()
                success &= result
                all_test_results.append({"test": "Register Trader Enabled", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["register_trader_disabled", "all"]:
                result = register_trader_tester.test_register_trader_disabled()
                success &= result
                all_test_results.append({"test": "Register Trader Disabled", "status": "PASS" if result else "FAIL"})
            
            if args.test in ["register_trader_invalid_status", "all"]:
                result = register_trader_tester.test_register_trader_invalid_status()
                success &= result
                all_test_results.append({"test": "Register Trader Invalid Status", "status": "PASS" if result else "FAIL"})
    
    # Выводим общую сводку только если выполнено больше одного теста или запущен тест "all"
    show_summary = len(all_test_results) > 1 or args.test == "all"
    
    if all_test_results and show_summary:
        print("\n" + "=" * 80)
        print("🎯 ОБЩАЯ СВОДКА ПО ВСЕМ ТЕСТАМ")
        print("=" * 80)
        
        passed = sum(1 for test in all_test_results if test["status"] == "PASS")
        failed = sum(1 for test in all_test_results if test["status"] == "FAIL")
        total = len(all_test_results)
        
        print(f"📊 Всего тестов: {total}")
        print(f"✅ Прошло: {passed}")
        print(f"❌ Провалено: {failed}")
        print(f"🎯 Процент успеха: {(passed/total*100):.1f}%" if total > 0 else "Нет тестов")
        print()
        
        print("📋 Детальные результаты:")
        for test in all_test_results:
            status_icon = "✅" if test["status"] == "PASS" else "❌"
            print(f"   {status_icon} {test['test']} - {test['status']}")
        
        print("=" * 80)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
# 一般的なISO 4217通貨コードの一部抜粋
valid_currency_codes = {
        "USD", "EUR", "JPY", "GBP", "AUD", "CAD",
        "CHF", "CNY", "SEK", "NZD", "MXN", "SGD",
        "HKD", "NOK", "KRW", "TRY", "RUB", "INR",
        "BRL", "ZAR", "DKK", "PLN", "TWD", "THB", "MYR"
}

def is_valid_currency_code(currency_code):
    return currency_code in valid_currency_codes

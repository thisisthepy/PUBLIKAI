import requests
import json
from typing import Dict, Any, List
from datetime import datetime


class CurrencyAPI:
    """Currency exchange rate API wrapper using free services."""
    
    def __init__(self):
        """Initialize Currency API client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Using exchangerate-api.com (free tier: 1500 requests/month)
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
    
    def get_exchange_rates(self, base_currency: str) -> Dict[str, Any]:
        """
        Get exchange rates from the free API.
        
        Args:
            base_currency: Base currency code (e.g., 'USD', 'EUR', 'KRW')
            
        Returns:
            Dict containing exchange rates or error
        """
        try:
            # Try primary free API (exchangerate-api.com)
            url = f"{self.base_url}/{base_currency.upper()}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "base": data.get("base", base_currency.upper()),
                "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
                "rates": data.get("rates", {}),
                "timestamp": datetime.now().isoformat(),
                "source": "ExchangeRate-API"
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch exchange rates: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response from exchange rate service"}
        except Exception as e:
            return {"error": f"Failed to get exchange rates: {str(e)}"}
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """
        Convert amount from one currency to another.
        
        Args:
            amount: Amount to convert
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            Dict with conversion result
        """
        try:
            # Get exchange rates with from_currency as base
            rates_data = self.get_exchange_rates(from_currency)
            
            if "error" in rates_data:
                return rates_data
            
            rates = rates_data.get("rates", {})
            
            # Check if target currency is available
            if to_currency.upper() not in rates:
                return {"error": f"Currency '{to_currency}' not found in exchange rates"}
            
            # Perform conversion
            exchange_rate = rates[to_currency.upper()]
            converted_amount = amount * exchange_rate
            
            return {
                "original_amount": amount,
                "from_currency": from_currency.upper(),
                "to_currency": to_currency.upper(),
                "exchange_rate": exchange_rate,
                "converted_amount": round(converted_amount, 2),
                "date": rates_data.get("date"),
                "source": rates_data.get("source")
            }
            
        except Exception as e:
            return {"error": f"Currency conversion failed: {str(e)}"}
    
    def get_popular_currencies(self) -> List[Dict[str, str]]:
        """Get list of popular currencies with their info."""
        return [
            {"code": "USD", "name": "US Dollar", "symbol": "$", "country": "United States"},
            {"code": "EUR", "name": "Euro", "symbol": "€", "country": "European Union"},
            {"code": "GBP", "name": "British Pound", "symbol": "£", "country": "United Kingdom"},
            {"code": "JPY", "name": "Japanese Yen", "symbol": "¥", "country": "Japan"},
            {"code": "KRW", "name": "South Korean Won", "symbol": "₩", "country": "South Korea"},
            {"code": "CNY", "name": "Chinese Yuan", "symbol": "¥", "country": "China"},
            {"code": "CAD", "name": "Canadian Dollar", "symbol": "C$", "country": "Canada"},
            {"code": "AUD", "name": "Australian Dollar", "symbol": "A$", "country": "Australia"},
            {"code": "CHF", "name": "Swiss Franc", "symbol": "CHF", "country": "Switzerland"},
            {"code": "SEK", "name": "Swedish Krona", "symbol": "kr", "country": "Sweden"},
            {"code": "NOK", "name": "Norwegian Krone", "symbol": "kr", "country": "Norway"},
            {"code": "SGD", "name": "Singapore Dollar", "symbol": "S$", "country": "Singapore"},
            {"code": "HKD", "name": "Hong Kong Dollar", "symbol": "HK$", "country": "Hong Kong"},
            {"code": "INR", "name": "Indian Rupee", "symbol": "₹", "country": "India"},
            {"code": "BRL", "name": "Brazilian Real", "symbol": "R$", "country": "Brazil"},
        ]


# Global currency API instance
currency_api = CurrencyAPI()


def get_exchange_rate(from_currency: str, to_currency: str, amount: float = 1.0) -> str:
    """
    Get exchange rate and convert currency amount.
    Uses free exchange rate APIs - no API key required.
    
    Args:
        from_currency (str): Source currency code (e.g., 'USD', 'EUR', 'KRW')
        to_currency (str): Target currency code (e.g., 'USD', 'EUR', 'KRW')
        amount (float): Amount to convert (default: 1.0)
        
    Returns:
        str: Formatted string with exchange rate and conversion result
    """
    try:
        # Validate inputs
        if amount <= 0:
            return "Error: Amount must be greater than 0"
        
        if len(from_currency) != 3 or len(to_currency) != 3:
            return "Error: Currency codes must be 3 letters (e.g., USD, EUR, KRW)"
        
        # Perform conversion
        conversion_result = currency_api.convert_currency(amount, from_currency, to_currency)
        
        if "error" in conversion_result:
            return f"Error: {conversion_result['error']}"
        
        # Get currency info for better formatting
        popular_currencies = currency_api.get_popular_currencies()
        currency_info = {curr["code"]: curr for curr in popular_currencies}
        
        from_info = currency_info.get(from_currency.upper(), {"name": from_currency.upper(), "symbol": ""})
        to_info = currency_info.get(to_currency.upper(), {"name": to_currency.upper(), "symbol": ""})
        
        # Format response
        from_symbol = from_info.get("symbol", "")
        to_symbol = to_info.get("symbol", "")
        
        response = f"Currency Exchange Rate:\n\n"
        
        # Conversion result
        response += f"💱 {from_symbol}{amount:,.2f} {from_currency.upper()} = {to_symbol}{conversion_result['converted_amount']:,.2f} {to_currency.upper()}\n\n"
        
        # Exchange rate details
        response += f"📊 Exchange Rate Details:\n"
        response += f"   • 1 {from_currency.upper()} = {conversion_result['exchange_rate']:.6f} {to_currency.upper()}\n"
        response += f"   • 1 {to_currency.upper()} = {1/conversion_result['exchange_rate']:.6f} {from_currency.upper()}\n\n"
        
        # Currency information
        response += f"🌍 Currency Information:\n"
        response += f"   • {from_info['name']} ({from_currency.upper()})\n"
        response += f"   • {to_info['name']} ({to_currency.upper()})\n\n"
        
        # Rate date and source
        response += f"📅 Rate Date: {conversion_result.get('date', 'Unknown')}\n"
        response += f"📡 Source: {conversion_result.get('source', 'Exchange Rate API')}"
        
        return response
        
    except Exception as e:
        return f"Error getting exchange rate: {str(e)}"


def get_currency_list() -> str:
    """
    Get list of popular supported currencies.
    
    Returns:
        str: Formatted list of popular currencies
    """
    try:
        currencies = currency_api.get_popular_currencies()
        
        response = "Popular Supported Currencies:\n\n"
        
        for curr in currencies:
            response += f"💰 {curr['code']} - {curr['name']}\n"
            response += f"   Symbol: {curr['symbol']}\n"
            response += f"   Country: {curr['country']}\n\n"
        
        response += "💡 Usage: get_exchange_rate('USD', 'EUR', 100)\n"
        response += "💡 Supports 100+ currencies worldwide"
        
        return response
        
    except Exception as e:
        return f"Error getting currency list: {str(e)}"


def get_multiple_rates(base_currency: str, target_currencies: List[str]) -> str:
    """
    Get exchange rates from one base currency to multiple target currencies.
    
    Args:
        base_currency: Base currency code
        target_currencies: List of target currency codes
        
    Returns:
        Formatted string with multiple exchange rates
    """
    try:
        rates_data = currency_api.get_exchange_rates(base_currency)
        
        if "error" in rates_data:
            return f"Error: {rates_data['error']}"
        
        rates = rates_data.get("rates", {})
        
        response = f"Exchange Rates from {base_currency.upper()}:\n"
        response += f"📅 Date: {rates_data.get('date', 'Unknown')}\n\n"
        
        for target_currency in target_currencies:
            target = target_currency.upper()
            if target in rates:
                rate = rates[target]
                response += f"💱 1 {base_currency.upper()} = {rate:.4f} {target}\n"
            else:
                response += f"❌ {target} - Rate not available\n"
        
        response += f"\n📡 Source: {rates_data.get('source', 'Exchange Rate API')}"
        
        return response
        
    except Exception as e:
        return f"Error getting multiple rates: {str(e)}"


# Example usage and test cases
if __name__ == '__main__':
    test_conversions = [
        ("USD", "EUR", 100),
        ("KRW", "USD", 1000000),
        ("JPY", "GBP", 10000),
        ("EUR", "KRW", 50),
        ("USD", "JPY", 1),
    ]
    
    print("Currency Exchange API Test Results:")
    print("=" * 60)
    
    # Test currency conversions
    for from_curr, to_curr, amount in test_conversions:
        print(f"\nTesting: {amount} {from_curr} to {to_curr}")
        print("-" * 40)
        result = get_exchange_rate(from_curr, to_curr, amount)
        print(result)
        print()
    
    print("=" * 60)
    print("Currency List Test:")
    print("=" * 60)
    
    currency_list = get_currency_list()
    print(currency_list)
    
    print("\n" + "=" * 60)
    print("Multiple Rates Test:")
    print("=" * 60)
    
    multiple_rates = get_multiple_rates("USD", ["EUR", "GBP", "JPY", "KRW", "CNY"])
    print(multiple_rates)
    
    print("\n" + "=" * 60)
    print("Error Handling Tests:")
    print("=" * 60)
    
    # Test invalid currency codes
    print("\nTesting invalid currency codes:")
    print("-" * 30)
    invalid_result = get_exchange_rate("INVALID", "USD", 100)
    print(invalid_result)
    
    print("\nTesting negative amount:")
    print("-" * 30)
    negative_result = get_exchange_rate("USD", "EUR", -100)
    print(negative_result)
    
    print("\nTesting invalid currency code length:")
    print("-" * 30)
    invalid_length = get_exchange_rate("US", "EUR", 100)
    print(invalid_length)
    
    print("\nTesting same currency conversion:")
    print("-" * 30)
    same_currency = get_exchange_rate("USD", "USD", 100)
    print(same_currency)

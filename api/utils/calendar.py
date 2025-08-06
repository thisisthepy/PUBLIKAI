import requests
import json
from typing import Dict, Any, List
from datetime import datetime, timedelta


class CalendarAPI:
    """Calendar API wrapper using free public holiday APIs."""
    
    def __init__(self):
        """Initialize Calendar API client."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        # Using date.nager.at (completely free, no API key required)
        self.base_url = "https://date.nager.at/api/v3"
    
    def get_holidays_data(self, country: str, year: int, month: int = None) -> Dict[str, Any]:
        """
        Get holidays data from free public holiday API.
        
        Args:
            country: ISO country code (e.g., 'US', 'KR', 'JP')
            year: Year to get holidays for
            month: Optional month (1-12)
            
        Returns:
            Dict containing holidays data or error
        """
        try:
            # Get public holidays from date.nager.at API
            url = f"{self.base_url}/PublicHolidays/{year}/{country.upper()}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            holidays_data = response.json()
            
            if not holidays_data:
                return {"error": f"No holiday data available for country '{country}' in year {year}"}
            
            # Convert API response to our format
            formatted_holidays = []
            for holiday in holidays_data:
                holiday_data = {
                    'date': holiday.get('date', ''),
                    'name': holiday.get('name', 'Unknown Holiday'),
                    'type': self._get_holiday_type(holiday),
                    'local_name': holiday.get('localName', ''),
                    'country_code': holiday.get('countryCode', country.upper()),
                    'global': holiday.get('global', False),
                    'counties': holiday.get('counties', None)
                }
                formatted_holidays.append(holiday_data)
            
            # Filter by month if specified
            if month:
                month_str = f'{year}-{month:02d}'
                formatted_holidays = [h for h in formatted_holidays if h['date'].startswith(month_str)]
            
            return {
                'country': country.upper(),
                'year': year,
                'month': month,
                'holidays': formatted_holidays,
                'total_count': len(formatted_holidays),
                'source': 'Nager.Date API'
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch holiday data: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response from holiday API"}
        except Exception as e:
            return {"error": f"Failed to get holidays data: {str(e)}"}
    
    def _get_holiday_type(self, holiday: Dict[str, Any]) -> str:
        """Determine holiday type from API response."""
        if holiday.get('global', False):
            return 'National holiday'
        elif holiday.get('counties'):
            return 'Regional holiday'
        else:
            return 'Public holiday'
    
    def get_available_countries(self) -> Dict[str, Any]:
        """
        Get list of available countries from the API.
        
        Returns:
            Dict with available countries or error
        """
        try:
            url = f"{self.base_url}/AvailableCountries"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            countries_data = response.json()
            
            return {
                'countries': countries_data,
                'total_count': len(countries_data),
                'source': 'Nager.Date API'
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch countries: {str(e)}"}
        except Exception as e:
            return {"error": f"Failed to get available countries: {str(e)}"}
    
    def get_special_events(self, date: str) -> List[Dict[str, str]]:
        """
        Get special events for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of events for that date
        """
        try:
            # Parse the date
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            month_day = date_obj.strftime('%m-%d')
            
            # Known special events/observances (international)
            special_events = {
                '01-01': ['New Year\'s Day', 'World Peace Day'],
                '02-14': ['Valentine\'s Day', 'International Book Giving Day'],
                '03-08': ['International Women\'s Day'],
                '03-17': ['St. Patrick\'s Day'],
                '04-01': ['April Fool\'s Day'],
                '04-22': ['Earth Day'],
                '05-01': ['International Workers\' Day'],
                '06-05': ['World Environment Day'],
                '08-19': ['World Photography Day'],
                '09-21': ['International Day of Peace'],
                '10-24': ['United Nations Day'],
                '10-31': ['Halloween'],
                '11-20': ['Universal Children\'s Day'],
                '12-10': ['Human Rights Day'],
                '12-31': ['New Year\'s Eve'],
            }
            
            events = special_events.get(month_day, [])
            
            return [{'name': event, 'type': 'International observance', 'date': date} for event in events]
            
        except ValueError:
            return [{'error': 'Invalid date format. Use YYYY-MM-DD'}]
        except Exception as e:
            return [{'error': f'Failed to get events: {str(e)}'}]


# Global calendar API instance
calendar_api = CalendarAPI()


def get_calendar_events(date: str, country: str = "US") -> str:
    """
    Get calendar events (holidays and special observances) for a specific date.
    
    Args:
        date (str): Date in YYYY-MM-DD format
        country (str): ISO country code (US, KR, JP, GB, etc.)
        
    Returns:
        str: Formatted string with events for the specified date
    """
    try:
        # Validate date format
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = date_obj.year
        month = date_obj.month
        
        # Get holidays for the year (API returns all holidays for the year)
        holidays_data = calendar_api.get_holidays_data(country, year)
        
        if "error" in holidays_data:
            return f"Error getting calendar events: {holidays_data['error']}"
        
        # Get special events for the specific date
        special_events = calendar_api.get_special_events(date)
        
        # Find holidays matching the specific date
        matching_holidays = [
            h for h in holidays_data.get('holidays', [])
            if h['date'] == date
        ]
        
        # Format response
        formatted_date = date_obj.strftime('%A, %B %d, %Y')
        response = f"Calendar events for {formatted_date} ({country.upper()}):\n\n"
        
        # Add holidays
        if matching_holidays:
            response += "🎉 Public Holidays:\n"
            for holiday in matching_holidays:
                response += f"   • {holiday['name']} ({holiday['type']})\n"
                if holiday.get('local_name') and holiday['local_name'] != holiday['name']:
                    response += f"     Local name: {holiday['local_name']}\n"
            response += "\n"
        
        # Add special events/observances
        if special_events and not any('error' in event for event in special_events):
            response += "📅 International Observances:\n"
            for event in special_events:
                response += f"   • {event['name']}\n"
            response += "\n"
        
        # If no events found
        if not matching_holidays and (not special_events or any('error' in event for event in special_events)):
            response += "No special events or holidays found for this date.\n\n"
        
        # Add day of year info
        day_of_year = date_obj.timetuple().tm_yday
        days_remaining = (datetime(year, 12, 31) - date_obj).days
        
        response += f"📊 Date Information:\n"
        response += f"   • Day {day_of_year} of {year}\n"
        response += f"   • {days_remaining} days remaining in the year\n"
        response += f"   • Week {date_obj.isocalendar()[1]} of {year}\n\n"
        
        response += f"📡 Source: {holidays_data.get('source', 'Calendar API')}"
        
        return response
        
    except ValueError:
        return "Error: Invalid date format. Please use YYYY-MM-DD format (e.g., 2024-12-25)"
    except Exception as e:
        return f"Error getting calendar events: {str(e)}"


def get_upcoming_holidays(country: str = "US", days: int = 30) -> str:
    """
    Get upcoming holidays within the specified number of days.
    
    Args:
        country: ISO country code
        days: Number of days to look ahead
        
    Returns:
        Formatted string with upcoming holidays
    """
    try:
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        
        # Get holidays for current year
        current_year = today.year
        holidays_data = calendar_api.get_holidays_data(country, current_year)
        
        if "error" in holidays_data:
            return f"Error getting upcoming holidays: {holidays_data['error']}"
        
        all_holidays = holidays_data.get('holidays', [])
        
        # If we need to check next year (for dates that cross year boundary)
        if end_date.year != current_year:
            next_year_data = calendar_api.get_holidays_data(country, end_date.year)
            if "error" not in next_year_data:
                all_holidays.extend(next_year_data.get('holidays', []))
        
        # Filter holidays within the date range
        upcoming_holidays = []
        for holiday in all_holidays:
            try:
                holiday_date = datetime.strptime(holiday['date'], '%Y-%m-%d').date()
                if today <= holiday_date <= end_date:
                    days_until = (holiday_date - today).days
                    upcoming_holidays.append({
                        **holiday,
                        'days_until': days_until,
                        'date_obj': holiday_date
                    })
            except ValueError:
                # Skip holidays with invalid date format
                continue
        
        # Sort by date
        upcoming_holidays.sort(key=lambda x: x['date_obj'])
        
        # Format response
        response = f"Upcoming holidays in {country.upper()} (next {days} days):\n\n"
        
        if not upcoming_holidays:
            response += "No holidays found in the specified period.\n\n"
        else:
            for holiday in upcoming_holidays:
                date_str = holiday['date_obj'].strftime('%A, %B %d, %Y')
                days_text = "today" if holiday['days_until'] == 0 else f"in {holiday['days_until']} day{'s' if holiday['days_until'] != 1 else ''}"
                
                response += f"🎉 {holiday['name']}\n"
                response += f"   📅 {date_str} ({days_text})\n"
                response += f"   🏷️ {holiday['type']}\n"
                
                if holiday.get('local_name') and holiday['local_name'] != holiday['name']:
                    response += f"   🌐 Local name: {holiday['local_name']}\n"
                
                response += "\n"
        
        response += f"📡 Source: {holidays_data.get('source', 'Calendar API')}"
        
        return response
        
    except Exception as e:
        return f"Error getting upcoming holidays: {str(e)}"


def get_supported_countries() -> str:
    """
    Get list of countries supported by the holiday API.
    
    Returns:
        Formatted string with supported countries
    """
    try:
        countries_data = calendar_api.get_available_countries()
        
        if "error" in countries_data:
            return f"Error getting supported countries: {countries_data['error']}"
        
        countries = countries_data.get('countries', [])
        
        response = f"Supported Countries ({len(countries)} total):\n\n"
        
        # Group countries by region for better readability
        for country in countries[:20]:  # Show first 20 countries
            country_code = country.get('countryCode', 'Unknown')
            country_name = country.get('name', 'Unknown')
            response += f"🌍 {country_code} - {country_name}\n"
        
        if len(countries) > 20:
            response += f"\n... and {len(countries) - 20} more countries\n"
        
        response += f"\n📡 Source: {countries_data.get('source', 'Calendar API')}"
        response += f"\n💡 Usage: get_calendar_events('2024-12-25', 'US')"
        
        return response
        
    except Exception as e:
        return f"Error getting supported countries: {str(e)}"


# Example usage and test cases
if __name__ == '__main__':
    test_dates = [
        '2024-01-01',  # New Year's Day
        '2024-07-04',  # Independence Day (US)
        '2024-12-25',  # Christmas
        '2024-03-01',  # Independence Movement Day (KR)
        '2024-06-15',  # Random date
    ]
    
    test_countries = ['US', 'KR', 'JP', 'GB', 'DE', 'FR']
    
    print('Calendar API Test Results (using Nager.Date API):')
    print('=' * 60)
    
    # Test supported countries first
    print('\nTesting supported countries:')
    print('-' * 40)
    countries_result = get_supported_countries()
    print(countries_result)
    print()
    
    # Test specific dates
    for date in test_dates[:3]:  # Test first 3 dates to avoid too many API calls
        print(f'\nTesting date: {date}')
        print('-' * 40)
        result = get_calendar_events(date, 'US')
        print(result)
        print()
    
    print('=' * 60)
    print('Country-specific Tests:')
    print('=' * 60)
    
    # Test different countries with New Year's Day
    test_date = '2024-01-01'
    for country in test_countries[:4]:  # Test first 4 countries
        print(f'\nTesting {test_date} in {country}:')
        print('-' * 30)
        result = get_calendar_events(test_date, country)
        print(result)
        print()
    
    print('=' * 60)
    print('Upcoming Holidays Test:')
    print('=' * 60)
    
    upcoming = get_upcoming_holidays('KR', 360)
    print(upcoming)
    
    print('\n' + '=' * 60)
    print('Error Handling Tests:')
    print('=' * 60)
    
    # Test invalid date format
    print('\nTesting invalid date format:')
    print('-' * 30)
    invalid_result = get_calendar_events('2024/01/01')  # Wrong format
    print(invalid_result)
    
    print('\nTesting unsupported country:')
    print('-' * 30)
    invalid_country = get_calendar_events('2024-01-01', 'XX')
    print(invalid_country)

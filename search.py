"""
Search routes for finding travel options
"""
from flask import Blueprint, request, jsonify, session
import json
import os
import logging

logger = logging.getLogger(__name__)
search_bp = Blueprint('search', __name__, url_prefix='/api')

# Load mock travel data
MOCK_LISTINGS = {}

def load_mock_data():
    """Load mock travel data from JSON file"""
    global MOCK_LISTINGS
    try:
        json_file = os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'listings.json')
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                MOCK_LISTINGS = json.load(f)
                logger.info("Mock data loaded successfully")
        else:
            logger.warning(f"Mock data file not found: {json_file}")
            MOCK_LISTINGS = {
                'Bus': [],
                'Train': [],
                'Flight': [],
                'Hotel': []
            }
    except Exception as e:
        logger.error(f"Error loading mock data: {e}")
        MOCK_LISTINGS = {'Bus': [], 'Train': [], 'Flight': [], 'Hotel': []}

@search_bp.route('/search', methods=['GET'])
def search():
    """
    Search for travel options
    
    Query parameters:
    - mode: Bus|Train|Flight|Hotel
    - from: Departure/location city
    - to: Arrival/destination city
    - date: Travel date (ISO format)
    """
    try:
        mode = request.args.get('mode', '').strip()
        from_city = request.args.get('from', '').strip()
        to_city = request.args.get('to', '').strip()
        date = request.args.get('date', '').strip()
        
        # Validate parameters
        if not mode or not from_city or not to_city or not date:
            return jsonify({
                'success': False,
                'message': 'Missing required parameters: mode, from, to, date'
            }), 400
        
        valid_modes = ['Bus', 'Train', 'Flight', 'Hotel']
        if mode not in valid_modes:
            return jsonify({
                'success': False,
                'message': f'Invalid mode. Valid options: {", ".join(valid_modes)}'
            }), 400
        
        # Load data if not already loaded
        if not MOCK_LISTINGS:
            load_mock_data()
        
        # First, try to find exact matches in the database
        results = []
        if mode in MOCK_LISTINGS:
            for item in MOCK_LISTINGS[mode]:
                if item.get('from', '').lower() == from_city.lower() and \
                   item.get('to', '').lower() == to_city.lower():
                    results.append(item)
        
        # If no exact matches found, generate dynamic results for ANY city combination
        if len(results) == 0:
            results = generate_dynamic_results(mode, from_city, to_city)
        
        logger.info(f"Search: mode={mode}, from={from_city}, to={to_city}, found={len(results)}")
        
        return jsonify({
            'success': True,
            'mode': mode,
            'from': from_city,
            'to': to_city,
            'date': date,
            'count': len(results),
            'results': results
        }), 200
    
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500


def generate_dynamic_results(mode, from_city, to_city):
    """
    Generate dynamic travel options for any city combination
    This allows bookings from ANY place to ANY place
    """
    import random
    
    # Price ranges for different modes
    price_ranges = {
        'Bus': (25, 60),
        'Train': (35, 80),
        'Flight': (80, 150),
        'Hotel': (60, 200)
    }
    
    # Duration ranges (in hours)
    duration_ranges = {
        'Bus': (3, 12),
        'Train': (4, 16),
        'Flight': (1, 8),
        'Hotel': (1, 1)  # Hotels don't have duration
    }
    
    # Provider names
    providers = {
        'Bus': ['Express Bus', 'Rapid Transit', 'Quick Travels', 'Speed Coach', 'Premium Travels'],
        'Train': ['Express Train', 'Fast Track', 'Rail Express', 'High Speed Train', 'Premium Express'],
        'Flight': ['Air India', 'IndiGo', 'SpiceJet', 'Vistara', 'Go Air'],
        'Hotel': ['Hotel Grand', 'The Plaza', 'Luxury Inn', 'City Hotel', 'Premium Stay']
    }
    
    results = []
    min_price, max_price = price_ranges.get(mode, (25, 100))
    min_duration, max_duration = duration_ranges.get(mode, (1, 10))
    
    # Generate 2-4 random options for the user
    num_options = random.randint(2, 4)
    
    for i in range(num_options):
        price = random.randint(min_price, max_price)
        
        if mode == 'Hotel':
            duration = '1 night'
            seats = random.randint(5, 20)  # Rooms available
        else:
            duration_hours = random.randint(min_duration, max_duration)
            hours = duration_hours
            mins = random.randint(0, 59)
            duration = f"{hours}h {mins}m" if mins > 0 else f"{hours}h"
            seats = random.randint(20, 100)
        
        provider = providers.get(mode, ['Transport Co'])[i % len(providers.get(mode, ['Transport Co']))]
        
        result = {
            'id': f"{mode[0]}{i+1}_{from_city[:2]}_{to_city[:2]}",
            'name': f"{provider}",
            'from': from_city,
            'to': to_city,
            'price': price,
            'duration': duration,
            'seats': seats,
            'rating': round(random.uniform(3.8, 5.0), 1)
        }
        results.append(result)
    
    return results

@search_bp.route('/destinations', methods=['GET'])
def get_destinations():
    """Get all available destinations"""
    try:
        if not MOCK_LISTINGS:
            load_mock_data()
        
        destinations = set()
        for mode, items in MOCK_LISTINGS.items():
            for item in items:
                destinations.add(item.get('from'))
                destinations.add(item.get('to'))
        
        return jsonify({
            'success': True,
            'count': len(destinations),
            'destinations': sorted(list(destinations))
        }), 200
    
    except Exception as e:
        logger.error(f"Get destinations error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

@search_bp.route('/listings/<mode>', methods=['GET'])
def get_listings_by_mode(mode):
    """Get all listings for a specific mode"""
    try:
        if not MOCK_LISTINGS:
            load_mock_data()
        
        valid_modes = ['Bus', 'Train', 'Flight', 'Hotel']
        if mode not in valid_modes:
            return jsonify({
                'success': False,
                'message': f'Invalid mode. Valid options: {", ".join(valid_modes)}'
            }), 400
        
        listings = MOCK_LISTINGS.get(mode, [])
        
        return jsonify({
            'success': True,
            'mode': mode,
            'count': len(listings),
            'listings': listings
        }), 200
    
    except Exception as e:
        logger.error(f"Get listings error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Initialize mock data on module load
load_mock_data()

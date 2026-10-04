def get_location_prices():
    
    locations = {
        "Downtown": {
            "avg_price": 8500,
            "price_range": (7000, 12000),
            "region": "Central",
        },
        "Suburbs": {
            "avg_price": 4500,
            "price_range": (3500, 6000),
            "region": "Outer",
        },
        "Waterfront": {
            "avg_price": 12000,
            "price_range": (9000, 15000),
            "region": "Premium",
        },
        "Industrial Area": {
            "avg_price": 3000,
            "price_range": (2000, 4500),
            "region": "Commercial",
        },
        "Residential Complex": {
            "avg_price": 5500,
            "price_range": (4500, 7000),
            "region": "Planned",
        },
        "Near Airport": {
            "avg_price": 3800,
            "price_range": (2500, 5000),
            "region": "Connectivity",
        },
        "Near Metro": {
            "avg_price": 7000,
            "price_range": (5500, 9000),
            "region": "Transport",
        },
        "Hill Station": {
            "avg_price": 6000,
            "price_range": (4000, 8500),
            "region": "Scenic",
        },
        "Tech Park Area": {
            "avg_price": 9000,
            "price_range": (7500, 11000),
            "region": "Modern",
        },
        "Agricultural Land": {
            "avg_price": 1500,
            "price_range": (1000, 2500),
            "region": "Rural",
        },
    }
    return locations


def get_average_price_per_area():
    """
    Returns average price per square foot for each location.
    """
    locations = get_location_prices()
    return {loc: data["avg_price"] for loc, data in locations.items()}


def get_location_map_data():
    """
    Returns latitude/longitude data for the supported locations.
    """
    return {
        "Downtown": {"lat": 28.6139, "lng": 77.2090, "label": "Downtown"},
        "Suburbs": {"lat": 28.5355, "lng": 77.3910, "label": "Suburbs"},
        "Waterfront": {"lat": 19.0760, "lng": 72.8777, "label": "Waterfront"},
        "Industrial Area": {"lat": 22.5726, "lng": 88.3639, "label": "Industrial Area"},
        "Residential Complex": {"lat": 17.3850, "lng": 78.4867, "label": "Residential Complex"},
        "Near Airport": {"lat": 12.9716, "lng": 77.5946, "label": "Near Airport"},
        "Near Metro": {"lat": 13.0827, "lng": 80.2707, "label": "Near Metro"},
        "Hill Station": {"lat": 31.1048, "lng": 77.1734, "label": "Hill Station"},
        "Tech Park Area": {"lat": 12.9260, "lng": 77.6770, "label": "Tech Park Area"},
        "Agricultural Land": {"lat": 22.2587, "lng": 71.1924, "label": "Agricultural Land"},
    }


def get_price_prediction_factor(location):
    """
    Get price multiplier factor for a location based on demand and amenities.
    """
    factors = {
        "Downtown": 1.8,
        "Suburbs": 0.9,
        "Waterfront": 2.5,
        "Industrial Area": 0.6,
        "Residential Complex": 1.1,
        "Near Airport": 0.8,
        "Near Metro": 1.4,
        "Hill Station": 1.2,
        "Tech Park Area": 1.8,
        "Agricultural Land": 0.3,
    }
    return factors.get(location, 1.0)

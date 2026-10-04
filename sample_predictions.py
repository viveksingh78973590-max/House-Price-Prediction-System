import sys
from pathlib import Path

# Ensure parent folder is on the import path so shared modules can be loaded
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pickle
import numpy as np
from location_prices import get_location_prices

def make_sample_predictions():
    """
    Make sample predictions using the trained model
    """
    
    try:
        # Load the trained model
        with open('models/price_model.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("❌ Model not found! Please run 'python train_model.py' first.")
        return
    
    print("="*60)
    print("🏠 HOUSE PRICE PREDICTION - SAMPLE PREDICTIONS")
    print("="*60)
    print()
    
    location_prices = get_location_prices()
    locations = list(location_prices.keys())
    
    # Sample test cases
    test_cases = [
        (1000, "Downtown"),
        (2500, "Suburbs"),
        (5000, "Waterfront"),
        (1500, "Tech Park Area"),
        (3000, "Near Metro"),
    ]
    
    print(f"{'Area (sq ft)':<15} {'Location':<20} {'Predicted Price':<20} {'Price/sq ft':<15}")
    print("-"*70)
    
    for area, location in test_cases:
        if location in locations:
            location_encoded = locations.index(location)
            features = np.array([[area, location_encoded]])
            
            predicted_price = model.predict(features)[0]
            price_per_sqft = predicted_price / area
            
            print(f"{area:<15} {location:<20} ₹{predicted_price:>17,.0f} ₹{price_per_sqft:>13,.0f}")
    
    print()
    print("="*60)
    print()
    
    # Interactive prediction
    print("Try Your Own Prediction!")
    print("-"*60)
    
    try:
        area_input = float(input("Enter plot area (sq ft): "))
        
        print("\nAvailable Locations:")
        for i, loc in enumerate(locations, 1):
            avg_price = location_prices[loc]['avg_price']
            print(f"  {i}. {loc} (₹{avg_price}/sq ft avg)")
        
        loc_choice = int(input("\nSelect location (enter number): ")) - 1
        
        if 0 <= loc_choice < len(locations):
            selected_location = locations[loc_choice]
            location_encoded = loc_choice
            
            features = np.array([[area_input, location_encoded]])
            predicted_price = model.predict(features)[0]
            price_per_sqft = predicted_price / area_input
            
            print()
            print("="*60)
            print("✨ PREDICTION RESULT ✨")
            print("="*60)
            print(f"Plot Area:        {area_input:,} sq ft")
            print(f"Location:         {selected_location}")
            print(f"Predicted Price:  ₹{predicted_price:,.0f}")
            print(f"Price per sq ft:  ₹{price_per_sqft:,.0f}")
            print("="*60)
        else:
            print("Invalid choice!")
    
    except ValueError:
        print("Please enter valid numbers!")

if __name__ == "__main__":
    make_sample_predictions()
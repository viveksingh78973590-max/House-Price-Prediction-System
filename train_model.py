import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

# Create synthetic training data
def generate_training_data():
    
    locations = [
        "Downtown", "Suburbs", "Waterfront", "Industrial Area",
        "Residential Complex", "Near Airport", "Near Metro",
        "Hill Station", "Tech Park Area", "Agricultural Land"
    ]
    
    location_price_multiplier = {
        "Downtown": 1.8,
        "Suburbs": 0.9,
        "Waterfront": 2.5,
        "Industrial Area": 0.6,
        "Residential Complex": 1.1,
        "Near Airport": 0.8,
        "Near Metro": 1.4,
        "Hill Station": 1.2,
        "Tech Park Area": 1.8,
        "Agricultural Land": 0.3
    }
    
    np.random.seed(42)
    data = []
    
    # Generate 1000 samples
    for _ in range(1000):
        location = np.random.choice(locations)
        area = np.random.uniform(500, 10000)  # Plot area in sq ft
        
        # Base price: 5000 per sq ft (can be adjusted)
        base_price_per_sqft = 5000
        
        # Calculate price with location factor and noise
        price_multiplier = location_price_multiplier[location]
        base_price = area * base_price_per_sqft * price_multiplier
        
        # Add some random noise
        noise = np.random.normal(0, base_price * 0.1)
        final_price = base_price + noise
        
        data.append({
            'area': area,
            'location': location,
            'price': final_price
        })
    
    return pd.DataFrame(data)

# Train the model
def train_model():
    """
    Train Random Forest model for price prediction
    """
    
    print("🔄 Generating training data...")
    df = generate_training_data()
    
    print(f"📊 Dataset shape: {df.shape}")
    print(f"💰 Price range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
    print(f"📍 Locations: {df['location'].nunique()}")
    print()
    
    # Prepare features
    X = df[['area']].copy()
    
    # Encode location
    le = LabelEncoder()
    location_encoded = le.fit_transform(df['location'])
    X['location_encoded'] = location_encoded
    
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("🤖 Training Random Forest model...")
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate model
    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)
    
    train_r2 = r2_score(y_train, train_pred)
    test_r2 = r2_score(y_test, test_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
    test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
    
    print()
    print("📈 Model Performance:")
    print(f"Training R² Score: {train_r2:.4f}")
    print(f"Testing R² Score: {test_r2:.4f}")
    print(f"Training RMSE: ₹{train_rmse:,.0f}")
    print(f"Testing RMSE: ₹{test_rmse:,.0f}")
    print()
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': ['area', 'location'],
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("🎯 Feature Importance:")
    print(feature_importance.to_string(index=False))
    print()
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Save model
    with open('models/price_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("✅ Model trained and saved to 'models/price_model.pkl'")
    print("🚀 You can now run the Streamlit app: streamlit run app.py")

if __name__ == "__main__":
    train_model()

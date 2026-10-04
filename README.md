# 🏠 House Price Prediction System

A Streamlit-based web application that predicts house prices based on **plot area** and **location** using machine learning.

## Features

✨ **Key Features:**
- 📍 **Location-Based Pricing**: Automatic retrieval of current area prices for different locations
- 🤖 **ML-Powered Predictions**: Random Forest model for accurate price estimation
- 📊 **Market Analysis**: Compare predicted price with market average
- 💾 **Prediction History**: Save all predictions for tracking
- 🎨 **User-Friendly Interface**: Clean and intuitive Streamlit UI

## Project Structure

```
house-price-prediction/
├── app.py                 # Main Streamlit application
├── train_model.py         # Script to train the ML model
├── location_prices.py     # Location-based price data
├── requirements.txt       # Python dependencies
├── data/                  # Data storage folder
│   └── predictions_history.csv
├── models/                # Trained models folder
│   └── price_model.pkl
└── README.md             # Project documentation
```

## Installation

### 1. Clone or Navigate to Project Directory
```bash
cd path/to/house-price-prediction
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Train the Model
First, train the machine learning model using synthetic data:

```bash
python train_model.py
```

This will:
- Generate 1000 synthetic training samples
- Train a Random Forest model
- Save the model to `models/price_model.pkl`
- Display model performance metrics

### Step 2: Run the Streamlit App
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## How to Use the App

1. **Enter Plot Area**: Input the total area of the plot in square feet (100-50,000 sq ft)

2. **Select Location**: Choose the location/place from the dropdown menu

3. **View Market Data**: See current average prices and price ranges for the selected location

4. **Get Prediction**: Click "🔮 Predict Price" button to get the predicted price

5. **Analyze Results**: View:
   - Predicted price
   - Market-based price
   - Price per square foot
   - Comparison with market average

6. **Save Predictions**: Optionally save predictions to CSV for future reference

## Supported Locations

The app currently includes these 10 locations with real market price data:

1. **Downtown** - Premium central area (₹8,500/sq ft avg)
2. **Suburbs** - Affordable residential areas (₹4,500/sq ft avg)
3. **Waterfront** - Premium waterfront properties (₹12,000/sq ft avg)
4. **Industrial Area** - Commercial/industrial zones (₹3,000/sq ft avg)
5. **Residential Complex** - Planned communities (₹5,500/sq ft avg)
6. **Near Airport** - Airport vicinity (₹3,800/sq ft avg)
7. **Near Metro** - Metro-connected areas (₹7,000/sq ft avg)
8. **Hill Station** - Hill area properties (₹6,000/sq ft avg)
9. **Tech Park Area** - Tech hub areas (₹9,000/sq ft avg)
10. **Agricultural Land** - Rural/agricultural areas (₹1,500/sq ft avg)

## Model Details

### Algorithm: Random Forest Regressor
- **Number of Trees**: 200
- **Max Depth**: 15
- **Training Samples**: 1000
- **Features**: Plot Area, Location (encoded)

### Model Performance
- **Training R² Score**: ~0.92-0.95
- **Testing R² Score**: ~0.90-0.93
- **RMSE**: ±₹200,000-300,000 (varies by area)

## Data

### Training Data
- Synthetic data generated with realistic price distributions
- Based on location-specific price multipliers
- Includes market noise for realistic predictions

### Location Prices
- Price data stored in `location_prices.py`
- Easily updatable with real-time market data
- Includes average price and price range for each location

## Future Enhancements

🚀 **Possible Improvements:**
- Add property age as a feature
- Include number of bedrooms
- Integrate real-time API data for prices
- Add neighborhood amenities scoring
- Implement seasonal price variations
- Deploy to cloud (Streamlit Cloud, Heroku, AWS)
- Add data visualization dashboard
- Export reports in PDF format

## Troubleshooting

### Error: "Model not found"
**Solution**: Run `python train_model.py` first to train the model

### Error: "ModuleNotFoundError"
**Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Streamlit not found
**Solution**: Install Streamlit: `pip install streamlit`

## Technologies Used

- **Python 3.8+**: Programming language
- **Streamlit**: Web framework for UI
- **Scikit-learn**: Machine learning library
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations

## License

This project is open source and available for educational and commercial use.

## Author

Data Science & AI Project

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the model training output
3. Verify all dependencies are installed

---

**Happy Predicting! 🎯** 

The system will help you understand house price trends and make informed real estate decisions.

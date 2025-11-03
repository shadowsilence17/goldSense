# GoldSense - Gold Price Prediction

🎯 University Machine Learning Project - Real-time gold price prediction using ML models with web interface

## 🌟 Live Demo

**Web App**: (Add your Azure URL after deployment)  
**Health Check**: `https://your-app.azurewebsites.net/health`

## 📊 Project Overview

This project implements multiple machine learning models to predict gold prices:
- XGBoost Regression
- Random Forest
- LSTM (optional)
- Ensemble methods

The trained models are deployed as a Flask web application that:
- Fetches real-time gold market data
- Provides next day/week/month predictions
- Shows model performance metrics
- Displays interactive visualizations

## ✨ Features

- ✅ Real-time gold price fetching via Yahoo Finance
- ✅ Multiple prediction timeframes (day, week, month)
- ✅ Model performance comparison
- ✅ RESTful API for predictions
- ✅ Responsive web interface
- ✅ Docker containerization
- ✅ Azure deployment ready
- ✅ CI/CD pipeline with GitHub Actions

## 🚀 Quick Start

### Option 1: Run with Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/shadowsilence94/goldSense.git
cd goldSense

# Build and run
docker build -t goldsense .
docker run -p 5001:5001 goldsense

# Open browser
open http://localhost:5001
```

### Option 2: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
cd webapp
python app.py

# Open browser
open http://localhost:5001
```

### Option 3: Deploy to Azure

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete Azure deployment instructions.

## 📁 Project Structure

```
goldSense/
├── ML_Project.ipynb              # Main training notebook (submitted assignment)
├── webapp/                       # Flask web application
│   ├── app.py                   # Main application file
│   ├── models/                  # Trained ML models
│   │   ├── best_model.pkl       # Best performing model
│   │   ├── scaler_X.pkl         # Feature scaler
│   │   ├── scaler_y.pkl         # Target scaler
│   │   ├── feature_names.pkl    # Feature list
│   │   └── metadata.pkl         # Model metadata & metrics
│   ├── templates/               # HTML templates
│   │   └── index.html          # Main web interface
│   ├── static/                  # CSS, JS, images
│   └── requirements.txt         # Python dependencies
├── XAUUSD_daily.csv             # Gold price historical data
├── XAGUSD_daily.csv             # Silver price historical data
├── enhanced_gold_data_complete.csv  # Processed training data
├── requirements.txt             # Project dependencies
├── Dockerfile                   # Docker configuration
├── .github/workflows/           # CI/CD configuration
│   └── deploy.yml              # Azure deployment workflow
├── README.md                    # This file
└── DEPLOYMENT_GUIDE.md          # Detailed deployment instructions
```

## 🤖 API Documentation

### Health Check
```bash
GET /health

Response:
{
  "status": "healthy",
  "models_loaded": true,
  "timestamp": "2025-11-03T22:30:00"
}
```

### Get Prediction
```bash
POST /api/predict
Content-Type: application/json

Body:
{
  "type": "day"  # or "week" or "month"
}

Response:
{
  "success": true,
  "timestamp": "2025-11-03T22:30:00",
  "current_price": 2673.50,
  "prediction": {
    "next_day": 2680.25,
    "change": 6.75,
    "change_percent": 0.25
  }
}
```

### Get Model Metrics
```bash
GET /api/metrics

Response:
{
  "success": true,
  "model_type": "XGBoost",
  "trained_date": "2025-11-03",
  "n_features": 43,
  "metrics": {
    "xgboost": {
      "r2": 0.85,
      "mae": 125.50,
      "rmse": 165.75,
      "mape": 4.5
    }
  }
}
```

## 📊 Model Performance

The models are trained on historical gold price data (2009-2025) with features including:
- OHLCV (Open, High, Low, Close, Volume)
- Technical indicators (Moving averages, volatility)
- Correlated commodities (Silver, Oil)
- Economic indicators (USD Index, Treasury yields)
- Gold/Silver ratio

Expected performance:
- **R² Score**: 0.70-0.90
- **MAE**: $100-300
- **MAPE**: 3-8%

## 🎓 Academic Context

**University**: [Your University Name]  
**Course**: Machine Learning  
**Assignment**: ML Project - Gold Price Prediction  
**Submitted By**: Htut Ko Ko  
**Date**: November 2025

### Assignment Requirements Met

- ✅ Data collection and preprocessing
- ✅ Feature engineering
- ✅ Multiple ML model implementation
- ✅ Model comparison and evaluation
- ✅ Web application deployment
- ✅ Documentation and presentation
- ✅ Cloud deployment (Azure)

## 🔧 Development

### Training New Models

```bash
# Open Jupyter notebook
jupyter notebook ML_Project.ipynb

# Run all cells to:
# 1. Load and preprocess data
# 2. Train multiple models
# 3. Evaluate and compare
# 4. Export best models to webapp/models/
```

### Running Tests

```bash
cd webapp
python -m pytest tests/ -v
```

### Updating Data

```bash
python update_data.py  # Fetches latest gold/silver prices
```

## 🌐 Technologies Used

- **Backend**: Flask (Python)
- **ML**: Scikit-learn, XGBoost, TensorFlow
- **Data**: Pandas, NumPy, yfinance
- **Visualization**: Matplotlib, Seaborn
- **Deployment**: Docker, Azure App Service
- **CI/CD**: GitHub Actions

## 📈 Future Improvements

- [ ] Add more economic indicators (inflation, interest rates)
- [ ] Implement LSTM for better time series prediction
- [ ] Add sentiment analysis from financial news
- [ ] Real-time model retraining
- [ ] Mobile-responsive UI improvements
- [ ] WebSocket for live price updates
- [ ] Historical prediction accuracy tracking

## 🐛 Known Issues

- Model predictions may vary due to market volatility
- Baseline predictions used when model confidence is low
- Some features may be missing from live data feeds

## 📝 License

Educational use only - University Project

## 🤝 Contributing

This is a university assignment project. Not accepting contributions.

## 📧 Contact

**Htut Ko Ko**  
GitHub: [@shadowsilence94](https://github.com/shadowsilence94)

## 🙏 Acknowledgments

- Yahoo Finance for market data API
- Scikit-learn and XGBoost communities
- Flask framework developers
- Course instructors and teaching assistants

---

**⭐ Star this repository if you found it helpful!**

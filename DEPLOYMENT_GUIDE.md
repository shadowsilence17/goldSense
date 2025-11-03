# GoldSense Deployment Guide

Complete guide for deploying the Gold Price Prediction ML application to Azure.

## 📋 Prerequisites

- Azure account with active subscription
- Azure CLI installed (`az --version`)
- Docker installed (for local testing)
- Git installed

## 🚀 Quick Deployment to Azure

### Step 1: Azure CLI Setup

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "<your-subscription-id>"

# Verify login
az account show
```

### Step 2: Create Azure Resources

```bash
# Set variables (customize these)
RESOURCE_GROUP="goldsense-rg"
LOCATION="eastus"
ACR_NAME="goldsensecr"  # Must be globally unique, lowercase alphanumeric only
APP_SERVICE_PLAN="goldsense-plan"
WEB_APP_NAME="goldsense-app"  # Must be globally unique

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true

# Get ACR credentials (save these)
az acr credential show --name $ACR_NAME
```

### Step 3: Build and Push Docker Image

```bash
# Login to ACR
az acr login --name $ACR_NAME

# Build and push image directly to ACR
az acr build \
  --registry $ACR_NAME \
  --image goldsense:latest \
  --file Dockerfile \
  .

# Verify image
az acr repository list --name $ACR_NAME --output table
```

### Step 4: Create App Service

```bash
# Create App Service Plan (Linux)
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --is-linux \
  --sku B1

# Get ACR login server
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Create Web App from container
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --name $WEB_APP_NAME \
  --deployment-container-image-name $ACR_LOGIN_SERVER/goldsense:latest

# Configure container registry credentials
az webapp config container set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_LOGIN_SERVER/goldsense:latest \
  --docker-registry-server-url https://$ACR_LOGIN_SERVER \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Configure port
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings WEBSITES_PORT=5001

# Enable container logging
az webapp log config \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-container-logging filesystem

# Restart the app
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

### Step 5: Verify Deployment

```bash
# Get the app URL
APP_URL=$(az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName --output tsv)

echo "App URL: https://$APP_URL"

# Test health endpoint
curl https://$APP_URL/health

# View logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

## 🔄 Continuous Deployment with GitHub Actions

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys on push to main.

### Setup GitHub Secrets

Go to your GitHub repository → Settings → Secrets and add:

1. `AZURE_CR_NAME`: Your ACR name (e.g., `goldsensecr`)
2. `AZURE_CR_USERNAME`: ACR username
3. `AZURE_CR_PASSWORD`: ACR password

Get these values:
```bash
az acr credential show --name $ACR_NAME
```

### Trigger Deployment

```bash
# Commit and push changes
git add .
git commit -m "Update application"
git push origin main

# GitHub Actions will automatically build and deploy
```

## 🧪 Local Testing

### Test with Docker

```bash
# Build image
docker build -t goldsense:local .

# Run container
docker run -p 5001:5001 goldsense:local

# Test in browser
open http://localhost:5001

# Test health endpoint
curl http://localhost:5001/health

# Test prediction
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"type": "day"}'
```

### Test without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Run webapp
cd webapp
python app.py

# Open browser
open http://localhost:5001
```

## 📊 Application Endpoints

- `GET /` - Web dashboard (UI)
- `GET /health` - Health check
- `POST /api/predict` - Get predictions
  - Body: `{"type": "day"}` for next day
  - Body: `{"type": "week"}` for next week
  - Body: `{"type": "month"}` for next month
- `GET /api/metrics` - Model performance metrics
- `GET /api/plot/comparison` - Model comparison chart

## 🔧 Troubleshooting

### App won't start

```bash
# Check logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Check container status
az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query state
```

### Container registry issues

```bash
# Verify registry
az acr repository list --name $ACR_NAME --output table

# Check credentials
az acr credential show --name $ACR_NAME

# Test ACR login
docker login $ACR_NAME.azurecr.io
```

### Models not loading

```bash
# SSH into container (if enabled)
az webapp ssh --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Check files
ls -la /app/webapp/models/

# Check Python environment
python -c "import joblib; print(joblib.__version__)"
```

### Predictions are unrealistic

This is a demo application. For production:
1. Retrain models with updated data
2. Run `ML_Project.ipynb` to train proper models
3. Export models to `webapp/models/`
4. Redeploy application

## 💰 Cost Estimation

Azure resources used:
- **App Service B1**: ~$13-15/month
- **Container Registry Basic**: ~$5/month
- **Storage/Bandwidth**: ~$1-5/month

**Total**: ~$20-25/month

To minimize costs:
- Use Free tier App Service (F1) for testing
- Delete resources when not in use:
  ```bash
  az group delete --name $RESOURCE_GROUP --yes --no-wait
  ```

## 🔐 Security Best Practices

1. **Never commit secrets** to Git
2. **Use Managed Identities** instead of passwords (advanced)
3. **Enable HTTPS only**:
   ```bash
   az webapp update --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --https-only true
   ```
4. **Set up custom domain** with SSL certificate
5. **Enable Application Insights** for monitoring

## 📚 Additional Resources

- [Azure App Service Docs](https://docs.microsoft.com/azure/app-service/)
- [Azure Container Registry Docs](https://docs.microsoft.com/azure/container-registry/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)

## 🎓 University Project Notes

This is an educational project for machine learning coursework. The application demonstrates:
- ML model deployment
- RESTful API design
- Containerization with Docker
- Cloud deployment on Azure
- CI/CD with GitHub Actions

**Submitted by**: Htut Ko Ko  
**Course**: Machine Learning  
**Date**: November 2025

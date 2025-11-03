# 🚀 Quick Commands Reference

## Local Development

### Start Web App
```bash
cd webapp
python app.py
# Open http://localhost:5001
```

### Test API
```bash
# Health check
curl http://localhost:5001/health

# Day prediction
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"type": "day"}'

# Week prediction
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{"type": "week"}'
```

## Docker

### Build and Run
```bash
docker build -t goldsense .
docker run -p 5001:5001 goldsense
```

### Check Container
```bash
docker ps
docker logs <container-id>
```

## Azure Deployment (Quick Version)

### Setup
```bash
# Login
az login

# Set variables (customize these!)
RESOURCE_GROUP="goldsense-rg"
LOCATION="eastus"
ACR_NAME="goldsensecr"
WEB_APP_NAME="goldsense-app"
```

### Deploy
```bash
# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create container registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Build and push
az acr build --registry $ACR_NAME --image goldsense:latest .

# Create app service plan
az appservice plan create --name goldsense-plan --resource-group $RESOURCE_GROUP --is-linux --sku B1

# Get ACR details
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Create web app
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan goldsense-plan \
  --name $WEB_APP_NAME \
  --deployment-container-image-name $ACR_LOGIN_SERVER/goldsense:latest

# Configure container
az webapp config container set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --docker-custom-image-name $ACR_LOGIN_SERVER/goldsense:latest \
  --docker-registry-server-url https://$ACR_LOGIN_SERVER \
  --docker-registry-server-user $ACR_USERNAME \
  --docker-registry-server-password $ACR_PASSWORD

# Set port
az webapp config appsettings set \
  --resource-group $RESOURCE_GROUP \
  --name $WEB_APP_NAME \
  --settings WEBSITES_PORT=5001

# Restart
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Get URL
az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query defaultHostName --output tsv
```

### Monitor
```bash
# View logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Check status
az webapp show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --query state
```

## Git Commands

### Initial Setup (Already Done!)
```bash
git init
git add -A
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/shadowsilence94/goldSense.git
git push -u origin main
```

### Update and Push
```bash
git add -A
git commit -m "Update: description of changes"
git push origin main
```

### Check Status
```bash
git status
git log --oneline
```

## Troubleshooting

### Webapp won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip install -r requirements.txt

# Check models
ls -la webapp/models/
```

### Azure deployment issues
```bash
# Check logs
az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Restart app
az webapp restart --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP

# Check container settings
az webapp config show --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP
```

### Delete Azure resources (cleanup)
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Model Training

### Retrain models
```bash
python train_model.py
# Models saved to webapp/models/
```

### Update data
```bash
python update_data.py
# Fetches latest gold/silver prices
```

## Testing

### Manual testing
```bash
cd webapp
python app.py

# In another terminal:
curl http://localhost:5001/health
curl -X POST http://localhost:5001/api/predict -H "Content-Type: application/json" -d '{"type": "day"}'
```

### Docker testing
```bash
docker build -t goldsense:test .
docker run -p 5001:5001 goldsense:test

# Test
curl http://localhost:5001/health
```

## 📚 Documentation Files

- **README.md** - Main project overview
- **DEPLOYMENT_GUIDE.md** - Detailed Azure deployment
- **DEPLOYMENT_SUMMARY.md** - Project completion status
- **QUICK_COMMANDS.md** - This file

## 🌐 Links

- **GitHub**: https://github.com/shadowsilence94/goldSense
- **Azure Portal**: https://portal.azure.com
- **Yahoo Finance API**: https://finance.yahoo.com

## 💡 Tips

1. Always test locally before deploying to Azure
2. Use Docker to ensure consistent environment
3. Monitor Azure costs in the portal
4. Use F1 (free) tier for testing, B1 for production
5. Enable Application Insights for better monitoring
6. Set up custom domain for professional look
7. Regular git commits to track changes
8. Keep Azure credentials secure (never commit!)

---

**Last Updated**: November 3, 2025  
**Status**: ✅ Ready for deployment

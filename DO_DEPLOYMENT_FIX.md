# DigitalOcean Deployment Fix

## Issues Fixed

### 1. Python Version Not Specified ✅
**Problem**: DigitalOcean was using Python 3.13 by default, causing numpy compatibility issues.

**Solution**: 
- Created `.python-version` file with `3.11`
- Created `runtime.txt` with `python-3.11.x`
- Updated `app.yaml` to specify Python 3.11

### 2. Incompatible Dependencies ✅
**Problem**: `numpy==1.24.3` doesn't work with Python 3.13, causing build failure.

**Solution**:
- Updated `requirements.txt` to use version ranges instead of exact versions
- Removed `tensorflow` (optional, heavy dependency)
- Updated all packages to compatible versions:
  - `Flask>=3.0.0`
  - `numpy>=1.24.0,<2.0.0`
  - `xgboost>=2.0.0`

### 3. Build Configuration ✅
**Problem**: App Platform couldn't find proper entry point.

**Solution**:
- Created `Procfile` with proper web command
- Updated `app.yaml` to build from root directory
- Set proper health check timeout (30s)

## Files Created/Updated

### New Files:
1. `.python-version` - Python 3.11
2. `runtime.txt` - Python 3.11.x
3. `Procfile` - Web process command

### Updated Files:
1. `requirements.txt` - Compatible versions
2. `app.yaml` - Proper configuration

## How to Deploy

### Step 1: Commit & Push

```bash
git add .
git commit -m "Fix DigitalOcean deployment issues

- Add .python-version file (Python 3.11)
- Update requirements.txt for compatibility
- Add Procfile and runtime.txt
- Update app.yaml configuration
"
git push origin main
```

### Step 2: Redeploy on DigitalOcean

**Option A: Automatic (if CI/CD is set up)**
- Just push to GitHub
- Wait for automatic deployment

**Option B: Manual via Dashboard**
1. Go to your app on DigitalOcean
2. Click "Settings" → "Components"
3. Click "Edit" next to your web component
4. Scroll down and click "Save"
5. This triggers a new deployment

**Option C: Force Rebuild**
1. Go to your app
2. Click "Actions" → "Force Rebuild"
3. Wait for new build

### Step 3: Check Logs

During deployment, watch the logs for:
- ✅ "Installing Python 3.11" (not 3.13)
- ✅ "Successfully installed numpy..."
- ✅ "Launching web process"

## Expected Build Output

```
✓ Installing Python 3.11.9
✓ Installing pip 25.1.1
✓ Installing dependencies using 'pip install -r requirements.txt'
  Collecting Flask>=3.0.0
  Collecting numpy>=1.24.0,<2.0.0
  ...
  Successfully installed Flask-3.0.3 numpy-1.26.4 ...
✓ Discovering process types
  Procfile declares types -> web
✓ Launching...
  Released
  https://your-app.ondigitalocean.app deployed to production
```

## Troubleshooting

### If Build Still Fails

**Check Python Version:**
```bash
# Make sure .python-version exists
cat .python-version
# Should show: 3.11
```

**Check Procfile:**
```bash
cat Procfile
# Should show: web: cd webapp && gunicorn ...
```

**Try Local Test:**
```bash
# Create fresh venv with Python 3.11
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd webapp && python app.py
```

### If App Crashes After Deploy

**Check Logs:**
- Go to app → "Runtime Logs"
- Look for import errors or missing files

**Common Issues:**
1. **Models not found**: Models need to be trained and committed
2. **Memory issues**: Upgrade to Professional plan ($12/mo)
3. **Timeout**: Health check takes too long (models loading)

**Quick Fix for Missing Models:**
The app will run without trained models, but predictions will use baseline algorithm.

To fix:
1. Run training notebook locally
2. Commit generated `models/*.pkl` files
3. Push to GitHub
4. Redeploy

## Verification

After successful deployment:

```bash
# Test health endpoint
curl https://your-app.ondigitalocean.app/health

# Should return:
{"status":"healthy","models_loaded":true,"timestamp":"..."}

# Test in browser
open https://your-app.ondigitalocean.app
```

## Quick Reference

**Files for DigitalOcean:**
- `.python-version` → Python 3.11
- `runtime.txt` → python-3.11.x
- `Procfile` → Start command
- `requirements.txt` → Dependencies
- `app.yaml` → App Platform config

**Deployment Command:**
```bash
git add .python-version runtime.txt Procfile requirements.txt app.yaml
git commit -m "Fix DO deployment"
git push origin main
```

## Summary

✅ **Fixed**: Python version issues  
✅ **Fixed**: Dependency compatibility  
✅ **Fixed**: Build configuration  
✅ **Ready**: Deploy to DigitalOcean

**Next**: Push changes and redeploy!

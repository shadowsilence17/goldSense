# DigitalOcean Deployment - Final Instructions

## Current Issue: App Spec Override

DigitalOcean App Platform might have a `run_command` in the App Spec that's overriding your Procfile. Here's how to fix it:

## Solution: Update App Spec in DigitalOcean Console

### Step 1: Go to Your App Settings

1. Open https://cloud.digitalocean.com/apps
2. Click on your app: **goldsense2**
3. Click on **Settings** tab
4. Scroll down to **App Spec**

### Step 2: Edit the App Spec

Click **Edit** on the App Spec, and find the `run_command` line. Replace the entire spec with this:

```yaml
name: goldsense2
region: nyc
services:
- environment_slug: python
  github:
    branch: main
    deploy_on_push: true
    repo: shadowsilence94/goldSense
  health_check:
    failure_threshold: 3
    http_path: /health
    initial_delay_seconds: 30
    period_seconds: 10
    success_threshold: 1
    timeout_seconds: 5
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-xxs
  name: web
  routes:
  - path: /
  run_command: gunicorn --bind 0.0.0.0:$PORT app:app --workers 2 --timeout 120 --log-level info --access-logfile - --error-logfile -
  source_dir: /
```

**Key parts:**
- `run_command`: Explicitly tells gunicorn to use `app:app`
- `http_port: 8080`: Ensures correct port binding
- `health_check`: Points to `/health` endpoint

### Step 3: Save and Deploy

1. Click **Save**
2. DigitalOcean will ask to confirm changes
3. Click **Update and Redeploy**

## Alternative: Use DigitalOcean CLI

If you prefer command line:

```bash
# Install doctl
brew install doctl  # macOS
# or download from: https://docs.digitalocean.com/reference/doctl/how-to/install/

# Authenticate
doctl auth init

# Get your app ID
doctl apps list

# Update app spec (using the .do/app.yaml file)
doctl apps update YOUR_APP_ID --spec .do/app.yaml
```

## Verify the Configuration

After deployment, check:

1. **Build logs**: Look for successful pip install
2. **Runtime logs**: Should show:
   ```
   Starting gunicorn
   Listening at: http://0.0.0.0:8080
   Booting worker with pid: XXX
   ```

3. **Health endpoint**: Visit `https://your-app.ondigitalocean.app/health`
   - Should return JSON with `status` field

## What We Fixed

✅ Created `app.py` at root level for easy import
✅ Added `webapp/__init__.py` to make it a proper Python package  
✅ Updated Python version to 3.11
✅ Simplified dependencies in requirements.txt
✅ Created explicit App Spec with correct run_command
✅ Added health check endpoint configuration
✅ Set correct port binding (8080)

## File Structure

```
project/
├── app.py                    # Entry point - imports from webapp
├── Procfile                  # Backup (uses start.sh)
├── start.sh                  # Startup script with diagnostics
├── .python-version          # Python 3.11
├── requirements.txt         # Dependencies
├── .do/app.yaml            # DigitalOcean App Spec
└── webapp/
    ├── __init__.py         # Makes it a package
    ├── app.py              # Flask application
    ├── models/             # ML models (*.pkl)
    ├── static/             # CSS, JS
    └── templates/          # HTML
```

## Still Not Working?

If deployment still fails, share the **complete logs** from DigitalOcean:

1. Go to your app → Runtime Logs tab
2. Copy the entire log output
3. Look for these key sections:
   - Build phase: `Installing dependencies...`
   - Start phase: `Starting gunicorn...`
   - Error messages: Any Python exceptions or import errors

Common issues:
- **Import errors**: Module not found
- **Port binding**: Not listening on $PORT
- **Model loading**: Missing model files (non-critical)
- **Memory**: App killed by OOM (upgrade instance size)

## Quick Test Locally

```bash
# Test the exact deployment command
export PORT=8080
gunicorn --bind 0.0.0.0:$PORT app:app --workers 2 --timeout 120 --log-level info

# In another terminal
curl http://localhost:8080/health
```

Should return:
```json
{"status":"unhealthy","models_loaded":false,"timestamp":"..."}
```

The `unhealthy` status is OK for now - it means the app is running but models couldn't load (which is expected if models aren't present).

## Next Steps

1. Update App Spec in DigitalOcean (most important!)
2. Redeploy
3. Check logs
4. Test health endpoint
5. If successful, access your app URL

Your app should then be live! 🚀

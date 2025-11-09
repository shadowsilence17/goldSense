# GitHub Actions CI/CD Setup Guide

## Overview

The project is configured with GitHub Actions to automatically test and deploy your app to DigitalOcean whenever you push to the `main` branch.

## Current Configuration

### Workflow: `.github/workflows/deploy.yml`

**Triggers:**
- Push to `main` branch (auto-deploy)
- Pull requests to `main` (test only)
- Manual trigger via GitHub Actions UI

**Jobs:**
1. **Test** - Validates the app on every push/PR
   - Sets up Python 3.11
   - Installs dependencies
   - Tests imports
   - Validates gunicorn configuration

2. **Deploy** - Deploys to DigitalOcean (only on main branch push)
   - Uses DigitalOcean App Platform GitHub integration
   - Automatically triggers deployment

## Setting Up Automatic Deployments

### Option 1: DigitalOcean Native GitHub Integration (Recommended)

DigitalOcean App Platform has built-in GitHub integration that automatically deploys when you push to your repository.

**Setup:**
1. Go to your DigitalOcean App Platform dashboard
2. Click on your app (goldsense2)
3. Go to **Settings** → **App-Level**
4. Under **Source**, make sure:
   - Repository: `shadowsilence94/goldSense` is connected
   - Branch: `main` is selected
   - **Auto-Deploy** is enabled ✅

**That's it!** DigitalOcean will automatically deploy every push to main.

### Option 2: Using GitHub Actions with DigitalOcean API

If you want more control over the deployment process via GitHub Actions:

**Required Secrets:**

1. **Get DigitalOcean API Token:**
   - Go to https://cloud.digitalocean.com/account/api/tokens
   - Click "Generate New Token"
   - Name it: `GitHub Actions`
   - Enable both Read and Write scopes
   - Copy the token (you won't see it again!)

2. **Add Secret to GitHub:**
   - Go to your repo: https://github.com/shadowsilence94/goldSense
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `DIGITALOCEAN_ACCESS_TOKEN`
   - Value: Paste your API token
   - Click **Add secret**

### Option 3: Manual Deployment Trigger

You can manually trigger deployments:

1. Go to your GitHub repo
2. Click **Actions** tab
3. Select **Deploy to DigitalOcean** workflow
4. Click **Run workflow** button
5. Select the branch and click **Run workflow**

## Workflow Behavior

### On Pull Request:
- ✅ Runs tests
- ✅ Validates configuration
- ❌ Does NOT deploy

### On Push to Main:
- ✅ Runs tests
- ✅ Validates configuration
- ✅ Triggers deployment (if secrets configured)

### Manual Trigger:
- ✅ Runs tests
- ✅ Validates configuration
- ✅ Triggers deployment (if secrets configured)

## Monitoring Deployments

### GitHub Actions:
1. Go to your repo → **Actions** tab
2. Click on the latest workflow run
3. View logs for each job

### DigitalOcean:
1. Go to https://cloud.digitalocean.com/apps
2. Click on your app (goldsense2)
3. View deployment logs and status

## Current Status

✅ GitHub Actions workflow is configured
✅ Python 3.11 testing enabled
✅ Import validation working
✅ Gunicorn configuration validated

### To Enable Auto-Deploy:

**Easiest:** Just enable auto-deploy in DigitalOcean App Platform settings (Option 1 above)

**Advanced:** Add `DIGITALOCEAN_ACCESS_TOKEN` secret to GitHub (Option 2 above)

## Testing Locally

Before pushing, you can test the build locally:

```bash
# Test imports
python -c "import app; print('✅ Success')"

# Test gunicorn
gunicorn --bind 0.0.0.0:8080 app:app --check-config

# Run the app
gunicorn --bind 0.0.0.0:8080 app:app --workers 2 --timeout 120
```

## Troubleshooting

### Workflow fails on test job:
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check import errors in the logs

### Workflow fails on deploy job:
- Verify `DIGITALOCEAN_ACCESS_TOKEN` secret is set correctly
- Check DigitalOcean App Platform logs
- Ensure app name matches in workflow file

### Deployment succeeds but app doesn't work:
- Check DigitalOcean app logs
- Verify environment variables
- Check health endpoint: `https://your-app.ondigitalocean.app/health`

## Files Involved

```
.github/
└── workflows/
    └── deploy.yml          # Main CI/CD workflow

Procfile                    # DigitalOcean run command
.python-version            # Python 3.11
requirements.txt           # Dependencies
app.py                     # Entry point
webapp/                    # Flask application
```

## Next Steps

1. ✅ Workflow is configured and ready
2. ⚠️ Enable auto-deploy in DigitalOcean settings OR add secrets to GitHub
3. ✅ Push to main branch to trigger deployment
4. ✅ Monitor deployment in GitHub Actions and DigitalOcean dashboard

Your app will automatically deploy every time you push to the main branch!

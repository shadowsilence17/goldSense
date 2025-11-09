#!/bin/bash
# Quick push script for DigitalOcean deployment fix

echo "🔧 Fixing DigitalOcean Deployment Issues..."
echo ""

# Add all changes
git add .python-version runtime.txt Procfile requirements.txt app.yaml DO_DEPLOYMENT_FIX.md

echo "📝 Files being committed:"
echo "  • .python-version (Python 3.11)"
echo "  • runtime.txt (Python 3.11.x)"
echo "  • Procfile (Start command)"
echo "  • requirements.txt (Updated dependencies)"
echo "  • app.yaml (Fixed configuration)"
echo "  • DO_DEPLOYMENT_FIX.md (Fix documentation)"
echo ""

# Commit
git commit -m "Fix DigitalOcean deployment issues

Changes:
- Add .python-version file specifying Python 3.11
- Add runtime.txt for buildpack
- Add Procfile with proper web command
- Update requirements.txt with compatible versions
- Remove tensorflow (optional heavy dependency)
- Update numpy to work with Python 3.11
- Fix app.yaml configuration
- Increase health check timeout to 30s

Fixes:
- Python 3.13 compatibility issues
- numpy build failures
- Missing entry point configuration

This should resolve the deployment failures."

if [ $? -eq 0 ]; then
    echo "✅ Changes committed"
    echo ""
    echo "🌐 Pushing to GitHub..."
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ Successfully pushed deployment fixes!"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "📋 Next Steps:"
        echo ""
        echo "1. ⏳ Wait for automatic deployment (if CI/CD enabled)"
        echo "   OR"
        echo "   Go to DigitalOcean → Your App → Force Rebuild"
        echo ""
        echo "2. 👀 Watch the build logs:"
        echo "   Should show: 'Installing Python 3.11' ✅"
        echo "   Should show: 'Successfully installed numpy...' ✅"
        echo ""
        echo "3. ✅ Test your deployed app:"
        echo "   curl https://your-app.ondigitalocean.app/health"
        echo ""
        echo "📚 Documentation:"
        echo "   See: DO_DEPLOYMENT_FIX.md for details"
        echo ""
    else
        echo "❌ Push failed"
    fi
else
    echo "❌ Commit failed"
fi

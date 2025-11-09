"""
WSGI entry point for DigitalOcean deployment
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app from webapp directory
from webapp.app import app as application

# For gunicorn
app = application

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    application.run(host='0.0.0.0', port=port)

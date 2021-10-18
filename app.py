"""
    Entry Point for mabusha Bouncers and Security Services Backend
"""
import os

from src.main import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8001)))
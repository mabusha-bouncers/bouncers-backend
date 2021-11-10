"""
    Bouncers & Security Guards Dispatcher
        Web Application
"""
import os
from src.main import create_app

app = create_app()


@app.route('/_ah/warmup')
def warmup():
    """warm app handler for google cloud platform"""
    return 'OK', 200


if __name__ == '__main__':
    """
        Runs a flask application 
    """
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8001)))

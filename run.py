import os

from dataAnalysis import app

#config_name = os.getenv('FLASK_CONFIG')
#app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
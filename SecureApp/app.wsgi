import sys
import os

# Add the directory containing your 'app.py' to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80)


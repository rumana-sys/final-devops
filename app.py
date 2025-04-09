from flask import Flask
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def hello_cloud():
    return 'Hello Cloud!'

app.run(host='0.0.0.0', port=5000)

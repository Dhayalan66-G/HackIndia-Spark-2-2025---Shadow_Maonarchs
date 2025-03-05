from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='bing')

# Serve the map.html file directly
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'map.html')

# Serve static files (like js, css, and images)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)

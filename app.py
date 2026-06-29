from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io
import requests

app = Flask(__name__)

@app.route('/remove-bg')
def remove_bg():
    url = request.args.get('url')
    if not url:
        return 'url parameter required', 400
    try:
        R = requests.get(url, timeout=10)
        image = Image.open(io.BytesIO(R.content))
        result = remove(image)
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        buf.seek(0)
        response = send_file(buf, mimetype='image/png')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

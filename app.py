from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    url = request.args.get('url') or request.form.get('url')
    if url:
        try:
            # Forward the request to the specified URL
            headers = {'X-Forwarded-For': request.remote_addr}  # Forward client's IP
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return jsonify({
                'status': 'success',
                'response': response.text
            })
        except requests.exceptions.RequestException as e:
            return jsonify({
                'status': 'error',
                'message': f"An error occurred: {e}"
            })

    return jsonify({
        'status': 'error',
        'message': 'URL parameter is missing'
    })

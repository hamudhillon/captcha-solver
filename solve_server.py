from flask import Flask, request, jsonify
from solve_captcha import solve_captcha

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve():
    base64_data = request.json.get("base64")
    if not base64_data:
        return jsonify({"error": "Missing 'base64' in request"}), 400
    result = solve_captcha(base64_data)
    print(result)
    return jsonify({"text": result})

if __name__ == '__main__':
    app.run(port=5005)

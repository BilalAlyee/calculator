from flask import Flask, render_template, request, jsonify
from calculator_math import safe_eval
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    expression = data.get('expression', '')
    angle_mode = data.get('angle_mode', 'deg')
    
    try:
        result = safe_eval(expression, angle_mode=angle_mode)
        return jsonify({'result': result, 'error': None})
    except Exception as e:
        return jsonify({'result': None, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

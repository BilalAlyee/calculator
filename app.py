"""
Scientific Calculator Web Application
A professional web-based scientific calculator with Flask backend.

Author: Bilal Alyee
License: MIT
"""

from flask import Flask, render_template, request, jsonify
from calculator_math import safe_eval
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    """Serve the main calculator HTML page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Process mathematical expressions and return results.
    
    Request JSON:
        - expression (str): Mathematical expression to evaluate
        - angle_mode (str): 'deg' or 'rad' for trigonometric functions
    
    Response JSON:
        - result (float): Calculation result
        - error (str): Error message if calculation failed, else None
    """
    try:
        data = request.get_json()
        expression = data.get('expression', '').strip()
        angle_mode = data.get('angle_mode', 'deg')
        
        if not expression:
            return jsonify({'result': None, 'error': 'Empty expression'})
        
        # Validate angle mode
        if angle_mode not in ('deg', 'rad'):
            angle_mode = 'deg'
        
        # Evaluate the expression safely
        result = safe_eval(expression, angle_mode=angle_mode)
        
        # Round to 10 decimal places to avoid floating point precision issues
        result = round(result, 10)
        
        return jsonify({'result': result, 'error': None})
    
    except Exception as e:
        logger.error(f"Calculation error: {str(e)}")
        return jsonify({'result': None, 'error': str(e)})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    logger.error(f"Server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server (use gunicorn in production)
    app.run(debug=True, host='127.0.0.1', port=5000)

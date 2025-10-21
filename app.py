import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def precedence(op):
    """Return precedence of operators"""
    if op in ['+', '-']:
        return 1
    if op in ['*', '/']:
        return 2
    if op == '^':
        return 3
    return 0

def is_operator(char):
    """Check if character is an operator"""
    return char in ['+', '-', '*', '/', '^']

def infix_to_postfix_steps(expression):
    """Convert infix to postfix with step-by-step tracking"""
    steps = []
    stack = []
    output = []
    
    # Remove spaces
    expression = expression.replace(' ', '')
    
    # Initial state
    steps.append({
        'step': 0,
        'token': '—',
        'stack': [],
        'output': [],
        'description': 'Initial state'
    })
    
    step_num = 1
    
    for i, char in enumerate(expression):
        if char.isalnum():  # Operand
            output.append(char)
            steps.append({
                'step': step_num,
                'token': char,
                'stack': stack.copy(),
                'output': output.copy(),
                'description': f'Operand "{char}" added to output'
            })
            step_num += 1
            
        elif char == '(':
            stack.append(char)
            steps.append({
                'step': step_num,
                'token': char,
                'stack': stack.copy(),
                'output': output.copy(),
                'description': 'Left parenthesis pushed to stack'
            })
            step_num += 1
            
        elif char == ')':
            while stack and stack[-1] != '(':
                popped = stack.pop()
                output.append(popped)
                steps.append({
                    'step': step_num,
                    'token': char,
                    'stack': stack.copy(),
                    'output': output.copy(),
                    'description': f'Popped "{popped}" from stack to output'
                })
                step_num += 1
            
            if stack:
                stack.pop()  # Remove '('
                steps.append({
                    'step': step_num,
                    'token': char,
                    'stack': stack.copy(),
                    'output': output.copy(),
                    'description': 'Right parenthesis: removed matching left parenthesis'
                })
                step_num += 1
                
        elif is_operator(char):
            while (stack and stack[-1] != '(' and
                   precedence(stack[-1]) >= precedence(char)):
                popped = stack.pop()
                output.append(popped)
                steps.append({
                    'step': step_num,
                    'token': char,
                    'stack': stack.copy(),
                    'output': output.copy(),
                    'description': f'Popped "{popped}" (higher/equal precedence) from stack'
                })
                step_num += 1
            
            stack.append(char)
            steps.append({
                'step': step_num,
                'token': char,
                'stack': stack.copy(),
                'output': output.copy(),
                'description': f'Operator "{char}" pushed to stack'
            })
            step_num += 1
    
    # Pop remaining operators
    while stack:
        popped = stack.pop()
        output.append(popped)
        steps.append({
            'step': step_num,
            'token': '—',
            'stack': stack.copy(),
            'output': output.copy(),
            'description': f'Popped remaining operator "{popped}" from stack'
        })
        step_num += 1
    
    return {
        'postfix': ''.join(output),
        'steps': steps,
        'total_steps': len(steps) - 1
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    expression = data.get('expression', '')
    
    if not expression:
        return jsonify({'error': 'No expression provided'}), 400
    
    try:
        result = infix_to_postfix_steps(expression)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
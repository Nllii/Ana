from flask import Flask, request
import subprocess
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the parent directory to the Python module search path
sys.path.append(parent_dir)
from library import notification
app = Flask(__name__)


@app.route('/')
def index():
    return "{ code: ''}, { message: ''}"


@app.route('/imessage', methods=['POST'])
def execute_code():
    code = request.form.get('code')  # Assuming the client sends the code in the 'code' field of the POST request
    if code:
        try:
            # Execute the code using the 'exec' function
            exec(code)
            return "Code executed successfully."
        except Exception as e:
            return f"Error executing code: {str(e)}", 400
    else:
        message = request.form.get('message')  # Assuming the client sends the command in the 'command' field of the POST request
        if not message:
            return "No code or command provided.", 400
        try:
            output = notification().send_message(message)
            return output
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.output}", 400






# Start the server.
if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5020, debug=False)

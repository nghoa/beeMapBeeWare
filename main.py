from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('mymap.html')

if __name__ == '__main__':
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "5000")

    # If the debug flag is set the server will automatically 
    # reload for code changes and show a debugger in case an exception happened.
    debugging = True
    app.run(host=host, port=port, debug=debugging)

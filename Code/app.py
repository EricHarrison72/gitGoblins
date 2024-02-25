# NOTE: This file exists to help us start us out. 
# We may want to break our app into several python files for different components later on.
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True)

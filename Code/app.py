# NOTE: This file exists to help us start us out. 
# We may want to break our app into several python files for different components later on.
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    message = "Hello World!"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)

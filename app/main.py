# hello world program
from flask import Flask, jsonify

# environment variables
from dotenv import load_dotenv
load_dotenv()  # take environment variables

# import environ variables
import os

# instance of flask application
app = Flask(__name__)

# index route
@app.route("/")
def index():
    return "<div>Index route accessed.</div>"

# string evaluator route
@app.route("/eval")
def evaluator():
    a = 1
    b = 2
    c = a + b
    return jsonify(c)

# hello world environment variable demonstration
@app.route("/hello-world")
def hello_world():
    return "<p>%s</p>" % os.environ['greeting']


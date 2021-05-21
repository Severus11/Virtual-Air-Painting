from flask import Flask, render_template, Response  

app = Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')
def gen ():
    while True:
        
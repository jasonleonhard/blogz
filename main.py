from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    """."""
    return render_template('index.html')

@app.route("/example", methods=['POST', 'GET'])
def example():
    """."""
    return render_template('example.html')

if __name__ == '__main__':
    app.run()

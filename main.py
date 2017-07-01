from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ornottodo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
# db.create_all()

# class extends db model
class Blog(db.Model):
    """."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    # def __repr__(self):
        # return '<Blog %r>' % self.name

    def __init__(self, name):
        self.name = name

@app.route("/")
def index():
    """."""
    return render_template('index.html')

@app.route("/example", methods=['POST', 'GET'])
def example():
    """."""
    return render_template('example.html')


blogs = []
@app.route("/blogs", methods=['POST', 'GET'])
def blog():
    if request.method == 'POST':
        blog = request.form['blog']
        blogs.append(blog)
    return render_template('blogs.html', title="Blogs!", blogs=blogs)

if __name__ == '__main__':
    app.run()

from flask import Flask, request, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from lib import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:ornottodo@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    """Blog class definition and init."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def index():
    """."""
    return render_template('index.html')

@app.route("/example", methods=['POST', 'GET'])
def example():
    """."""
    return render_template('example.html')

@app.route("/blog")
def blog(blog_title='', blog_body='', blog_title_error='', blog_body_error='',
             blogs='', prev_blog_title='',prev_blog_body=''):
    """."""
    blogs = Blog.query.all() # show current blogs in db
    # add to database
    if request.args: # if request.method == 'GET':
        blog_title = request.args.get('blog_title')
        blog_body = request.args.get('blog_body')
    else:
        return render_template('blogs.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body,
                               blog_title_error=blog_title_error, blog_body_error=blog_body_error)
    # Validation Section # make sure that
    # last blog is not the same as next blog
    blog_count = Blog.query.count()
    if blog_count:
        prev_blog_title = Blog.query.order_by('-id').first().title
        prev_blog_body = Blog.query.order_by('-id').first().body
    if blogs_have_same_content(prev_blog_title, blog_title, prev_blog_body, blog_body):
        blog_title_error = 'Blogs must be different'
    # not blank
    if no_field_blank(blog_title, blog_body):
        blog_title_error = 'Must not leave any field blank'
    # no errors on page before or rerender page with errors
    if blog_title_error or blog_body_error:
        return render_template('blogs.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body,
                               blog_title_error=blog_title_error, blog_body_error=blog_body_error)
    else: # actual adding of new blog to db
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        blogs = Blog.query.all()
        return render_template('blogs.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body,
                               blog_title_error=blog_title_error, blog_body_error=blog_body_error)

@app.route("/delete_blog", methods=['POST'])
def delete_blog():
    """."""
    blog_id = int(request.form['blog-id']) # id was found http://localhost:5000/POST?blog-id=27 The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()
    blogs = Blog.query.all()
    # return render_template('blogs.html', title="Blogs", blogs=blogs) # works
    return redirect('/blog') # better bc returns to page without /delete_blog in url


# disable browser caching
@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run()

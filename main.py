"""CRUD functionality for blogging."""
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
    """Renders links. Could also become a splash screen or signin."""
    return render_template('index.html', title='Greetings', directions='Links provided below.')

@app.route("/blog")
def blog(blog_title='', blog_body=''):
    """Lists all blogs. Does not allow new blog creation nor validation.
        aka if given the correct url the id template will render all 3 requested
            http://localhost:5000/blog?id=366&blog_title=title&blog_body=body
        otherwise:
            http://localhost:5000/blog"""
    if request.args:
        blog_title = get_title()
        blog_body = get_body()
        # return "blog-id: %s <br> blog_title: %s <br> blog_body: %s" % (id, blog_title, blog_body)
        return render_template('id.html', title="Blogs",
                               blog_title=blog_title, blog_body=blog_body)
    else:
        blogs = query_all_blogs_lifo()
        return render_template('blog.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body)

@app.route("/blogs")
def blogs(blog_title='', blog_body='', blog_title_error='', blog_body_error='',
          prev_blog_title='', prev_blog_body='', blogs=''):
    """I would prefer to handle posts, gets and validations all on one page '/blogs'"""
    blogs = query_all_blogs_lifo()
    # add to database
    if request.args: # if request.method == 'GET':
        blog_title = get_title()
        blog_body = get_body()
    else: # Avoid validation first time template is rendered
        return render_template('blogs.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body)
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
    # actual adding of new blog to DB
    if not blog_title_error or blog_body_error:
        create_new_blog(blog_title, blog_body)
        blogs = query_all_blogs_lifo()

    # no errors on page or rerender page with errors
    return render_template('blogs.html', title="Blogs", blogs=blogs,
                           blog_title=blog_title, blog_body=blog_body,
                           blog_title_error=blog_title_error, blog_body_error=blog_body_error)

@app.route("/newpost")
def newpost(blog_title='', blog_body='', blog_title_error='', blog_body_error='',
            prev_blog_title='', prev_blog_body=''):
    """Create new blog and validate. Does not list blogs."""
    if request.args: # if request.method == 'GET':
        blog_title = get_title()
        blog_body = get_body()
    else: # Avoid validation first time template is rendered
        return render_template('newpost.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body)
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
        return render_template('newpost.html', title="Blogs",
                               blog_title=blog_title, blog_body=blog_body,
                               blog_title_error=blog_title_error, blog_body_error=blog_body_error)
    # add new blog to DB
    else:
        create_new_blog(blog_title, blog_body)
        # on successful creation, show that new blog entry
        return render_template('id.html', title="Blogs", blog=blog, blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body, id=id)

@app.route("/delete_blog", methods=['GET', 'POST'])
def delete_blog():
    """Remove a blog from /blog."""
    deleting_blog()
    return redirect('/blog')

@app.route("/delete_blog2", methods=['GET', 'POST'])
def delete_blog2():
    """Remove a blog from /blogs. Added for different redirect for /blogs"""
    deleting_blog()
    return redirect('/blogs') # better bc returns to page without /delete_blog in url

@app.route("/delete_blog3", methods=['GET', 'POST'])
def delete_blog3():
    """Remove a blog from /id. Just redirects to blog where the same button actually can delete."""
    return redirect('/blog')

# Section added to DRY up the code
def get_title():
    """Accessing get request parameters of title."""
    return request.args.get('blog_title')

def get_body():
    """Accessing get request parameters of body."""
    return request.args.get('blog_body')

def query_all_blogs_fifo():
    """FIFO query all blogs, aka order of first appearance order."""
    return Blog.query.all()

def query_all_blogs_lifo():
    """LIFO query all blogs, aka reverse order."""
    return Blog.query.order_by(Blog.title.desc()).all()

def deleting_blog():
    """Delete a blog by blog-id we use request parameters and session."""
    blog_id = int(request.form['blog-id'])
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()
    # blogs = query_all_blogs_lifo()
    # return render_template('blogs.html', title="Blogs", blogs=blogs) # works

def create_new_blog(blog_title='', blog_body=''):
    """Create a new blog using session."""
    blog = Blog(blog_title, blog_body)
    db.session.add(blog)
    db.session.commit()
    return blog

# interesting experiment section
    # @app.route('/blog/<int:blog_id>')
    # def show_blog(blog_id):
    #     """show the post with the given id, the id is an integer
    #     This works to show an id by its url ie http://localhost:5000/blog/368"""
    #     return 'blog %d' % blog_id

    # @app.route('/blog<int:id>')
    # def show_one_blog(id):
    #     """Sort of works for individual blog by id... http://localhost:5000/blog368"""
    #     # id = id
    #     id = Blog.query.get(id)
    #     return render_template('id.html', title="Blogs", id=id)

    # @app.route("/blog")
    # def bloggy(blog_title='', blog_body='', blogs='', prev_blog_title='', prev_blog_body=''):
    #     """This allows for params to be accessed but not /blog without it.
    #     http://localhost:5000/blog?id=366"""
    #     if request.args:
    #         id = request.args.get('id') # grabbing yes
    #         title = request.args.get('title') # none to grab
    #         body = request.args.get('body')
    #         return "blog-id: %s <br> title: %s <br> body: %s" % (id, title, body)

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

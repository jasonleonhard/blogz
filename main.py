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
    """Renders links."""
    # return render_template('index.html'
    return redirect('/blogs')

@app.route("/example", methods=['POST', 'GET'])
def example():
    """Very simple example of routing and template rendering."""
    return render_template('example.html')

@app.route("/blog")
def blog(blog_title='', blog_body='',
             blogs='', prev_blog_title='',prev_blog_body=''):
    """Lists all blogs. Does not allow new blog creation nor validation."""
    blogs = Blog.query.all() # show current blogs in db

    # this version works great if you don't delete the first item
    return render_template('blog.html', title="Blogs", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body)

    # # this version works great for deleting first item but doesn't render all blogs at all...
    # return render_template('blog.html', title="Blogs",
    #                         blog_title='', blog_body='')

@app.route("/newpost")
def newpost(blog_title='', blog_body='', blog_title_error='', blog_body_error='',
            prev_blog_title='', prev_blog_body=''):
    """Create new blog and validate. Does not list blogs."""
    if request.args: # if request.method == 'GET':
        blog_title = request.args.get('blog_title')
        blog_body = request.args.get('blog_body')

    # Validation Section # make sure that
    # last blog is not the same as next blog
    blog_count = Blog.query.count()
    if blog_count > 1:
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
    else:
        # actual adding of new blog to db
        new_blog = Blog(blog_title, blog_body)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blog') # better bc returns to page without /delete_blog in url

@app.route("/delete_blog", methods=['POST'])
def delete_blog():
    """Remove a blog. WIP: Works great with /blogs, but on /blog cannot delete top blog item."""
    blog_id = int(request.form['blog-id'])
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()
    # return render_template('blogs.html', title="Blogs", blogs=blogs) # works
    blog_count = Blog.query.count()  # work around to delete last blog
    if blog_count != 1:
        return redirect('/blog')  # better bc returns to page without /delete_blog in url
    else:
        return redirect('/blogs')

@app.route("/blogs")
def blogs(blog_title='', blog_body='', blog_title_error='', blog_body_error='',
             blogs='', prev_blog_title='',prev_blog_body=''):
    """I would prefer to handle posts, gets and validations all on one page '/blogs'"""
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

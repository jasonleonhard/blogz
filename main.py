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

@app.route("/example", methods=['POST', 'GET'])
def example():
    """Very simple example of routing and template rendering."""
    return render_template('example.html')

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
    if blog_count != 0:
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
    # add new blog to db
    else:
        blog = Blog(blog_title, blog_body)
        db.session.add(blog)
        db.session.commit()
        # on successful creation, show that new blog entry
        return render_template('id.html', title="Blogs", blog=blog, blogs=blogs,
                                blog_title=blog_title, blog_body=blog_body, id=id)

@app.route("/delete_blog", methods=['GET', 'POST'])
def delete_blog():
    """Remove a blog from /blog."""
    blog_id = int(request.form['blog-id'])
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()
    return redirect('/blog')

@app.route("/delete_blog2", methods=['GET', 'POST'])
def delete_blog2():
    """Remove a blog from /blogs. Added for different redirect for /blogs"""
    blog_id = int(request.form['blog-id'])
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()
    # blogs = Blog.query.all()
    # return render_template('blogs.html', title="Blogs", blogs=blogs) # works
    return redirect('/blogs') # better bc returns to page without /delete_blog in url

@app.route("/delete_blog3", methods=['GET', 'POST'])
def delete_blog3():
    """Remove a blog from /id. Just redirects to blog where the same button actually can delete."""
    return redirect('/blog')

@app.route("/blog")
def blog(blog_title='', blog_body='', blogs='', prev_blog_title='',prev_blog_body=''):
    """ If params are captured into the url:
    aka if given the correct url the id template will render all 3 requested
    http://localhost:5000/blog?id=366&blog_title=title&blog_body=body
    otherwise:
    http://localhost:5000/blog
    Lists all blogs. Does not allow new blog creation nor validation.
    WIP part is when title is clicked that the id title and body are added to url and then a rerender
    """
    if request.args:
        id = request.args.get('id')
        blog_title = request.args.get('blog_title')
        blog_body = request.args.get('blog_body')
        # return "blog-id: %s <br> blog_title: %s <br> blog_body: %s" % (id, blog_title, blog_body)
        return render_template('id.html', title="Blogs", blogs=blogs,
                                blog_title=blog_title, blog_body=blog_body, id=id)
    else:
        blogs = Blog.query.all() # show current blogs in db
        # if blogs:
        # this version works great if you don't delete the first item
        return render_template('blog.html', title="Blogs", blogs=blogs,
                                    blog_title=blog_title, blog_body=blog_body)
        # else:
            # this version works great for deleting first item but doesn't render all blogs at all...
            # return render_template('blog.html', title="Blogs",
                                    # blog_title='', blog_body='')

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
    # def bloggy(blog_title='', blog_body='', blogs='', prev_blog_title='',prev_blog_body=''):
    #     """This allows for params to be accessed but not /blog without it.
    #     http://localhost:5000/blog?id=366"""
    #     if request.args:
    #         id = request.args.get('id') # grabbing yes
    #         title = request.args.get('title') # none to grab
    #         body = request.args.get('body')
    #         return "blog-id: %s <br> title: %s <br> body: %s" % (id, title, body)

    # # /blog?id=6
    # @app.route("/individual", methods=['GET', 'POST'])
    # def individual(id = ''):
    #     # if request.args: # if request.method == 'GET':
    #     # if request.args.id: # if request.method == 'GET':
    #     #     id = int(id)
    #     # else:
    #     #     id = int(0)
    #     form_value = request.args.get('param_name')
    #     # request.args.get = 6
    #     # http://localhost:5000/blog?id=6
    #     # return render_template('individual.html', title="Blogs",
    #     #                     blog_title=blog_title, blog_body=blog_body,
    #     #                     blog_title_error=blog_title_error, blog_body_error=blog_body_error)
    #     return render_template('individual.html', title="Blogs", id=id)

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

"""CRUD functionality for users blogging."""
from flask import request, redirect, render_template, session, flash #, url_for
import cgi
from app import app, db
from models import User, Blog
from lib import *
import hashutils
# from hashutils import check_pw_hash

@app.route('/session', methods=['POST', 'GET'])
def current_session():
    """ALl of the logic here can be tested and or ttd
    1: Users dont exist
         Create users by redirecting to signup page
    2: Users exist
         Check if there is a session cookie
           if so then
             log users data
           if not then
             redirect to log in page
    """
    users = query_all_users_lifo()
    if len(users) == 0:
        return redirect('/signup')
    if session:
        print("\n" + str(session) + "\n")
        return render_template('session.html', users=users, title='Session')
    else:
        return redirect('/login')

@app.route('/userlist', methods=['POST', 'GET'])
def userlist():
    """
    1. Check if there are any users
         if so then
           list them lifo: name, pw, id
         if not then
           redirect to signup page
    """
    users = query_all_users_lifo()
    if len(users) == 0:
        return redirect('/signup')
    else:
        return render_template('userlist.html', title='User List', users=users)

@app.route('/randstr', methods=['POST', 'GET'])
def randstr():
    if request.method == 'GET':
        return render_template('randstr.html', title='randstr')
    if request.method == 'POST':
        hashed_password = hashutils.make_salt()
        print(hashed_password)
        return render_template('randstr.html', title='randstr', hashed_password=hashed_password)

@app.route('/salt', methods=['POST', 'GET'])
def salt():
    if request.method == 'GET':
        return render_template('salt.html', title='Salt')
    if request.method == 'POST':
        # password = request.form['password']
        # hashed_password = password + hashutils.make_salt()
        # password = request.form['hashed_password']
        # password = request.form['password']
        # print(hashed_password)
        # return render_template('salt.html', title='Salt', password=password, hashed_password=hashed_password)

        # vs LC way
        password = request.form['password']
        salt = hashutils.make_salt()
        hash = hashutils.make_pw_hash(password, salt)
        hashed_password = password + hash
        print(hashed_password)
        password = hashutils.check_pw_hash(password, hash)
        # check_result = hashutils.check_pw_hash(password, hash)
        return render_template('salt.html', title='Salt', password=password, hashed_password=hashed_password)

@app.route('/signup', methods=['POST', 'GET'])
def signup(users=''):
    """
    00. if session
          no need to sign up, redirect to newpost
    0. display username and password input fields with add user button next to fields
    1. Check if there are any users
        if not then
          No users signed up yet shows on page
        if so then
          list all users
            have delete user button near each user
    2. On POST request by add user button
         validate users name and password
           deny if
             repetition
             too short
             not alpha numeric characters
             etc
           if not denied then
             start to create user
             capture session data needed for blog post
               username, password (maybe), user id."""
    if session:
        return redirect('/newpost')
    else:
        users = query_all_users_lifo()
        # if request.method == 'GET':
        #     username = ''
        #     return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            verify = request.form['verify']
            # validate user's data
            # if not existing_user:
            if verify == '' or password == '' or username == '':
                username_error = "Must not leave any field blank."
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            if verify != password:
                username_error = "Password and verify do not match."
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            # only allow unique user names to be created
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                username_error = "Duplicate user."
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            if len(username) < 3 or len(password) < 3:
                username_error = "Username and password must be at least 3 characters."
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            if username == password:
                username_error = "Username and password must be different"
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            offensive_list = ['bitch', 'cunt', 'dick', 'whore', 'slut', 'republican', 'trump', 'cock', 'pussy', 'twat', 'tits',
                            'porn', 'semen', 'ass', 'asshole', 'jizz', 'fuck', 'orgy', 'christ', 'death', 'shit', 'racist',
                            'piss', 'vagina', 'penis', 'boner', 'murder', 'hostage', 'kidnap', 'sex', 'feces', 'poop', 'crap',
                            'breast', 'genital', 'genitalia', 'scrotum', 'balls', 'ballsac', 'ballsack', 'clitoris', 'kkk', 'ku klux klan',
                            'assault', 'torture', 'domestic violence', 'suicide', 'kill', 'killer', 'fart', 'bile', 'bad words' ]
            for word in offensive_list:
                if username == word or password == word:
                    username_error = "Please tone down that language."
                    return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
                # Other ideas for improving on offensive list
                    # no combonations of these
                    # _ - ....
                    # pluralities verbs and past tense: s, es, ed, ing
                    # racist words, phrases and slurs
            if not username.isalpha:
                username_error = "Username must only contain characters in the alphabet."
                return render_template('signup.html', title='Sign up', users=users, username_error=username_error, username=username, password=password, verify=verify)
            else:
                # When all validations have passed, create user and store name, pw and id in session
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                session['password'] = password

                # re-query all users so when page shows again it will reflect new user
                users = query_all_users_lifo()
                user = User.query.filter_by(username=username).first()
                session['id'] = user.id
                # username_error = "Duplicate user"
                return render_template('signup.html', title='Sign up', users=users)
        return render_template('signup.html', title='Sign up', users=users)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if session:
        del session['id']
        del session['username']
        del session['password']
    return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    """If someone is logged in they should not see login page,
    they should instead be redirected to the new post page.
    Otherwise they should log in."""
    if session:
        return redirect('/newpost')
    else:
        users = query_all_users_lifo()
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            # pw_hash = hashutils.check_pw_hash(password, user.pw_hash)
            if user and user.password == password: # regular pw
            # if user and pw_hash: # hashed pw
                session['username'] = username
                session['password'] = password
                    # session['pw_hash'] = pw_hash
                    # session['password'] = pw_hash
                session['id'] = user.id
                db.session.commit()
                flash("Logged in as: " + username)
                # return render_template('newpost.html', title="New Post", user=user)
                return redirect('/newpost')
            else:
                flash('User password incorrect, or user does not exist', 'error')
        return render_template('login.html', users=users, title="Log in")

def create_new_blog(owner, blog_title='', blog_body=''):
    """Create a new blog using session."""
    blog = Blog(blog_title, blog_body, owner)
    db.session.add(blog)
    db.session.commit()
    return blog

@app.route("/newpost", methods=['POST', 'GET'])
def newpost(blog_title='', blog_body='', blog_error=''):
    """1. Must be logged in to create a post (aka session present)
    if logged in (session)
      if get
        return basic empty template
      if post
        grab imputs
          title
          body
    """
    """Create new blog and validate. Does not list blogs."""
    if session:
        if request.method == 'GET':
            return render_template('newpost.html', title="New Post")
        if request.method == 'POST':
            # users = query_all_users_lifo()
            blog_title = request.form['blog_title']
            blog_body = request.form['blog_body']
            username = session['username']
            owner = User.query.filter_by(username=username).first()
            # blogs = Blog.query.filter_by(owner=owner).all()
            user_id = session['id']
            user = User.query.get(user_id)
            # print()
            # print()
            # print(user)
            # print(user.username)
            # print(username)
            # print(user.id)
            # print(user_id)
            # print()
            # print()
            # WIP: validate before creation
            # 1. only allow unique blog names to be created
            existing_blog_title = Blog.query.filter_by(title=blog_title).first()
            existing_blog_body = Blog.query.filter_by(body=blog_body).first()
            # print(existing_blog_title)
            # print(existing_blog_body)
            if existing_blog_title or existing_blog_body:
                blog_error = "Duplicate Blog."
                return render_template('newpost.html', title='New Post', blog_title=blog_title, blog_body=blog_body, blog_error=blog_error)
            if len(blog_title) < 3 or len(blog_body) < 3:
                blog_error = "title and body must be at least 3 characters."
                return render_template('newpost.html', title='New Post', blog_title=blog_title, blog_body=blog_body, blog_error=blog_error)
            if blog_title == blog_body:
                blog_error = "title and body must be different"
                return render_template('newpost.html', title='New Post', blog_title=blog_title, blog_body=blog_body, blog_error=blog_error)
            offensive_list = ['bitch', 'cunt', 'dick', 'whore', 'slut', 'republican', 'trump', 'cock', 'pussy', 'twat', 'tits',
                            'porn', 'semen', 'ass', 'asshole', 'jizz', 'fuck', 'orgy', 'christ', 'death', 'shit', 'racist',
                            'piss', 'vagina', 'penis', 'boner', 'murder', 'hostage', 'kidnap', 'sex', 'feces', 'poop', 'crap',
                            'breast', 'genital', 'genitalia', 'scrotum', 'balls', 'ballsac', 'ballsack', 'clitoris', 'kkk', 'ku klux klan',
                            'assault', 'torture', 'domestic violence', 'suicide', 'kill', 'killer', 'fart', 'bile', 'bad words' ]
            for word in offensive_list:
                if blog_title == word or blog_body == word:
                    blog_error = "Please tone down that language."
                    return render_template('newpost.html', title='New Post', blog_title=blog_title, blog_body=blog_body, blog_error=blog_error)
                # Other ideas for improving on offensive list
                    # no combonations of these
                    # _ - ....
                    # pluralities verbs and past tense: s, es, ed, ing
                    # racist words, phrases and slurs
            if not blog_title.isalpha:
                blog_error = "blog title must only contain characters in the alphabet."
                return render_template('newpost.html', title='New Post', blog_title=blog_title, blog_body=blog_body, blog_error=blog_error)
            else:
                # When all validations have passed, create user and store name, pw and id in session
                create_new_blog(owner, blog_title, blog_body)
                blog = create_new_blog(owner, blog_title, blog_body)
                # on successful creation, show that new blog entry
                blogs = query_all_blogs_lifo()
                # return render_template('blog.html', title="Blog", blogs=blogs,
                #                         blog_title=blog_title, blog_body=blog_body, owner=owner)

                # instead of listing all blogs the client wishes we show just the newly created blog
                return render_template('singlePost.html', title="New Blog Post", blog=blog)
    else:
        return redirect('/login')

@app.route("/myblogs", methods=['POST', 'GET'])
def myblogs(blog_title='', blog_body=''):
    """Only list my blogs."""
    if session:
        owner = User.query.filter_by(username=session['username']).first()
        myblogs = Blog.query.filter_by(owner=owner).all()
        return render_template('blog.html', title="My Blogs", myblogs=myblogs, blog_title=blog_title,
                                blog_body=blog_body, owner=owner)
    else:
        return redirect('/login')

@app.route("/blog")
def blog(blog_title='', blog_body='', blog_id=''):
    """Lists all blogs. Does not allow new blog creation nor validation.
        aka if given the correct url the id template will render all 3 requested
            http://localhost:5000/blog?id=366&blog_title=title&blog_body=body
        otherwise:
            http://localhost:5000/blog"""
    if request.args:
        blog_title = get_title()
        blog_body = get_body()
        blog_id = get_id()
        blog_owner = get_owner()
        return render_template('id.html', title="Blog",
                               blog_title=blog_title, blog_body=blog_body, blog_id=blog_id, blog_owner=blog_owner)
    else:
        blogs = query_all_blogs_lifo()
        return render_template('blog.html', title="Blog", blogs=blogs,
                               blog_title=blog_title, blog_body=blog_body, blog_id=blog_id)

@app.route("/blogs")
def blogs(blogs='', owner='', blog_title='', blog_body='', blog_title_error='', blog_body_error='',
          prev_blog_title='', prev_blog_body=''):
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
        create_new_blog(blog_title, blog_body, owner)
        blogs = query_all_blogs_lifo()

    # no errors on page or rerender page with errors
    return render_template('blogs.html', title="Blogs", blogs=blogs,
                           blog_title=blog_title, blog_body=blog_body,
                           blog_title_error=blog_title_error, blog_body_error=blog_body_error)

@app.route('/delete-user', methods=['GET', 'POST'])
def delete_user():
    """Delete user works. grabs hidden user id from form, queries by it and deletes with db commit."""
    # if request.method == 'POST':
    user_id = int(request.form['user-id'])
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    if session:
        del session['id']
        del session['username']
        del session['password']
    return redirect('/signup')

def deleting_blog():
    """Delete a blog by blog-id we use request parameters and session."""
    blog_id = int(request.form['blog-id'])
    blog_target = Blog.query.get(blog_id)
    db.session.delete(blog_target)
    db.session.commit()

@app.route("/delete_blog", methods=['GET', 'POST'])
def delete_blog():
    """Remove a blog from /blog."""
    deleting_blog()
    return redirect('/blog')

@app.route("/delete_blog2", methods=['GET', 'POST'])
def delete_blog2():
    """Remove a blog from /blogs. Added for different redirect for /blogs"""
    deleting_blog()
    return redirect('/blogs')

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

def get_id():
    """Accessing get request parameters of body."""
    return request.args.get('blog_body')

def get_owner():
    """Accessing get request parameters of body."""
    return request.args.get('owner')

def query_all_blogs_fifo():
    """FIFO query all blogs, aka order of first appearance order."""
    return Blog.query.all()

def query_all_blogs_lifo():
    """LIFO query all blogs, aka reverse order."""
    return Blog.query.order_by(Blog.title.desc()).all()

def query_all_users_lifo():
    """LIFO query all blogs, aka reverse order."""
    return User.query.order_by(User.username.desc()).all()

@app.route("/")
def home():
    """Loop users and create urls that send a user to a particular users blog posts.
    As per the clients request we render a list of user links.
    Could become a splash screen or signin."""

    users = query_all_users_lifo()
    return render_template('index.html', title='Greetings', directions='Links provided below.', users=users)

@app.route("/singleuser", methods=['POST', 'GET'])
def singleuser():
    blogs = query_all_blogs_lifo()
    users = query_all_users_lifo()
    user_id = request.args.get('user_id')
    username = request.args.get('username')
    owner = User.query.filter_by(username=username).first()
    owner_id = owner.id
    print('user_id: ' + user_id)              # 8
    print('username: ' + username)            # abb
    print('str(owner_id): ' + str(owner_id))  # 8
    return render_template('singleUser.html', title="This Users Blogs", blogs=blogs, users=users, user_id=user_id, username=username, owner=owner, owner_id=owner_id)

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

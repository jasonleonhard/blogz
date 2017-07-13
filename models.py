"""Note on string limits, they should also be validated."""
from app import db
from hashutils import make_pw_hash

class User(db.Model):
    """User class definition and init."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))#, unique=True)
    password = db.Column(db.String(30)) # regular pw
    hidden = db.Column(db.Boolean)
    # pw_hash = db.Column(db.String(30))    # hashed pw
    blogs = db.relationship('Blog', backref='owner', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password                       # regular pw
        self.hidden = False
        # self.pw_hash = hashutils.make_pw_hash(password)  # hashed pw
        # self.password = hashutils.make_pw_hash(password) # hashed pw

class Blog(db.Model):
    """Blog class definition and init."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))#, unique=True)
    body = db.Column(db.String(140))#, unique=True)
    hidden = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        self.hidden = False

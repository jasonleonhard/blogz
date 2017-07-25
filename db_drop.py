# python3 db_drop.py
from app import db
from models import User, Blog
db.drop_all()
db.session.commit()
exit()


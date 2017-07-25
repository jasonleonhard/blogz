from app import db
from models import User, Blog

# clear data if you need to
# db.drop_all()

# create the database and the db table
db.create_all()

# insert data
user = User('Dingo', 'dingos')
db.session.add(user)

user2 = User('Robot', 'robots')
db.session.add(user2)

user3 = User('Kitten', 'kittens')
db.session.add(user3)

blog = Blog('Dingo: a true story', 'Once there was a dingo of humble beginnings', user)
db.session.add(blog)

blog2 = Blog('Dingo: a true story2', 'Once again there was a dingo of humble beginnings', user)
db.session.add(blog2)

blog3 = Blog('Memoirs of a computer', '000010110100101001010100010011010101110100011010010010101010100010101010101010010101110', user2)
db.session.add(blog3)

blog4 = Blog('Bucket of bolts', 'How I managed to replace half the worlds jobs in under a century: Bleep Blop Bloop', user2)
db.session.add(blog4)

blog5 = Blog('meow for can opener to feed me', 'Chase after silly colored fish toys around the house plop down in the middle where everybody walks yet scratch leg', user3)
db.session.add(blog5)

blog6 = Blog('Jump on human and sleep on her all night long', 'purr in the morning and then give a bite to every human around for not waking up request food', user3)
db.session.add(blog6)

admin = User('Admin', 'admins')
db.session.add(admin)

db.session.commit()
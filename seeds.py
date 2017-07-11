# how to recreate the database and seed data:

# when interactive mode:
    # python3

# otherwise run:
    # python3 seeds.py

from main import db, User, Blog

db.drop_all() # if an when needed
db
db.create_all()
db.session.commit()

# model schema
    # User
        # id, username, password
    # req.
        # username, password

    # Blog
        # id, title, body # owner_id (a foreign key)
    # req.
        # title, body, owner_id

user = User('aaaa', 'aaa')
blog = Blog('Dingo: a true story', 'Once there was a dingo of humble beginnings', user)

db.session.add(user)
db.session.add(blog)
db.session.commit()
# exit()
###########################################################################
# Ref.
users = User.query.all()
blogs = Blog.query.all()
# blogs             # view all
# blogs[0].name     # view first
# blogs[0].title    # view first title
# blogs[0].body     # view first body
# blogs[0].owner    # view first owner object aka user who posted
# blogs[0].owner.id # view first owner id
# blogs[0].owner.username # view first owner id
print()
print('blogs[0].owner.username')
print(blogs[0].owner.username)
print()
print('blogs[0].owner.id')
print(blogs[0].owner.id)
print()
print('users[0].username')
print(users[0].username)
print()
print('users[0].id')
print(users[0].id)
print()
print('if users[0].id == blogs[0].owner.id: return or print True')
if users[0].id == blogs[0].owner.id:
    print(True)

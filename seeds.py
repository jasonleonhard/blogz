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

blog5 = Blog('meow for can opener to feed me, Chase after silly colored fish toys around the house plop down in the middle where everybody walks yet scratch leg', user3)
db.session.add(blog5)

blog6 = Blog('Jump on human and sleep on her all night long be long in the bed', 'purr in the morning and then give a bite to every human around for not waking up request food, purr loud scratch the walls', user3)
db.session.add(blog6)

db.session.commit()
# exit()
###########################################################################
# # Ref.
# users = User.query.all()
# blogs = Blog.query.all()
# # blogs             # view all
# # blogs[0].name     # view first
# # blogs[0].title    # view first title
# # blogs[0].body     # view first body
# # blogs[0].owner    # view first owner object aka user who posted
# # blogs[0].owner.id # view first owner id
# # blogs[0].owner.username # view first owner id
# print()
# print('blogs[0].owner.username')
# print(blogs[0].owner.username) # Dingo
# print()
# print('blogs[0].owner.id')
# print(blogs[0].owner.id)       # 1
# print()
# print('users[0].username')
# print(users[0].username)       # Dingo
# print()
# print('users[0].id')
# print(users[0].id)             # 1
# print()
# print('if users[0].id == blogs[0].owner.id: return or print True')
# if users[0].id == blogs[0].owner.id:
#     print(True)
# ###########################################################################
# # session['username'] = username
# # owner = User.query.filter_by(username=session['username'])
# print()
# username = users[0].username
# print('username')
# print(username)  # Dingo
# print()
# users = User.query.filter_by(username=username)
# print('users')
# print(users)
#     # SELECT user.id AS user_id, user.username AS user_username, user.password AS user_password
#     # FROM user
#     # WHERE user.username = %(username_1)s
# print()
# print('users[0]')
# print(users[0])
# print()
# print('users[0].username')
# print(users[0].username)    # Dingo # and associated SQL query
# print()
# print('users[0].id')
# print(users[0].id)          # 1     # and associated SQL query
# print()
###########################################################################
# # TODO: instead of deleting, add new column that marks hidden=True

# # hidden = False value for model param by default
#     # class Blog(db.Model):
#         # ...
#         # hidden = db.Column(db.Boolean, default=False)
#         # ...

#     # def __init__(self, title, body, owner):
#         # ...
#         # self.hidden = False
#         # ...

# # this will show 0 in phpmyadmin

# # now to grab a list of hidden=False
# current_user_id = users[0].id

# # current_user_id = user[0].id
# def get_current_watchlist(current_user_id):
#     return Blog.query.filter_by(hidden=False, owner_id=current_user_id).all()
# print()
# print(get_current_watchlist(current_user_id))
# # [<models.Blog object at 0x103f690b8>, <models.Blog object at 0x103ea0f60>]
# print()

# # print(get_current_watchlist(current_user_id)[0].title)
# watch_list = get_current_watchlist(current_user_id)
# print(watch_list)
# for i in watch_list:
#     print(i.title)
# print()

# # def get_current_list():
# #     return Blog.query.filter_by(hidden=False).all()

# # def get_hidden_Blogs():
# #     return Blog.query.filter_by(hidden=True).all()

# # Blog = Blog.query.get(Blog_id)

# # tasks = Task.query.filter_by(...).all()
# # tasks = Task.query.get(id)


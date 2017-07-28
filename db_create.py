from app import db
from models import User, Blog
import string
import random
from random import randint
import names
import os

# clear data if you need to
# db.drop_all()

# create the database and the db table
db.create_all()

# from random import *
# print randint(1, 100)
# print random()     # Generate a pseudo-random number between 0 and 1.
# for x in range(10):
#   print random.randint(1,101)

# import requests
# word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
# response = requests.get(word_site)
# WORDS = response.content.splitlines()

def create_word_list():
    word_file = "/usr/share/dict/words"
    WORDS = open(word_file).read().splitlines()
    return WORDS
word_list = create_word_list()
# print(word_list)

def rand_str(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def rand_number():
    return random.randint(0, 9)
# print(rand_number())
# for i in range(100):
#     print(rand_number())

def rand_name():
    return names.get_full_name()

def rand_word(word_list):
    word_list_len = len(word_list) - 1
    rand_num = randint(0, word_list_len)
    return word_list[rand_num]
# print(rand_word(word_list))

def rand_sentence(word_list, words=4):
    sentence = ""
    for i in range(1, words):
        word = rand_word(word_list)
        sentence += word + " "
    return sentence
# print(rand_sentence(word_list))

def create_users(word_list, n=6):
    i = 0
    while i < n:
        current_user = User(rand_name(), 'abc')
        # rs1 = rand_str(11)
        # # rs2 = rand_str(11)

        rs1 = rand_sentence(word_list)
        rs2 = rand_sentence(word_list, 8)

        # print(rs1)
        # print()
        # print(rs2)
        current_blog = Blog(rs1, rs2, current_user)

        db.session.add(current_user)
        db.session.add(current_blog)
        i += 1
print(create_users(word_list))
# print(word_list)
# print(type(word_list))


# insert data
user1 = User('Dingo', 'dingos')
user2 = User('Robot', 'robots')
user3 = User('Kitten', 'kittens')
user4 = User(rand_str(11), 'abc')

blog = Blog('Dingo: a true story', 'Once there was a dingo of humble beginnings', user1)
blog2 = Blog('Dingo: a true story2', 'Once again there was a dingo of humble beginnings', user1)
blog3 = Blog('Memoirs of a computer', '000010110100101001010100010011010101110100011010010010101010100010101010101010010101110', user2)

blog4 = Blog('Bucket of bolts', 'How I managed to replace half the worlds jobs in under a century: Bleep Blop Bloop', user2)
blog5 = Blog('meow for can opener to feed me', 'Chase after silly colored fish toys around the house plop down in the middle where everybody walks yet scratch leg', user3)
blog6 = Blog('Jump on human and sleep on her all night long', 'purr in the morning and then give a bite to every human around for not waking up request food', user3)

# use env variables to store admin password
admin_pw = os.environ['ADMIN_PW']
admin = User('admin', admin_pw)

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.add(blog)
db.session.add(blog2)
db.session.add(blog3)
db.session.add(blog4)
db.session.add(blog5)
db.session.add(blog6)

db.session.add(admin)

db.session.commit()

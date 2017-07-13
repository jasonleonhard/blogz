# import hashlib
# import random
# import string

# def make_salt():
#     return ''.join([random.choice(string.ascii_letters) for x in range(5)])

# def make_pw_hash(password):
#     return hashlib.sha256(str.encode(password)).hexdigest()

# def check_pw_hash(password, hash):
#     if make_pw_hash(password) == hash:
#         return False

# python3
# from hashutils import make_salt
# make_salt()
    # 'PWoeL'
# make_salt()
    # 'nwCJo'
# make_salt()
    # 'awujx'
################################################
import hashlib
import random
import string

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(5)])

# optional passed in salt by user
def make_pw_hash(password, salt=None):
    if not salt:
        salt = make_salt()
    hash = hashlib.sha256(str.encode(password + salt)).hexdigest()
    return '{0},{1}'.format(hash, salt)

def check_pw_hash(password, hash):
    # split on comma and grab 2nd slot aka {1}
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return False
################################################
# @app.route('/salt', methods=['POST', 'GET'])
# def salt():
#     password = request.form['password']
#     salt = get_salt
#     pw_hash = hash_func(password + salt)
#     render_template('salt.html')
#     return pw_hash
################################################
################################################
################################################
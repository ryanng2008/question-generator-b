from datetime import datetime, timedelta, timezone
import os
import algorithm.mongo as db
import algorithm.encryption as enc

EXPIRES_IN = int(os.getenv('JWT_EXPIRES_IN'))


# SENIOR FUNCTIONS

def handle_register(username: str, password: str):
    # check if username exists
    # if no, hash the password and push
    user_exists = db.fetch_user(username)
    if user_exists:
        return { 'success': False, 'message': 'Username is taken' }
    hashed_password = enc.hash_password(password)
    register_user = db.post_user({ 'username': username, 'password': hashed_password })
    if register_user is None:
        return { 'success': False, 'message': 'An error occurred. Try again!' }
    access_token = enc.generate_token(username)
    return { 
        'success': True, 
        'message': 'Successfully created a new account', 
        'id': register_user, 
        'token': access_token, 
        'expires': datetime.now(timezone.utc) + timedelta(hours=EXPIRES_IN), 
        'max_age': timedelta(hours=EXPIRES_IN) 
        }
    # TODO
    # Find how to hash w/ bcrypt
    # Mongo route - post new user: return an indicator if already exists

def handle_login(username: str, password: str):
    # fetch user object with this username
    # compare hashed passwords
    # if same, return a JWT: if not, return Invalid Credentials
    user = db.fetch_user(username)
    if not user:
        return { 'success': False, 'message': 'User does not exist' }
    user_hashedpw = user['password']
    success = enc.check_password(password, user_hashedpw)
    if success:
        # This determines what's stored in the JWT. Right now it's username
        access_token = enc.generate_token(username)
        return { 
            'success': True, 
            'message': 'Login successful', 
            'token': access_token, 
            'expires': datetime.now(timezone.utc) + timedelta(hours=EXPIRES_IN), 
            'max_age': timedelta(hours=EXPIRES_IN) 
            }
    return { 'success': False, 'message': 'Wrong username or password' }



# JUNIOR FUNCTIONS? if needed
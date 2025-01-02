import bcrypt
import jwt
import os
import algorithm.mongo as db

JWT_SECRET_KEY = os.getenv('JWT_KEY')

# Hash a password using the fixed salt
def hash_password(password: str) -> bytes:
    salt = generate_fixed_salt()
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.hashpw(password, salt)

# Check if the provided password matches the hashed password
def check_password(password: str, hashed: bytes) -> bool:
    if isinstance(password, str):
        password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed)

# Generate a fixed salt with 12 rounds
def generate_fixed_salt() -> bytes:
    # 12 salt rounds
    return bcrypt.gensalt(rounds=12)

# This should work, theoretically
def generate_token(identity): # it should be able to store any data in identity
    # THIS IS THE TOKEN
    payload = {
        "identity": identity,
        # "exp": datetime.now(timezone.utc) + timedelta(hours=EXPIRES_IN)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

# This should theoretically work
def validate_token(token: str):
    try:
        data = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        # print('from validate token:')
        # print(data)
        # identity = data['identity'] # Visualise data as payload (above)
        return { 'success': True, 'message': '', 'identity': data['identity'] } # {'identity': 'adturnup'}
    except jwt.ExpiredSignatureError:
        return { 'success': False, 'message': 'Token has expired' }
    except jwt.InvalidTokenError:
        return { 'success': False, 'message': 'Token is invalid' }
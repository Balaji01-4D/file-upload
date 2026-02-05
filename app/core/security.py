import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt())

def check_password(hashed_pw: str, password: str) -> bool:
    return bcrypt.checkpw(password=password, hashed_password=hash_password)

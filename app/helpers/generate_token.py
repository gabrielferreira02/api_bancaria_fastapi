from datetime import timedelta, timezone, datetime
from jose import jwt
from app.core.vars import SECRET_KEY, ALGORITHM

def generate_token(account: str, duration=timedelta(minutes=7)):
    expiration_date = datetime.now(timezone.utc) + duration
    info = {"sub": account, "exp": expiration_date}
    token = jwt.encode(info, SECRET_KEY, ALGORITHM)
    return token
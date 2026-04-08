import random
import string

def generate_account_number() -> str:
    account = ''.join(random.choices(string.digits, k=10))
    return account
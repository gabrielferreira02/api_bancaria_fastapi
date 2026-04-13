import hashlib
import json
from app.schemas.transaction_schemas import CreateTransactionSchema

def generate_request_hash(body: CreateTransactionSchema):
    body_dict = body.dict()
    encoded_body = json.dumps(body_dict, sort_keys=True).encode('utf-8')
    return hashlib.sha256(encoded_body).hexdigest()
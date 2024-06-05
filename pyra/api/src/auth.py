import requests
import base64
import hashlib
from src.db import *
from src.constants import *

def authenticate(db, username, password):
    base64_pwd = base64_password(username, password)
    payload = { 'email': username, 'password': base64_pwd }

    session = requests.Session()
    response = session.post(Constants.IRACING_LOGIN_URL, data=payload)
    authcode = response.json()['authcode']
    if authcode == 0:
        return [session, 0]

    cust_id = response.json()['custId']
    upsert_user(db, username, cust_id, base64_pwd)

    return [session, cust_id]

def base64_password(email, password):
    phrase = password + email.lower()
    base64_hash = base64.b64encode(hashlib.sha256(phrase.encode('utf-8')).digest())
    return base64_hash.decode('utf-8')

def base64_encode(str):
    base64_hash = base64.b64encode(str.encode('ascii'))
    return base64_hash.decode('ascii')

def base64_decode(str):
    base64_hash = base64.b64decode(str.encode('ascii'))
    return base64_hash.decode('ascii')
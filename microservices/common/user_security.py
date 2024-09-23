from time import sleep
import requests
import jwt
import sys

def infinite_retry(func, expected_status, cicle=1):
    if cicle == 1500: 
        return 500
    if cicle != 1: sleep(60)
    result = func()
    if result == None: 
        infinite_retry(func, expected_status, cicle+1)
        
    if expected_status != result.status_code:
        infinite_retry(func, expected_status, cicle+1)
        
    if expected_status == result.status_code:
        sys.exit()
        return result.status_code

def logged_warning(secret_key, email):
    token = jwt.encode({"data":secret_key}, secret_key, algorithm='HS256')
    requests.put("https://mail.softkitacademy.com/security/logged", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {token}"}, json={"email":email})
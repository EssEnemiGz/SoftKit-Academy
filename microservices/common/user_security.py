from time import sleep
from user_agents import parse
from datetime import datetime
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

def logged_warning(secret_key, email, remote_addr, user_agent):
    token = jwt.encode({"data":secret_key}, secret_key, algorithm='HS256')
    device_info = get_device_info(remote_addr, user_agent)
    device_info.setdefault("email", email)
    r = requests.put("https://mail.softkitacademy.com/security/logged", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {token}"}, json=device_info)
    return r

def get_device_info(remote_addr, user_agent):
    user_ip = remote_addr
    user_agent_string = user_agent
    user_agent = parse(user_agent_string)
    date = datetime.now()

    device_info = {
        'ip': user_ip,
        'device': str(user_agent.device),
        'os': str(user_agent.os),
        'browser': str(user_agent.browser),
        'date':f"{date.day}/{date.month}/{date.year} - {date.hour}:{date.minute}",
        'date_object':date
    }
    
    return device_info
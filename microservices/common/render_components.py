import requests
import jwt

def retry(func, times: int, expected_status, actual_time=1):
    if actual_time > times:
        return None, 500
    
    result, status = func()
    if expected_status != status:
        retry(func, times, expected_status, actual_time=actual_time+1)
        
    return result, status
    
def get_component(*, session, component: str, secret_key: str, server_url: str):
    r = requests.get(f"{server_url}/api/render/components?component={component}", headers={"Content-Type":"application/json", "Accept":"application/json", "Authorization":f"Bearer {generate_jwt(session, secret_key)}"})
    if r.status_code == 200:
        return r.text, 200
    
    return None, 500

def generate_jwt(data, secret_key):
    payload = {
        "id": data.get("id"),
        "username": data.get("username"),
        "role": data.get("role"),
        "subscription": data.get("subscription"),
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token 
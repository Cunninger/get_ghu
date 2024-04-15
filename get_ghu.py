import requests
import time
import webbrowser


def get_device_code_and_user_code(client_id, scope):
    url = "https://github.com/login/device/code"
    payload = {"client_id": client_id, "scope": scope}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # 确保请求成功
    return response.json()


def poll_for_access_token(client_id, device_code):
    url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    while True:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        if "access_token" in response_data:
            return response_data["access_token"]
        if "error" in response_data:
            error = response_data["error"]
            if error == "authorization_pending":
                time.sleep(response_data.get("interval", 5))
            elif error == "slow_down":
                time.sleep(response_data.get("interval", 5) + 5)
            else:
                raise Exception(f"Error: {error}")
        else:
            raise Exception("Unexpected response from GitHub.")


# Step 1: 获取device_code和user_code
client_id = "Iv1.b507a08c87ecfe98"
scope = "read:user"
device_code_data = get_device_code_and_user_code(client_id, scope)
user_code = device_code_data["user_code"]
device_code = device_code_data["device_code"]
verification_uri = device_code_data["verification_uri"]
interval = device_code_data["interval"]

print(f"Your user code is: {user_code}")
print(f"Please go to {verification_uri} and enter this user code.")

# Step 2: 自动打开浏览器到GitHub验证页面
webbrowser.open(verification_uri)
input("Press Enter to continue...")
# Step 3: 查询获取访问令牌
try:
    access_token = poll_for_access_token(client_id, device_code)
    print("Your access token is:", access_token)
    # Save the access token to a file
    with open('ghupool.txt', 'w') as f:
        f.write(access_token)
except Exception as e:
    print(f"An error occurred: {e}")
    

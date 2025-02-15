import requests
import base64

url = "http://127.0.0.1:80"

def prepareAuthHeader(username = None, password = None):
    if (username != None or password != None):
        encodedCredentials = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8'))
        return { 'Authorization' : 'Basic ' + encodedCredentials.decode('utf-8') }
    return None

def send_post(mUrl, username = None, password = None):
    payload = {"server_version": "1.0.2"}
    response = requests.post(url=mUrl, json = payload, headers = prepareAuthHeader(username, password))
    print(f"Response for POST: {response.text}")

def send_get(mUrl, username = None, password = None):
    response = requests.get(url=mUrl, headers = prepareAuthHeader(username, password))
    print(f"Response for GET: {response.text}")

def send_put(mUrl, username = None, password = None):
    payload = {"server_version": "1.0.3", "data": "myData"}
    response = requests.put(url=mUrl, json=payload, headers = prepareAuthHeader(username, password))
    print(f"Response for PUT: {response.text}")

def send_delete(mUrl, username = None, password = None):
    payload = {"server_version": "1.0.3"}
    response = requests.delete(url=mUrl, json=payload, headers = prepareAuthHeader(username, password))
    print(f"Response for DELETE: {response.text}")

send_get(url)
send_get(url, username = 'user_name1', password = 'password')
send_get(url, username = 'user_name', password = 'password')
send_post(url)
send_post(url, username = 'user_name1', password = 'password')
send_post(url, username = 'user_name', password = 'password')
send_put(url)
send_put(url, username = 'user_name1', password = 'password')
send_put(url, username = 'user_name', password = 'password')
send_delete(url)
send_delete(url, username = 'user_name1', password = 'password')
send_delete(url, username = 'user_name', password = 'password')
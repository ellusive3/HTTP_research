from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import base64
import json

serverVersion = "1.0.1"

class HTTPHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Cache-Control', 'max-age=200') 
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Lab1 Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def __printHeaders(self):
        print('\r\n__HEADERS__\r\n'.join('{}: {}'.format(k, v) for k, v in self.headers.items()))

    def prepareResponse(self, response):
        key = self.server.get_auth_key()

        if (self.headers.get('Authorization') == None):
            self.do_AUTHHEAD()
            _response = {
                'success': False,
                'error': 'No auth header received'
            }
            self.wfile.write(bytes(json.dumps(_response), 'utf-8'))
        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.do_HEAD();
            global serverVersion
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()
            _response = {
                'success': False,
                'error': 'Invalid credentials'
            }
            self.wfile.write(bytes(json.dumps(_response), 'utf-8'))

    def do_GET(self):
        global serverVersion
        self.prepareResponse(response = {
                'server_version' : serverVersion,
                'request_type' : 'GET'
            });

    def do_POST(self):
        global serverVersion
        self.str_data = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.str_data)

        print(f"Got the version: {data['server_version']}\n")
        serverVersion = data['server_version']
        self.prepareResponse(response = {
                'server_version' : serverVersion,
                'request_type' : 'POST'
            });
    def do_PUT(self):
        global serverVersion
        self.str_data = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.str_data)
        print(f"Got the version: {data['server_version']}\n")
        print(f"Got the data: {data['data']}\n")
        serverVersion = data['server_version']
        self.prepareResponse(response = {
                'server_version' : serverVersion,
                'request_type' : 'PUT',
                'received_data' : data['data']
            })
    def do_DELETE(self):
        global serverVersion
        self.str_data = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.str_data)
        print(f"Got the version: {data['server_version']}\n")
        if (data['server_version'] == "1.0.3"):
            serverVersion = "1.0.1"
        self.prepareResponse(response = {
                'server_version' : serverVersion,
                'request_type' : 'DELETE'
            })

class CustomHTTPServer(HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=HTTPHandler):
        super().__init__(address, handlerClass)
    def set_auth(self, username, password):
        self.key = base64.b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode('utf-8')
    def get_auth_key(self):
        return self.key


if __name__ == '__main__':
    server = CustomHTTPServer(address=("127.0.0.1", 8084))
    server.set_auth('user_name', 'password')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
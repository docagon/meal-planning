import http.server
import json
import os

PORT = 8080
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'userdata')
APP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')

os.makedirs(DATA_DIR, exist_ok=True)

def data_path():
    return os.path.join(DATA_DIR, 'data.json')

def load_data():
    p = data_path()
    if os.path.exists(p):
        with open(p, 'r') as f:
            return json.load(f)
    return {}

def save_data(d):
    with open(data_path(), 'w') as f:
        json.dump(d, f, indent=2)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/data':
            d = load_data()
            body = json.dumps(d).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == '/' or self.path == '/index.html':
            with open(APP_FILE, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/data':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                incoming = json.loads(body)
                existing = load_data()
                existing.update(incoming)
                save_data(existing)
                resp = json.dumps({'ok': True}).encode()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
            except Exception as e:
                resp = json.dumps({'error': str(e)}).encode()
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass

if __name__ == '__main__':
    server = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    print('Meal Planner server on http://127.0.0.1:{}'.format(PORT))
    server.serve_forever()
